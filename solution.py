## TODO: import all necessary packages and functions
import time
import pandas as pd
import numpy as np


## These are the possible datasets currently available to analyze
chicago = 'chicago.csv'
new_york_city = 'new-york-city.csv'
washington = 'washington.csv'


def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
    if 'y' in city.lower():
        print('Looks like you want to hear about New York!  If this is not true, restart the program now!\n\n')
        return new_york_city
    if 'c' in city.lower():
        print('Looks like you want to hear about Chicago!  If this is not true, restart the program now!\n\n')
        return chicago
    else:
        print('Looks like you want to hear about Washington!  If this is not true, restart the program now!\n\n')
        return washington


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (bool) Time period information.
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no time filter.\n')

    if 'm' in time_period.lower():
        print('We will make sure to filter by month!\n\n')
        return 'month'
    if 'd' in time_period.lower():
        print('We will make sure to filter by day!\n\n')
        return 'day'
    else:
        print('Got it!  No filter necessary.\n\n')
        return "none"


def get_month(month_):
    '''Asks the user for a month and returns the specified month.

    Args:
        month_ - the output from get_time_period()
    Returns:
        (str) Month information.
    '''
    if month_ == 'month':
        month = input('\nWhich month? January, February, March, April, May, or June? Please type out the full month name.\n')
        while month.lower().strip() not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nSorry, I did not catch that - Which month? January, February, March, April, May, or June? Again, please type out the full month name.\n')
        return month.lower().strip()
    else:
        return 'none'


def get_day(day_):
    '''Asks the user for a day and returns the specified day.

    Args:
        day_ - bool - should data be filtered by day
    Returns:
        (str) Day information.
    '''
    if day_ == 'day':
        day = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        while day.lower().strip() not in ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']:
            day = input('\nSorry, I did not catch that - Which day? Please type a day M, Tu, W, Th, F, Sa, Su. \n')
        return day.lower().strip()
    else:
        return 'none'

def read_filter_data(city, time_period, month, day):
    '''
    Reads and filters the data to the data specified by the user.
    INPUT:
        city - path to the file as a string
    OUTPUT:
        df - dataframe to be used to calculate all aggregates that is filtered according to
    '''
    #Read in correct df and obtain the weekday and month data
    print('Just one moment... loading the data\n')
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month

    print('Data loaded. Now applying filters... this will be done super fast.')
    #Filter by Month if Necessary
    if time_period == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month']==month]

    #Filter by Day if Necessary
    if time_period == 'day':
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for d in days:
            if day.capitalize() in d:
                day_of_week = d
        df = df[df['day_of_week']==day_of_week]
    return df


def popular_month(df):
    '''What is the most popular month for start time?
    INPUT:
        df - dataframe returned from read_filter_data

    OUTPUT:
        most_popular_month - string of most frequent month

    '''
    print('What is the most popular month for traveling?')
    mnth = df.month.mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_popular_month = months[mnth - 1].capitalize()
    return most_popular_month


def popular_day(df):
    '''What is the most popular day of week for start time?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        popular_day - string of most popular day by number of rides

    '''
    print('What is the most popular day for traveling?')
    popular_day = df['day_of_week'].value_counts().reset_index()['index'][0]
    return popular_day


def popular_hour(df):
    '''What is the most popular hour of day for start time?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        popular_hour - int of the most popular hour

    '''
    print('What is the most popular hour of the day to start your travels?')
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df.hour.mode()[0]
    return popular_hour


def trip_duration(df):
    '''What is the total trip duration and average trip duration?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        tuple = total_trip, avg_trip - each is a pandas._libs.tslib.Timedelta objects

    '''
    print('What was the total traveling done for 2017 through June, and what was the average time spent on each trip?')
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_trip = np.sum(df['Travel Time'])
    avg_trip = np.mean(df['Travel Time'])
    return total_trip, avg_trip


def popular_stations(df):
    '''What is the most popular start station and most popular end station?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        tuple holding start_station, end_station - each is a string with the most popular start, end station
    '''
    print('Below are the most popular start and end stations respectively.')
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    return start_station, end_station


def popular_trip(df):
    '''What is the most popular trip?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        result - pandas.core.frame.DataFrame - with start, end, and number of trips for most popular trip
    '''
    result = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('What was the most popular trip from start to end?')
    return result


def users(df):
    '''What are the counts of each user type?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        users - pandas series with counts for each user type

    '''
    print('What is the breakdown of users?')
    users = df['User Type'].value_counts()
    return users


def gender(df):
    '''What are the counts of gender?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        gender - pandas.core.series.Series counts for each gender
    '''
    try:
        print('What is the breakdown of gender?')
        gender = df['Gender'].value_counts()
        return gender
    except:
        print('No gender data to share.')


def birth_years(df):
    '''What is the oldest, youngest, and most popular birth year?
    INPUT:
        df - dataframe returned from read_filter_data
    OUTPUT:
        tuple of oldest, youngest, and most popular birth year

    '''
    try:
        print('What is the oldest, youngest, and most popular year of birth, respectively?')
        oldest = np.min(df['Birth Year'])
        youngest = np.max(df['Birth Year'])
        pop_year = df['Birth Year'].mode()[0]
        return oldest, youngest, pop_year
    except:
        print('No birth year data to share.')

def calc_stat(f, df):
    print('\nCalculating statistic...\n')
    start_time = time.time()
    stat = f(df)
    print(stat)
    print("That took %s seconds." % (time.time() - start_time))


def main():
    '''Calculates and prints out the descriptive statistics about a city and time period specified by the user via raw input.

    Args:
        none.
    Returns:
        none.
    '''
    city = get_city()
    time_period = get_time_period()
    month = get_month(time_period)
    day = get_day(time_period)
    df = read_filter_data(city, time_period, month, day)

    function_list = [popular_month, popular_day, popular_hour, trip_duration, popular_stations, popular_trip, users, gender, birth_years]

    for f in function_list:
        calc_stat(f, df)

    # Restart?
    restart = input('Would you like to restart? Type \'yes\' or \'no\'.')
    if restart.lower() == 'yes':
        main()

if __name__ == '__main__':
    main()
