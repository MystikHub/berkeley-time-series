import load_feature_sets

feature_sets = load_feature_sets.get_data_feature_sets()

# Loop through the three types of feature sets
for feature_set_type in feature_sets:

    # Placeholder for the evaluation stage
    feature_set_results = []

    # ???
    for city_data in feature_set_type:

        # Start the lasso regression training and evaluation
        for data_point in city_data:
