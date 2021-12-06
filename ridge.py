from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
import load_feature_sets
import matplotlib.pyplot as plt

N_FEATURE_SETS = 3

# Result from cross-validation to be used in the final training and predictions
cross_validated_c = 0.
# Boolean toggle for whether this script does cross validation or training,
#   prediction, and evaluation
cross_validate = True

if cross_validate:

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
                    print("Processing feature set: {}, C: {}, country: {}, city: {}".format(feature_set_number, C,
                                                                                            country, city), end='\r')

                    # Get this city's data frame
                    data_frame = load_feature_sets.get_data_frame(country, city, feature_set_number)

                    shape = data_frame.shape
                    n_columns = shape[1]

                    # Find x and y for training
                    # x will be training feature sets
                    # y will be day's recorded temperature
                    x = data_frame.iloc[:, range(1, n_columns - 1)]
                    y = data_frame.iloc[:, 0]

                    # Split the data into 5 "folds" and train then evaluate
                    kf = KFold(n_splits=5)
                    for train, test in kf.split(x):
                        # Train the model
                        Ridge_regression = Ridge(alpha=(1 / C))
                        Ridge_regression.fit(x.values[train], y.values[train])

                        y_pred = Ridge_regression.predict(x.values[test])
                        error = mean_squared_error(y.values[test], y_pred)

                        total_error = total_error + error
                        total_error_count += 1

            # Save the average error for this feature set and C value
            this_feature_set_average_errors.append(total_error / total_error_count)

        feature_set_c_errors.append(this_feature_set_average_errors)
    C_range = [str(x) for x in C_range]
    plt.plot(C_range, feature_set_c_errors[0])
    plt.plot(C_range, feature_set_c_errors[1])
    plt.plot(C_range, feature_set_c_errors[2])
    plt.legend(['Feature set: past 5 years and months',
                'Feature set: past 3 years and months',
                'Feature set: past 12 months'])
    plt.xlabel('Ridge regression penalty (C)')
    plt.ylabel('Mean square error')
    plt.title("Mean square error of a Ridge regression model with different penalties")
    plt.show()

    print(feature_set_c_errors)

