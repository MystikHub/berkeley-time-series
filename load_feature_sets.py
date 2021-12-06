import csv
import numpy as np
import os
import pandas
from sklearn.model_selection import train_test_split

FEATURE_SET_DIRECTORY = './feature-sets'

# Organized by {country}/{city}/{feature_set}
Feature_Set_Map = {1: 'feature-set-1', 2: 'feature-set-2', 3: 'feature-set-3'}
def get_data_structured():

    # Check if the feature sets directory exists
    if not os.path.isdir(FEATURE_SET_DIRECTORY):
        print("Couldn't find any feature sets")
        print("Did you run 'python3 make-feature-sets.py'?")
        exit(1)

    # Dictionary to store all our data
    data = {}

    # Loop through the feature-sets directory
    for country_name in os.listdir(FEATURE_SET_DIRECTORY):

        if country_name not in data:
            data[country_name] = {}

        # Loop through the cities in each country
        for city_name in os.listdir("{}/{}".format(FEATURE_SET_DIRECTORY, country_name)):

            if city_name not in data[country_name]:
                data[country_name][city_name] = []

            # Loop through each feature set
            for feature_set in os.listdir("{}/{}/{}".format(FEATURE_SET_DIRECTORY, country_name, city_name)):

                # Open the file for reading
                # Feature sets are lists of lines, where each line is a list of the
                #   values in the csv row
                this_feature_set = []
                with open("{}/{}/{}/{}".format(FEATURE_SET_DIRECTORY, country_name, city_name, feature_set)) as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        this_feature_set.append(row)
                
                data[country_name][city_name].append(this_feature_set)

    return data

# No country or city data
def get_data_feature_sets():

    # Check if the feature sets directory exists
    if not os.path.isdir(FEATURE_SET_DIRECTORY):
        print("Couldn't find any feature sets")
        print("Did you run 'python3 make-feature-sets.py'?")
        exit(1)

    # Dictionary to store our feature sets
    # Each element in this array will correspond to one of the three feature sets
    # We defined in the "make_feature_sets.py" file
    #   It's set up this way to easily add other feature sets later rather than
    #   hard-coding feature-set-1, feature-set-2, and feature-set-3
    #
    # Furthermore, each of the feature sets in this dictionary will be a list
    #   of csv files corresponding to each country and city
    data = {}

    # Loop through the feature-sets directory
    for country_name in os.listdir(FEATURE_SET_DIRECTORY):
        print("Loading {}".format(country_name))
        # Loop through the cities in each country
        for city_name in os.listdir("{}/{}".format(FEATURE_SET_DIRECTORY, country_name)):

            # Loop through each feature set
            for feature_set in os.listdir("{}/{}/{}".format(FEATURE_SET_DIRECTORY, country_name, city_name)):

                # Trim off the ".csv"
                if feature_set.endswith(".csv"):
                    friendly_feature_set = feature_set.split(".")[0]

                if friendly_feature_set not in data:
                    data[friendly_feature_set] = []

                # Open the file for reading
                # Feature sets are lists of lines, where each line is a list of the
                #   values in the csv row
                this_feature_set = []
                with open("{}/{}/{}/{}".format(FEATURE_SET_DIRECTORY, country_name, city_name, feature_set)) as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        this_feature_set.append(row)
                
                data[friendly_feature_set].append(this_feature_set)

    return data

def get_countries():

    # Check if the feature sets directory exists
    if not os.path.isdir(FEATURE_SET_DIRECTORY):
        print("Couldn't find feature sets for any country")
        print("Did you run 'python3 make-feature-sets.py'?")
        exit(1)
    
    countries = os.listdir(FEATURE_SET_DIRECTORY)
    countries.sort()
    return countries

def get_cities(country_name):

    # Check if the country's directory exists
    if not os.path.isdir("{}/{}".format(FEATURE_SET_DIRECTORY, country_name)):
        print("Couldn't find feature sets for the country " + country_name)
        print("Did you run 'python3 make-feature-sets.py'?")
        exit(1)

    # Loop through the cities in each country
    cities = os.listdir("{}/{}".format(FEATURE_SET_DIRECTORY, country_name))
    cities.sort()
    return cities

def get_data_frame(country, city, feature_set_number):

    # Check if the city's directory exists
    if not os.path.isdir("{}/{}/{}".format(FEATURE_SET_DIRECTORY, country, city)):
        print("Couldn't find any feature sets for the city " + city)
        print("Did you run 'python3 make-feature-sets.py'?")
        exit(1)

    # See if the file we're looking for is in this directory
    if "feature-set-{}.csv".format(feature_set_number) in os.listdir("{}/{}/{}".format(FEATURE_SET_DIRECTORY, country, city)):

        # Load the pandas dataframe for this feature set
        data_frame = pandas.read_csv("{}/{}/{}/feature-set-{}.csv".format(FEATURE_SET_DIRECTORY, country, city, feature_set_number))
        return data_frame
    else:
        print("Couldn't find feature set {} for country {} and city {}".format(feature_set_number, country, city))

    
def prepare_data_split(raw_data, feature_type):
    #feature_type in 1, 2 or 3
    feature_key_str = Feature_Set_Map[feature_type]
    feature_set_raw = raw_data[feature_key_str]
    feature_set_data = []
    for city_data in feature_set_raw:
        feature_set_data.extend(city_data)
    feature_set_data = np.array(feature_set_data)
    Y,X = feature_set_data[:,0], feature_set_data[:,1:]
    x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=.08)
    return x_train, x_test, y_train, y_test
# raw_data = get_data_feature_sets()

#retrieve splitted data for feature set 1:
# x_train, x_test, y_train, y_test = prepare_data_split(raw_data, 1)
# print("Loading feature sets complete: \n-#training examples: {}\n-#test examples: {}".format(x_train.shape[0], x_test.shape[0]))