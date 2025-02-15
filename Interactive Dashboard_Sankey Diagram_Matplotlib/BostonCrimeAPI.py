# Import functions
import pandas as pd
import sankey as sk

class CRIMEAPI:

    def load_crime(self, filename):
        #self.crime = pd.read_csv(filename) #dataframe (database) - STATE VARIABLE
        self.crime = pd.read_csv(filename, dtype={'OFFENSE_DESCRIPTION': str, 'HOUR': str}, low_memory=False)

    def get_offenses(self):
        """Returns a sorted list of unique crime types (OFFENSE_DESCRIPTION)."""
        offense = self.crime[self.crime['OFFENSE_DESCRIPTION'].notna()]
        offense_types = offense['OFFENSE_DESCRIPTION'].str.lower().unique()  # Convert to lowercase for consistency
        return sorted(offense_types)  # Return a sorted list of unique crime types

    def extract_local_network(self, offense_type, min_num):
        offense = self.crime[self.crime['OFFENSE_DESCRIPTION'].notna()]
        offense_data = offense[['OFFENSE_DESCRIPTION', 'HOUR']].dropna()
        offense_data.OFFENSE_DESCRIPTION = offense_data.OFFENSE_DESCRIPTION.str.lower()
        offense_data['HOUR'] = offense_data['HOUR'].astype(str)
        offense_data = offense_data.groupby(['OFFENSE_DESCRIPTION', 'HOUR']).size().reset_index(name = 'number_crime')
        offense_data.sort_values('number_crime', ascending = False, inplace = True)
        offense_data = offense_data[offense_data['number_crime'] >= min_num]
        Offense_type = offense_data[offense_data.OFFENSE_DESCRIPTION == offense_type]
        local = offense_data[offense_data['HOUR'].isin(Offense_type['HOUR'])]
        return local

    def extract_hourly_crime(self, offense_type, min_num):
        offense_data = self.crime[self.crime['OFFENSE_DESCRIPTION'].notna()]
        offense_data = offense_data[['OFFENSE_DESCRIPTION', 'HOUR']].dropna()

        # Convert to lowercase for consistency
        offense_data['OFFENSE_DESCRIPTION'] = offense_data['OFFENSE_DESCRIPTION'].str.lower()

        # Convert HOUR to string (or keep it numeric if using Bokeh)
        offense_data['HOUR'] = offense_data['HOUR'].astype(int)

        # Filter by selected offense
        offense_data = offense_data[offense_data['OFFENSE_DESCRIPTION'] == offense_type.lower()]

        # Group by Hour to count occurrences
        offense_data = offense_data.groupby('HOUR').size().reset_index(name='crime_count')

        # Apply min_num filter
        offense_data = offense_data[offense_data['crime_count'] >= min_num]

        return offense_data


def main():
    crimeapi = CRIMEAPI()
    crimeapi.load_crime('crime2023.csv')

    offense_type = 'investigate person'
    min_num = 3

    local = crimeapi.extract_local_network(offense_type, min_num)


    sk.show_sankey(local, 'OFFENSE_DESCRIPTION', 'HOUR', vals = 'number_crime')



if __name__ == "__main__":
    main()
