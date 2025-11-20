import json
import pandas as pd
import numpy as np
from random import choice
from collections import Counter

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from catboost import CatBoostRegressor
from sklearn.metrics import root_mean_squared_error


def train_model_and_predict(train_file: str, test_file: str) -> np.ndarray:
    """
    This function reads dataset stored in the folder, trains predictor and returns predictions.
    :param train_file: the path to the training dataset
    :param test_file: the path to the testing dataset
    :return: predictions for the test file in the order of the file lines (ndarray of shape (n_samples,))
    """

    train_data = pd.read_json(train_file, lines=True)
    test_data = pd.read_json(test_file, lines=True)

    target_values = train_data["awards"]

    train_processed = train_data.drop(columns=['questions', 'keywords', "awards"])
    test_processed = test_data.drop(columns=['questions', 'keywords'])

    for idx in range(3):
        age_column = f'actor_{idx}_age'
        age_median = train_processed[age_column].median()
        train_processed[age_column] = train_processed[age_column].apply(
            lambda val: age_median if val < 0 else val
        )
        test_processed[age_column] = test_processed[age_column].apply(
            lambda val: age_median if val < 0 else val
        )

    director_list = sum((
        director_group
        for director_group in train_processed['directors']
        if isinstance(director_group, list)
    ), start=[])

    director_frequency = Counter(director_list)

    def compute_director_score(directors):
        if not isinstance(directors, list):
            return 0
        return max([director_frequency.get(director, 0) for director in directors])

    data_resources = [train_processed, test_processed]

    for data_resource in data_resources:
        for idx in range(3):
            gender_column = f'actor_{idx}_gender'
            data_resource[gender_column] = data_resource[gender_column].replace('UNKNOWN', 'Male')

        data_resource['director_impact'] = data_resource['directors'].apply(compute_director_score)

        data_resource['lead_director'] = data_resource['directors'].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'missing'
        )
        data_resource['primary_location'] = data_resource['filming_locations'].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'missing'
        )
        data_resource['dominant_genre'] = data_resource['genres'].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 'missing'
        )
        
        data_resource['engagement_score'] = np.log1p(data_resource['potions']) * np.log1p(data_resource['preorders'])
        data_resource['production_quality'] = data_resource['critics_liked'] * np.log1p(data_resource['runtime'])

        data_resource['top_actor_popularity'] = data_resource[
            ['actor_0_postogramm', 'actor_1_postogramm', 'actor_2_postogramm']
        ].max(axis=1)

        data_resource['top_actor_experience'] = data_resource[
            ['actor_0_known_movies', 'actor_1_known_movies', 'actor_2_known_movies']
        ].max(axis=1)
        

    
    list_columns = ['directors', 'filming_locations', 'genres']
    train_processed = train_processed.drop(columns=list_columns)
    test_processed = test_processed.drop(columns=list_columns)

    categorical_columns = [
        'lead_director', 'primary_location', 'dominant_genre',
        'actor_0_gender', 'actor_1_gender', 'actor_2_gender'
    ]

    categorical_indices = []
    for index, column in enumerate(train_processed.columns):
        if column in categorical_columns:
            categorical_indices.append(index)

    predictor = CatBoostRegressor(
        learning_rate=0.030,
        depth=8,
        l2_leaf_reg=5,
        random_state=42,
        verbose=False,
        train_dir='/tmp/catboost_info',
        cat_features=categorical_indices,
        early_stopping_rounds=100,
        n_estimators=1000,
        thread_count=-1
    )
    
    predictor.fit(train_processed, target_values)

    return predictor.predict(test_processed)
