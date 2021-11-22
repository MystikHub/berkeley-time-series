import csv
import os

FEATURE_SET_DIRECTORY = './feature-sets'

def get_data():

    # Check if the feature sets directory exists
    if not os.path.isdir(FEATURE_SET_DIRECTORY):
        print("Couldn't find any feature sets")
        print("Did you run 'python3 make-feature-sets.py'?")
        exit(1)

    # Map to store all our data
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