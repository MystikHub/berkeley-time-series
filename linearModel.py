from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import load_feature_sets
import matplotlib.pyplot as plt

N_FEATURE_SETS = 3
isLinear = True

if isLinear:

    # Array where each element is the average mean error for each c value
    feature_set_c_errors = []

    for feature_set_number in range(1, N_FEATURE_SETS + 1):
        this_feature_set_average_errors = []

        # Error for all cities in this feature set with this C value
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
                #   test data. Use the predictions to measure the mean square
                #   error
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
        feature_set_c_errors.append(this_feature_set_average_errors)
    print(feature_set_c_errors)
    #[[1.7575477064199365], [1.9361970663128996], [1.9769303271622913]]nu Dhabi