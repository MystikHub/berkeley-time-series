from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import load_feature_sets
import matplotlib.pyplot as plt
import math

N_FEATURE_SETS = 3

AllFeaturesIncluded = "false"

if(AllFeaturesIncluded == "true"):
    for feature_set_number in range(1, N_FEATURE_SETS + 1):
        this_feature_set_average_errors = []

        # Error for all cities in this feature set
        total_error = 0
        total_error_count = 0

        # Loop through each country
        for country in load_feature_sets.get_countries():

            # Loop through each city
            for city in load_feature_sets.get_cities(country):
                print("Processing feature set: {},  country: {}, city: {}".format(feature_set_number, country, city), end='\r')

                # Get this city's data frame
                data_frame = load_feature_sets.get_data_frame(country, city, feature_set_number)

                shape = data_frame.shape
                n_columns = shape[1]
        
                # Find x and y for training
                # x will be training feature sets
                # y will be day's recorded temperature
                x = data_frame.iloc[:, range(1, n_columns - 1)]
                y = data_frame.iloc[:, 0]

                # Train the model on training data, then make predictions on the
                # test data. Use the predictions to measure the mean square
                # error
                x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

                # Train the model
                linear_regression = LinearRegression().fit(x_train, y_train)

                y_pred = linear_regression.predict(x_test)
                error = mean_squared_error(y_test, y_pred)

                total_error = total_error + error
                total_error_count += 1
                del data_frame
                
        # Save the average error for this feature set
        this_feature_set_average_errors.append(total_error / total_error_count)
        print('this_feature_set_average_errors',this_feature_set_average_errors)

else:
    # Train the model on each city's data set
    model_total_error = 0
    baseline_total_error = 0
    n_cities_processed = 0
    total_RMSerror = 0
    total_cities = 0 # Used in the progress indicator
    for country in load_feature_sets.get_countries():
        total_cities += len(load_feature_sets.get_cities(country))

    # Loop through each country
    for country in load_feature_sets.get_countries():

        # Loop through each city
        for city in load_feature_sets.get_cities(country):
            progress = ((n_cities_processed + 1) / total_cities) * 100

            # Get this city's data frame for the "Past 5 years and months" feature set
            data_frame = load_feature_sets.get_data_frame(country, city, 1)

            shape = data_frame.shape
            n_rows = shape[0]
            n_columns = shape[1]

            # Find x and y for training
            # x = training feature sets
            # y = day's recorded temperature
            x = data_frame.iloc[:, range(1, n_columns - 1)]
            y = data_frame.iloc[:, 0]

            # Manually split the data at an 80:20 ratio
            split_train = int(n_rows * 0.8)
            split_test = int(n_rows * 0.2)
            x_train = x.head(split_train)
            y_train = y.head(split_train)
            x_test = x.tail(split_test)
            y_test = y.tail(split_test)

            # Train the model
            linear_regression = LinearRegression().fit(x_train, y_train)

            #Predictions for the model
            model_pred = linear_regression.predict(x_test)
            model_error = mean_squared_error(y_test, model_pred)
            rmse = math.sqrt(model_error)

            # Baseline predictions for the same x values
            baseline_pred = x_test.mean(axis=1)
            baseline_error = mean_squared_error(y_test, baseline_pred)

            model_total_error += model_error
            baseline_total_error += baseline_error
            n_cities_processed += 1
            total_RMSerror += rmse

    print()

    model_average_error = model_total_error / n_cities_processed
    print("Model average error: {}".format(model_average_error))

    baseline_average_error = baseline_total_error / n_cities_processed
    print("Baseline average error: {}".format(baseline_average_error))

    root_mean_average_error = total_RMSerror / n_cities_processed
    print("Root Mean Square average error: {}".format(root_mean_average_error))