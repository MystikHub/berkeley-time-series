import csv
import os

FEATURE_SET_DIRECTORY = './feature-sets'

# Organized by {country}/{city}/{feature_set}
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