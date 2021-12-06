from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import baseline
import load_feature_sets
import matplotlib.pyplot as plt

N_FEATURE_SETS = 3

# Result from cross-validation to be used in the final training and predictions
cross_validated_c = 100
# Boolean toggle for whether this script does cross validation or training,
#   prediction, and evaluation
mode = "Evaluate"

if mode == "Cross validate":

    # Array where each element is the average mean error for each c value
    feature_set_c_errors = []
    C_range = [1, 10, 100, 1000]

    for feature_set_number in range(1, N_FEATURE_SETS + 1):

        # Keep track of the errors for each C value in this feature set for a
        #   graph
        this_feature_set_average_errors = []

        # Before we train the model on our full data, do some cross validation
        #   on a subset of it
        #   Try using the values in C_range
        for C in C_range:

            # Error for all cities in this feature set with this C value
            total_error = 0
            total_error_count = 0

            # Loop through each country
            for country in load_feature_sets.get_countries():

                # Loop through each city
                for city in load_feature_sets.get_cities(country):
                    print("Processing feature set: {}, C: {}, country: {}, city: {}".format(feature_set_number, C, country, city), end='\r')

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
                    lasso_regression = Lasso(alpha=(1/C))
                    lasso_regression.fit(x_train, y_train)

                    y_pred = lasso_regression.predict(x_test)
                    error = mean_squared_error(y_test, y_pred)

                    total_error = total_error + error
                    total_error_count += 1
            
            # Save the average error for this feature set and C value
            this_feature_set_average_errors.append(total_error / total_error_count)
        
        feature_set_c_errors.append(this_feature_set_average_errors)

    plt.plot(C_range, feature_set_c_errors[0])
    plt.plot(C_range, feature_set_c_errors[1])
    plt.plot(C_range, feature_set_c_errors[2])
    plt.legend(['Feature set: past 5 years and months',
                'Feature set: past 3 years and months',
                'Feature set: past 12 months'])
    plt.xlabel('Lasso regression penalty (C)')
    plt.ylabel('Mean square error')
    plt.title("Mean square error of a lasso regression model with different penalties")
    plt.show()

    print(feature_set_c_errors)

elif mode == "Evaluate":

    # Train the model on each city's data set
    # Keep track of the lasso regression model's error and the baseline's error
    #   separately
    model_total_error = 0
    baseline_total_error = 0
    n_cities_processed = 0

    # Used in the progress indicator
    total_cities = 0
    for country in load_feature_sets.get_countries():
        total_cities += len(load_feature_sets.get_cities(country))

    # Loop through each country
    for country in load_feature_sets.get_countries():

        # Loop through each city
        for city in load_feature_sets.get_cities(country):
            progress = ((n_cities_processed + 1) / total_cities) * 100
            print("Processing country: {}, city: {}, progress: {:.1f}%".format(country, city, progress), end='\r')

            # Get this city's data frame for the "Past 5 years and months"
            #   feature set
            data_frame = load_feature_sets.get_data_frame(country, city, 1)

            shape = data_frame.shape
            n_rows = shape[0]
            n_columns = shape[1]

            # Find x and y for training
            # x will be training feature sets
            # y will be day's recorded temperature
            x = data_frame.iloc[:, range(1, n_columns - 1)]
            y = data_frame.iloc[:, 0]

            # Manually split the data at an 80:20 ratio
            # We originally wanted to use sklearn's train_test_split
            #   function, but it had no way of disabling randomization
            # Here, I did the split manually in preparation for creating
            #   feature sets for future values (where predictions depend on
            #   their previous values, i.e. their order matters)
            split_train = int(n_rows * 0.8)
            split_test = int(n_rows * 0.2)
            x_train = x.head(split_train)
            y_train = y.head(split_train)
            x_test = x.tail(split_test)
            y_test = y.tail(split_test)

            # Train the model
            lasso_regression = Lasso(alpha=(1/cross_validated_c))
            lasso_regression.fit(x_train, y_train)

            # Get the predictions done by the regression model
            model_pred = lasso_regression.predict(x_test)
            model_error = mean_squared_error(y_test, model_pred)

            # Make the baseline predictions for the same x values
            baseline_pred = x_test.mean(axis=1)
            baseline_error = mean_squared_error(y_test, baseline_pred)

            model_total_error += model_error
            baseline_total_error += baseline_error
            n_cities_processed += 1
    
    print()

    model_average_error = model_total_error / n_cities_processed
    print("Model average error: {}".format(model_average_error))

    baseline_average_error = baseline_total_error / n_cities_processed
    print("Baseline average error: {}".format(baseline_average_error))