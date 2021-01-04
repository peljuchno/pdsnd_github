import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
dow = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - number of the month to filter by, or "0" for none
        (str) day - number of the day of week to filter by, with Monday=0,
        Sunday=6, None=8 (to not confuse 7 with the last day of the week)
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # set all variables to empty strings

    city = ''
    month = ''
    day = ''
    is_filter = ''

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while city not in ['Washington', 'Chicago', 'New York City']:
        city = input("Would you like to see data for Chicago, New York City or Washington? ").title()

        if city not in ['Washington', 'Chicago', 'New York City']:
            print('Invalid input. Please type in "New York City", "Chicago" or "Washington". \n')
            continue

    # get user input for month (all, january, february, ... , june)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while is_filter not in ['Month', 'Day', 'None']:
        is_filter = input("Would you like to filter the data by month, day, or not at all? Type 'Month', 'Day' or 'None': ").title()

    # while user provides a wrong input, ask him again and display an clarifying message

        if is_filter not in ['Month', 'Day', 'None']:
            print('Invalid input. Please type "Month", "Day" or "None". \n')
            continue

        else:
            if is_filter == 'Month':
                day = '8'
                while month not in ['1', '2', '3', '4', '5', '6']:
                    month = input("Which month? Please enter a number from 1 to 6, where 1 = January, ..., 6 = June: ").title()

    # while user provides a wrong input, ask him again and display an clarifying message

                    if month not in ['1', '2', '3', '4', '5', '6']:
                        print('Invalid input. Please type one of the following: 1, 2, 3, 4, 5 or 6: \n')
                        continue

            elif is_filter == 'Day':
                month = '0'
                while day not in ['0', '1', '2', '3', '4', '5', '6']:
                    day = input("Which day? Type in a number between 0 and 6 with Monday=0, Sunday=6. ").title()

    # while user provides a wrong input, ask him again and display an clarifying message

                    if day not in ['0', '1', '2', '3', '4', '5', '6']:
                        print('Invalid input. Please type one of the following: 0, 1, 2, 3, 4, 5 or 6. \n')
                        continue

            else:
                month = '0'
                day = '8'

    print('-'*40)
    return city, month, day


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

    # load the correct csv

    df = pd.read_csv(CITY_DATA[city.lower()])

    # transform the columns 'Start Time' and 'End Time' into datetime format

    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['End Time'] = pd.to_datetime(df['End Time'], format='%Y-%m-%d %H:%M:%S')

    # add two columns for month and day of the trip, as seen by the start time

    df.insert(1, 'Month', df['Start Time'].dt.month)
    df.insert(2, 'Day', df['Start Time'].dt.weekday)

    # filter by month

    if int(month) > 0:
        df = df[df['Month'] == int(month)]

    # filter by day

    if int(day) < 8:
        df = df[df['Day'] == int(day)]

    # could also filter by both, month and day, but I believe this has not been asked for

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    print("The most common month: {}".format(months[df['Month'].value_counts().idxmax()]))

    # display the most common day of week

    print("The most common day of the week: {}".format(dow[df['Day'].value_counts().idxmax()]))

    # display the most common start hour

    df.insert(1, 'Hour', df['Start Time'].dt.hour)
    print("The most common start hour: {}".format(df['Hour'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print("The most common start station: {}.".format(df['Start Station'].value_counts().idxmax()))

    # display most commonly used end station

    print("The most common end station: {}.".format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip

    df.insert(1, 'Start-End-Combination', df['Start Station']+' to '+df['End Station'])

    print("The most frequent combination of start station and end station trip is from {}.".format(df['Start-End-Combination'].value_counts().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    print('Total travel time: {} hours.'.format(round(df['Trip Duration'].sum()/60/60,2)))

    # display mean travel time

    print('Mean travel time: {} minutes.'.format(round(df['Trip Duration'].mean()/60,2)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    df.insert(1, 'type_subscriber', df['User Type'] == 'Subscriber')
    df.insert(1, 'type_customer', df['User Type'] == 'Customer')

    print('Count of user type "Customer": {}.'.format(df['type_subscriber'].sum()))
    print('Count of user type "Subscriber": {}.\n'.format(df['type_customer'].sum()))

    # Display counts of gender

    try:
        df.insert(1, 'gender_m', df['Gender'] == 'Male')
        df.insert(1, 'gender_f', df['Gender'] == 'Female')
        df.insert(1, 'gender_nan', df['Gender'].isnull())

        print('Count of male users: {}.'.format(df['gender_m'].sum()))
        print('Count of female users: {}.'.format(df['gender_f'].sum()))
        print('Count of unknown gender: {}.\n'.format(df['gender_nan'].sum()))
    except:
        print('No gender information available.')

    # Display earliest, most recent, and most common year of birth

    try:
        print('Earliest birthyear: {}.'.format(round(df['Birth Year'].min())))
        print('Most recent birthyear: {}.'.format(round(df['Birth Year'].max())))
        print('Most common birthyear: {}.\n'.format(round(df['Birth Year'].value_counts().idxmax())))
    except:
        print('No birthyear information available.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Ask whether user wants to see individual trip data and then show five rows.

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

# Remove unneeded columns

        try:
            df.pop('gender_m')
            df.pop('gender_f')
            df.pop('gender_nan')
            df.pop('Start-End-Combination')
            df.pop('Hour')
            df.pop('Day')
            df.pop('Month')
            df.pop('type_subscriber')
            df.pop('type_customer')
        except:
            df.pop('Start-End-Combination')
            df.pop('Hour')
            df.pop('Day')
            df.pop('Month')
            df.pop('type_subscriber')
            df.pop('type_customer')

        i = 0
        j = 5
        individual_trip_data = input('Would you like to see individual trip data? Type "yes" or "no".\n')
        while individual_trip_data == 'yes':
            print(df[i:j])
            i += 5
            j += 5
            individual_trip_data = input('Would you like to see 5 more rows? Type "yes" or "no".\n')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
