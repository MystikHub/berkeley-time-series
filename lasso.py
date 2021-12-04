from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import load_feature_sets
import matplotlib.pyplot as plt

feature_sets = load_feature_sets.get_data_frames()

# Result from cross-validation to be used in the final training and predictions
cross_validated_c = 0.
# Boolean toggle for whether this script does cross validation or training,
#   prediction, and evaluation
cross_validate = True
if cross_validate:
    average_errors = []
    # Loop through the three types of feature sets
    for feature_set_type, feature_set in feature_sets.items():

        # Before we train the model on our full data, do some cross validation
        #   on a subset of it
        #   Try using the following 5 values for C
        C_range = [1, 10, 100, 1000]

        # Keep track of the errors for each C value in this feature set for a
        #   graph
        this_feature_set_average_errors = []
        for C in C_range:

            # Error for all cities in this feature set with this C value
            total_error = 0

            # Look at each city in this feature set
            for data_frame in feature_set:
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
            
            # Save the average error for this feature set and C value
            this_feature_set_average_errors.append(total_error / len(feature_set))
        
        average_errors.append(this_feature_set_average_errors)

    plt.plot(C_range, average_errors[0])
    plt.plot(C_range, average_errors[1])
    plt.plot(C_range, average_errors[2])
    plt.legend(['Feature set: past 5 years and months',
                'Feature set: past 3 years and months',
                'Feature set: past 12 months'])
    plt.xlabel('Lasso regression penalty (C)')
    plt.ylabel('Mean square error')
    plt.title("Mean square error of a lasso regression model with different penalties")
    plt.show()

    print(average_errors)

else:
    # Training and prediction on the full data set
    for all_cities in feature_set_type:

        # Start the lasso regression training and evaluation
        for city_data in all_cities:
            lasso_regression = Lasso(alpha=(1/cross_validated_c))
            lasso_regression.fit(feature_sets, temperatures)