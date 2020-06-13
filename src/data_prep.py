import pandas as pd
import numpy as np
from imblearn.under_sampling import RandomUnderSampler

def import_process_chi_traffic_accident_data():
    """
    Imports and prepares Chicago's traffic accident for exploratory data analysis.
    Develops the boolean classification label "Incapacitated or Fatal".

    Parameters
    ----------

    Return
    -------

    accidents : dataframe
        The dataset used for EDA.

    """

    accidents = pd.read_csv('data/traffic_crashes.csv')

    # Develop classification flag.
    # Positive represents the accideent resulted in incapacitation and/or fatality.
    accidents['crash_date'] = pd.to_datetime(accidents['CRASH_DATE'])
    accidents['crash_year'] = accidents['crash_date'].dt.year
    accidents['fatal_bool'] = np.where(accidents['MOST_SEVERE_INJURY'] == 'FATAL', 1, 0)
    accidents['incap_bool'] = np.where(accidents['MOST_SEVERE_INJURY'] == 'INCAPACITATING INJURY', 1, 0)
    accidents['fatal_incap'] = accidents['fatal_bool'] + accidents['incap_bool']

    return accidents


def train_split_resample(dataset):
    '''
    Obtains, splits and resampled (due to imbalances) the data required for the models.
    
    Parameters
    ----------
    dataset: dataframe
        Dataset generated from "import_process_chi_traffic_accident_data" function.
    
    Returns
    -------
    X_train_resampled: arr
        Independent variables for training models. Adjusted from imbalance.
    
    y_train_resampled: arr
        Depedent variables for training models. Adjusted from imbalance.
    
    X_test: arr
        Independent variables for testing models.
    
    y_test: arr
        Dependent variables used to evaluate models.
        
    '''
    
    accidents = import_process_chi_traffic_accident_data()
    X = accidents[['POSTED_SPEED_LIMIT', 'CRASH_HOUR', 'CRASH_DAY_OF_WEEK', 'TRAFFIC_CONTROL_DEVICE', 'TRAFFICWAY_TYPE',
                   'FIRST_CRASH_TYPE', 'PRIM_CONTRIBUTORY_CAUSE']].copy
    y = accidents[['fatal_incap']]

    trfc_cntrl = pd.get_dummies(X['TRAFFIC_CONTROL_DEVICE'])
    prime_cause = pd.get_dummies(X['PRIM_CONTRIBUTORY_CAUSE'])
    first_crash = pd.get_dummies(X_['FIRST_CRASH_TYPE'])
    trafficway = pd.get_dummies(X['TRAFFICWAY_TYPE'])

    concat_lst = [X[['POSTED_SPEED_LIMIT', 'CRASH_HOUR', 'CRASH_DAY_OF_WEEK']], trfc_cntrl, prime_cause, first_crash, trafficway]
    X_concat = pd.concat(concat_lst, axis=1).values

    X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.20, random_state=42)
    
    sampler = RandomUnderSampler(random_state=42)
    sampler.fit(X_train, y_train)
    X_train_resampled, y_train_resampled = sampler.fit_resample(X_train, y_train)
    
    return X_train_resampled, y_train_resampled, X_test, y_test

def timer(start_time=None):
    '''
    Use to calculate time required to optimize models and its parameters.
    
    Parameters
    ----------
    start_time: datetime
        The date and time to start the timer.
    
    Return
    --------
    
    '''
    
    if not start_time:
        start_time = datetime.now()
        return start_time
    elif start_time:
        thour, temp_sec = divmod((datetime.now() - start_time).total_seconds(), 3600)
        tmin, tsec = divmod(temp_sec, 60)
        print('\n Time taken: %i hours %i minutes and %s seconds.' % (thour, tmin, round(tsec, 2)))