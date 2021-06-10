import time
import pandas as pd
# By importing package you can access their functions
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ["January", "February", "March", "April", "May", "June"]
day_of_week_list=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city_list=["Chicago", "New York", "Washington"]
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York or Washington?\n')
    if city.title() not in city_list:
        print("Invalid city name, Please select Chicago, New York or Washington")
        return city, None, None, "error"


    filter_value = input('Would you like to filter data by month, day or both?\n')

    if filter_value.title() == "Month":
        month = get_month()
        if month == "error":
            return city, month, None, "error"
        else:
           return city, month, None, "no_error"

    elif filter_value.title() == "Day":
        day = get_day()
        if day == "error":
            return city, None, day, "error"
        else:
            return city, None, day, "no_error"

    elif filter_value.title() == "Both":
        month = get_month()
        if month == "error":
            return None, None, None, "error"
        day = get_day()
        if day == "error":
            return None, None, None, "error"
    else:
        print('Invalid filter, Please select month, day or both')
        return None, None, None, "error"

    print('-'*40)
    return city, month, day, "no_error"

def get_month():
    # TO DO: get user input for month (january, february, ... , june)
    month = input('Which month - January, February, March, April, May, or June?\n')
    while month.title() not in month_list:
        print("Invalid month, Please select month - January, February, March, April, May, or June")
        return "error"
    return month

def get_day():
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n')
    while day.title() not in day_of_week_list:
        print("Invalid day of the week, Please select day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday")
        return "error"
    return day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    if month is not None:
        df['month'] = df['Start Time'].dt.month
    # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1

            # filter by month to create the new dataframe
            df = df[df['month'] == month]
    if day is not None:
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # TO DO: display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print('Most common day of the week:', popular_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', start_station)


    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', end_station)


    # TO DO: display most frequent combination of start station and end station trip
    start_end_station=df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most frequent combination of start station and end station trip: ', start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time: ", total_time)

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("display mean travel time: ", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw details as user requests to have more details"""
    count = 0
    while True:
        request = input("Would you like to see 5 more lines of raw data\n")
        count+=1
        if request.lower() != 'yes':
             break

        print(df.head(5*count))

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:\n", user_types)

    if 'Gender' in df :
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print("Counts of gender:\n", gender)

    if 'Birth Year' in df :
        # TO DO: Display earliest, most recent, and most common year of birth
        recent_year = df['Birth Year'].iloc[0]
        print("Most recent year of birth: ", recent_year)

        earliest_year = df['Birth Year'].iloc[-1]
        print("Earliest year of birth: ", earliest_year)

        common_year = df['Birth Year'].mode()[0]
        print("Most common year of birth: ", common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, error_alert = get_filters()

        if error_alert == "error":
            break

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter y or n\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
