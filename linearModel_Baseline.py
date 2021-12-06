from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import load_feature_sets
import matplotlib.pyplot as plt
import math

 
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
        split_train = int(n_rows * 0.8)
        split_test = int(n_rows * 0.2)
        x_train = x.head(split_train)
        y_train = x.head(split_train)
        x_test = x.tail(split_test)
        y_test = x.tail(split_test)

        # Train the model using the train sets created
        linear_regression = LinearRegression()
        linear_regression.fit(x_train, y_train)

        #make predictions using the test data set
        y_pred = linear_regression.predict(x_test)

        #print("Coefficients: \n", linear_regression.coef_)
        error = mean_squared_error(y_test, y_pred)
        rmse = math.sqrt(error)

        total_error += error
        total_RMSerror += rmse
        n_cities_processed += 1
    
average_error = total_error / n_cities_processed
root_mean_average_error = total_RMSerror / n_cities_processed
print()
print("Average Mean Square Error:\n")
print(average_error)
print("Average Root Mean Square Error:\n")
print(root_mean_average_error)
#print("Coefficients: \n", linear_regression.coef_)
plt.scatter(x_test, y_test, color="black", label="Test Data Set(Temperature for Past 5 Years and Months)", marker="v")
plt.plot(x_test, y_pred, color="blue", linewidth=1)
plt.xlabel('Feature Set: Past 5 years and months')
plt.ylabel('Temperature')
plt.title("Comparision of performance with a baseline model of previous data point")
plt.legend()
plt.show()