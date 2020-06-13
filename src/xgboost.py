import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import RandomizedSearchCV

from data_prep import import_process_chi_traffic_accident_data, train_split_resample, timer


if __name__ == "__main__":

    accidents = import_process_chi_traffic_accident_data()
    
    X_train_resampled, y_train_resampled, X_test, y_test = train_split_resample(accidents) 


    params = {
        "loss" : ["deviance"], # means log loss. appropriate for classification
        "learning_rate" : [0.01, 0.1, 0.5, 1.0],
        "n_estimators" : [10, 25, 50],
        "criterion" : ['friedman_mse', 'mse', 'mae'],
        "max_depth" : [3, 5, 7], 
        "min_samples_split" : [0.1, 0.25, 0.5, 1.0],
        'subsample': [0.6, 0.8, 1.0],
        "random_state": [1]
    }

    gdbt = RandomizedSearchCV(estimator=GradientBoostingClassifier(), n_iter=50, param_distributions=rs_params_gdbt, cv=5, n_jobs=-1, scoring = 'roc_auc')

    start_time = timer(None)
    gdbt.fit(X_train_resampled, y_train_resampled)
    y_pred = gdbt.predict(X_test)

    print(timer(start_time))
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))