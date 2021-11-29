import csv
import os
import math
import numpy as np
DEBUG_MAX_PROCESSED_LINES = -1
FEATURE_SET_DIRECTORY = './feature-sets'
FEATURE_SET_TYPES = [
    "Past 5 years and months",
    "Past 3 years and months",
    "Past 12 months"
]

# CSV Format
# 0: Date of data capture
# 1: Temperature on that day in degrees celsius
# 2: Temperature uncertainty
# 3: City
# 4: Country
# 5: Latitude
# 6: Longitude

# Create a directory for our feature sets if it doesn't already exist
if os.path.isdir(FEATURE_SET_DIRECTORY):
    # Make sure it's empty before writing over any of the user's data
    if len(os.listdir(FEATURE_SET_DIRECTORY)) != 0:
        print('Error: "{}" must be empty'.format(FEATURE_SET_DIRECTORY))
        exit(0)
else:
    os.makedirs(FEATURE_SET_DIRECTORY)

# Make sure the data file exists
if "GlobalLandTemperaturesByCity.csv" not in os.listdir('.'):
    print("Could not find the berkely data set")
    exit(0)
    
# Set up CSV reader
countries = {}
berkeley_data = open('GlobalLandTemperaturesByCity.csv', 'r',encoding='utf-8')
csv_reader = csv.reader(berkeley_data)

# Function to clean our data points
# csv_row: [string]
# returns: [string] or None
def clean_data_point(csv_row):
    # Placeholder function, returns its input
    return csv_row

# Read data from CSV reader to our country map
line_count = 0
for row in csv_reader:
    if line_count > DEBUG_MAX_PROCESSED_LINES and DEBUG_MAX_PROCESSED_LINES != -1:
        break

    # Skip the CSV header
    if line_count == 0:
        line_count += 1
        continue

    country = row[4]
    city = row[3]
    
    # Each country in our countries map is another map of cities
    if country not in countries:
        countries[country] = {}
    
    # And each city in each country is a list of temperature data points
    if city not in countries[country]:
        countries[country][city] = []
    
    # Clean our data set
    cleaned_line = clean_data_point(row)

    # Some lines might be rejected
    if cleaned_line != None:
        countries[country][city].append(row)

    if line_count % 100000 == 0:
        print("Read {} data points\r".format(line_count), end='')

    line_count += 1


# Takes a feature set type and a city's data then and returns a list of strings
#   to be written to that city's feature set file
# feature_set_type: string
# city_data: [[string]]
# returns: [string]
def get_feature_set_old(feature_set_type, city_data):
    # Placeholder, retuns a list of strings of the city's data
    return_list = []
    for csv_row in city_data:
        this_line = ""
        first_index = True

        for value in csv_row:
            if first_index:
                this_line += value
                first_index = False
            else:
                this_line += "," + value
        return_list.append(this_line + "\n")
    return return_list

def get_feature_set(feature_set_type, city_data):
    # Placeholder, retuns a list of strings of the city's data
    return_list = []
    last_valid_tem = -1
    total = len(city_data)

    for index, csv_row in enumerate(city_data):

        #padding empty values.
        if csv_row[1]:
            tem = float(csv_row[1])
            last_valid_tem = tem

        else:
            csv_row[1] = last_valid_tem + np.random.uniform(-1, 1)
        tgt_tem = csv_row[1]
        src = []
        if feature_set_type == "Past 5 years and months":
            p5_y_index = [index-12*y for y in range(1,6)]
            p5_m_index = [index-1*m for m in range(1,6)]
            all_ids = p5_y_index+p5_m_index
        elif feature_set_type == "Past 3 years and months":
            p3_y_index = [index-12*y for y in range(1,4)]
            p3_m_index = [index-1*m for m in range(1,4)]
            all_ids = p3_y_index+p3_m_index
        else:
            all_ids = [index-1*m for m in range(1,13)]

        for i in all_ids:
            if i in range(0, total):
                src.append(city_data[i][1])
            else:
                src.append(last_valid_tem + np.random.uniform(-1, 1))
        feature_data = [tgt_tem] + src
        # first element is tgt, rest is src.
        feature_data = [str(t) for t in feature_data]


        return_list.append(','.join(feature_data)+'\n')
    return return_list

# Loop through our csv and make files and folders for each data point
progress = 0
for country, country_data in countries.items():
    percentage_complete = 100 * progress / (len(countries))
    print("Processing {:<15} ({:.1f}% complete)\r".format(country, percentage_complete), end='')
    
    # Loop through each city
    for city, city_data in country_data.items():
        # Make a folder for this country and city if it doesn't already exist
        country_city_path = "{}/{}/{}".format(FEATURE_SET_DIRECTORY, country, city)
        if not os.path.isdir(country_city_path):
            os.makedirs(country_city_path)
        
        # Open a file for each feature set
        feature_type_index = 1
        for feature_set_type in FEATURE_SET_TYPES:
            # Start appending into the feature set file
            data_file_path = country_city_path + "/feature-set-"
            data_file_path += str(feature_type_index) + ".csv"

            data_file = open(data_file_path, 'a')

            # The function below takes a feature set type and a 
            feature_set = get_feature_set(feature_set_type, city_data)
            data_file.writelines(feature_set)
            data_file.close()

            feature_type_index += 1
    
    progress += 1

print("Processing complete! Data has been written to " + FEATURE_SET_DIRECTORY)
print("It's organized by: feature-sets/{country}/{city}/feature-set-n.csv")