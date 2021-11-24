import load_feature_sets

feature_sets = load_feature_sets.get_data_feature_sets()

# What percentage of the data should be used in cross-validating a C value for
#   the lasso regression penalty
#   The full dataset contains approximately 8,500,000 data points, so this value
#   will provide around 85,000 data points to be considered in the
#   cross-validation stage
cross_validation_ratio = 0.01
cross_validated_c = 0.1

# Loop through the three types of feature sets
for feature_set_type in feature_sets:

    # Placeholder for the evaluation stage
    feature_set_results = []

    # Before we train the model on our full data, do some cross validation
    #   on a subset of it
    #   Try using the following 5 values for C
    if cross_validate:
        for C in [0.1, 1, 10, 100, 1000]:

            # Loop through the subset specified by cross_validation_ratio
            for all_cities in feature_set_type:

                # Start the lasso regression training and evaluation
                for city_data in all_cities[:(len(all_cities) * cross_validation_ratio)]:
                    lasso_regression = Lasso(alpha=(1/C))
                    lasso_regression.fit(feature_sets, temperatures)
                    print("C={}\t{}, {}".format(C, lasso_regression.intercept_, lasso_regression.coef_))
    else:
        # Training and prediction on the full data set
        for all_cities in feature_set_type:

            # Start the lasso regression training and evaluation
            for city_data in all_cities:
                lasso_regression = Lasso(alpha=(1/cross_validated_c))
                lasso_regression.fit(feature_sets, temperatures)