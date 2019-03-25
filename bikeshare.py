#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8
# Udacity - Programming for Data Science
# Explore US Bikeshare Data Project - Jason Rodrigues

import time
import pandas as pd
import numpy as np
import datetime
cities = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter city ({}):\n".format(cities).title()).casefold()
    while city not in cities:
        city = input("Please enter one of the following cities: {}: \n".format(cities).title()).casefold()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Enter month ({}): \n".format(months).title()).casefold()
    while month not in months:
        month = input("Please enter one of the following months: ({}): \n".format(months).title()).casefold()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day of week ({}): \n".format(days).title()).casefold()
    while day not in days:
        day = input("Please enter one of the following: ({}): \n".format(days).title()).casefold()

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # create a Start & End stations combo column
    df['Start/End Stations'] = df['Start Station'] + "/" + df['End Station']
    
    # convert the Start & End Times columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])    
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # create new column for start time hour
    df['hour'] = df['Start Time'].dt.hour
    
    # rename first column to "Trip Number"
    df.columns.values[0] = 'Trip Number'

    # convert trip durations to timedelta format
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], 'S')
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

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
    print("The most common month is: ", months[df['month'].mode()[0]].title())

    # TO DO: display the most common day of week
    print("The most common day is: ", df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    common_hour = str(df['hour'].mode()[0])
    print("The most common hour is: ", datetime.datetime.strptime(common_hour, "%H").strftime("%I %p"))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common starting station is: ", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most common ending station is: ", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print("The most common start/end station combo is: ", df['Start/End Stations'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time (for all trips) is: ', str(total_travel_time))

    # TO DO: display mean travel time
    avg_trip_travel_time = df['Trip Duration'].mean()
    print('Average travel time (for all trips) is: ', str(avg_trip_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
   
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("The number of trips by user type is:\n(Note: \'NaN\' indicates no user type data exists for trip)\n{}\n".format(df['User Type'].value_counts(dropna = False).to_string()))


    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print("The number of trips by user gender is :\n(Note: \'NaN\' indicates no user gender data exists for trip)\n{}\n".format(df['Gender'].value_counts(dropna = False).to_string()))
    else:
        print("No gender data exists for this city")
    

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = int(df['Birth Year'].min())
        latest_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode())
        print("Birth year stats of users:\nEarliest birth year: {}\nLatest birth year: {}\nMost common birth year: {}".format(earliest_birth_year, latest_birth_year, most_common_birth_year))
    else:
        print("No birth year data exists for this city")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    # function for requesting whether or not to display raw data
    def see_data():
        # compile standardized view of raw data
        df2 = pd.read_csv(CITY_DATA[city])
        # get user input and display raw data or end/restart
        see_more = input("\nWould you like to see the raw data? Enter yes or no: ")
        while see_more.lower() not in ['yes', 'y', 'no', 'n']:
            try:
                see_more = input("Would you like to see the raw data?  Please enter only yes or no: ")
            except:
                see_more = input("Would you like to see the raw data?  Please enter only yes or no: ")
            if see_more.lower() in ('yes', 'y', 'no', 'n'):
                break
        if see_more.lower() in ('yes' or 'y'):
            i=0
            print(df2[i:i+5])
            even_more = input("\nWould you like to see more? Enter yes or no.")            
            while even_more not in ('no', 'n'):
                if even_more in ('yes', 'y') and i <= (len(df2) - 5):
                    i += 5
                    print(df2[i:i+5])
                    even_more = input("Would you like to see more? Enter yes or no: ")
                else:
                    if i > (len(df2) - 5):
                        break
                    try:
                        even_more = input("Would you like to see more? Please enter only yes or no: ")
                    except:
                        even_more = input("Would you like to see more? Please enter only yes or no: ")

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print("City: " + city.title())
        print("Month: " + month.title())
        print("Day: " + day.title())

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_data()
        
        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() not in ('yes', 'y'):
            break


if __name__ == "__main__":
	main()


# In[ ]:


# 

