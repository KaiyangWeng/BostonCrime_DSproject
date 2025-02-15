from bokeh.models import ColumnDataSource
from BostonCrimeAPI import CRIMEAPI
import matplotlib.pyplot as plt
import bokeh.plotting as bp
import sankey as sk
import panel as pn
import io


# Initialize Panel and API
pn.extension()
api = CRIMEAPI()
api.load_crime('crime2023.csv')

# Widgets
offense_select = pn.widgets.Select(name='Offense', options=api.get_offenses(), value='investigate person')
min_num_slider = pn.widgets.IntSlider(name="Min Number",start= 1, end=880, step= 5, value = 10)

# Plotting widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1000)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=1000)

def get_catalog(offense, min_num):
    global local
    local = api.extract_local_network(offense, min_num)
    table = pn.widgets.Tabulator(local, selectable=False)
    return table


def get_plot(offense, min_num, width, height):
    return sk.make_sankey(local, 'OFFENSE_DESCRIPTION', 'HOUR', vals = 'number_crime', width = width, height = height)


def extract_hourly_crime(offense_type, min_num):
    """Extracts hourly crime data for plotting."""
    offense_data = api.crime[api.crime['OFFENSE_DESCRIPTION'].notna()]
    offense_data = offense_data[offense_data['HOUR'].notna()]

    offense_data['OFFENSE_DESCRIPTION'] = offense_data['OFFENSE_DESCRIPTION'].str.lower()
    offense_data['HOUR'] = offense_data['HOUR'].astype(int)

    offense_data = offense_data[offense_data['OFFENSE_DESCRIPTION'] == offense_type.lower()]
    offense_data = offense_data.groupby('HOUR').size().reset_index(name='crime_count')

    offense_data = offense_data[offense_data['crime_count'] >= min_num]
    return offense_data


# Bokeh Widget (Bar Chart)
def create_bokeh_plot(offense_type, min_num):
    data = extract_hourly_crime(offense_type, min_num)

    if data.empty:
        return bp.figure(title="No Data Available")

    source = ColumnDataSource(data)
    p = bp.figure(title=f"Crime Count by Hour: {offense_type}",
                  x_axis_label="Hour",
                  y_axis_label="Crime Count",
                  width=600,
                  height=400)

    p.vbar(x='HOUR', top='crime_count', width=0.5, source=source, color="navy")
    return p


# Matplotlib Widget (Line Plot)
def create_matplotlib_plot(offense_type, min_num):
    data = extract_hourly_crime(offense_type, min_num)

    if data.empty:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No Data Available", horizontalalignment='center', verticalalignment='center')
        return fig

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(data['HOUR'], data['crime_count'], marker='o', linestyle='-', color='red')
    ax.set_title(f"Crime Trends by Hour: {offense_type}")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Crime Count")
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    return pn.pane.Image(buf, width=600)


# Table Widget
def create_data_table(offense_type, min_num):
    data = extract_hourly_crime(offense_type, min_num)
    return pn.widgets.DataFrame(data, fit_columns=True)


# Bind widgets to functions
catalog = pn.bind(get_catalog, offense_select, min_num_slider)
plot = pn.bind(get_plot, offense_select, min_num_slider, width, height)
bokeh_plot = pn.bind(create_bokeh_plot, offense_select, min_num_slider)
matplotlib_plot = pn.bind(create_matplotlib_plot, offense_select, min_num_slider)
crime_table = pn.bind(create_data_table, offense_select, min_num_slider)

# Dashboard Widget Containers
card_width = 320
search_card = pn.Card(
    pn.Column(offense_select, min_num_slider),
    title="Search", width=card_width, collapsed=False
)

plot_card = pn.Card(
    pn.Column(width, height),
    title="Plot", width=card_width, collapsed=True
)

# Layout for Dashboard**
layout = pn.template.FastListTemplate(
    title="Crime & Hour Explorer",
    sidebar=[search_card, plot_card],
    main=[
        pn.Tabs(
            ("Associations", catalog),
            ("Network", plot),
            ('Visualization',pn.Row(bokeh_plot, matplotlib_plot)),
            ('Crime_Table', pn.Row(crime_table)),
            active=1)], header_background='#A93226')

layout.servable()
layout.show()
