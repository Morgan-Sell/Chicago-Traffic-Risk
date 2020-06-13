import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

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

def plot_accident_results_by_hour_of_the_day(dataset):
    """
    Creates a two-axis bar-line chart that summarizes accidents and their results by hour of the day.

    Parameters
    ----------
    dataset: dataframe
        Dataset generated from "import_process_chi_traffic_accident_data" function.


    Return
    -------

    """

    hour_grpd = dataset.groupby(['CRASH_HOUR', 'fatal_incap']).agg({'fatal_incap':'count'})
    hour_grpd.columns = ['count']
    hour_grpd.reset_index(inplace=True)
    hour_no_fatal = hour_grpd[hour_grpd['fatal_incap'] == 0]
    hour_fatal_DF = hour_grpd[hour_grpd['fatal_incap'] == 1]

    hour_fatal_df = pd.DataFrame()
    hour_fatal_df['hour'] = pd.Series(range(0,24))
    hour_fatal_df['num_not_fatal'] = np.array(hour_grpd[hour_grpd['fatal_incap'] == 0]['count'])
    hour_fatal_df['num_fatal'] = np.array(hour_grpd[hour_grpd['fatal_incap'] == 1]['count'])
    hour_fatal_df['total'] = hour_fatal_df['num_not_fatal'] + hour_fatal_df['num_fatal']
    hour_fatal_df['prcnt_fatal'] = hour_fatal_df['num_fatal'] / hour_fatal_df['total']

    pos_hour = list(range(len(hour_fatal_df['hour'])))
    width = 0.4

    fig, ax1 = plt.subplots(figsize=(14,7))

    ax1.bar(pos_hour, hour_fatal_df['num_not_fatal'], width, alpha=0.5, color='b', label='Not Fatal')
    ax1.bar([p + width for p in pos_hour], hour_fatal_df['num_fatal'], width, alpha=0.5, color='orange', label='Fatal')
    ax1.set_ylabel('Number of Accidents', fontsize=12)
    ax1.set_xticks([p + 0.5 * width for p in pos_hour])
    ax1.set_xticklabels(hour_fatal_df['hour'])
    ax1.set_xlabel('Hour', fontsize=12)
    ax1.set_title('Total Traffic Accidents by the Hour', fontsize=28, fontweight='bold')

    ax1.set_xlim(-0.5, len(hour_fatal_df))

    ax1.legend(loc='upper left', facecolor='white', fontsize=11)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.grid(color=None, linestyle='None')
    ax1.set_facecolor('white')

    # Share x-axis
    ax2=ax1.twinx()

    ax2.set_ylabel('% of Accidents Resulting in Fatalities', fontsize=12)
    ax2.set_ylim(0,0.05)
    ax2.plot([p + width/2 for p in pos_hour], hour_fatal_df['prcnt_fatal'] , color='red', linestyle='--', linewidth=3,
             label='% - Fatal')

    ax2.legend(bbox_to_anchor=(0, 0, 0.105, 0.90), facecolor='white', fontsize=11)
    ax2.grid(color=None, linestyle='None')
    #plt.rcParams['font.family'] = 'garamond'

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    plt.tight_layout();


def plot_accidents_by_speed_limit(dataset):
    """
    Shows the percentage of accidents that resulted in fatality or incapacitation by the posted speed limit.

    Parameters
    ----------
    dataset: dataframe
        Dataset generated from "import_process_chi_traffic_accident_data" function.

    Return
    ------

    """
    accidents_spd_lim = dataset[dataset['POSTED_SPEED_LIMIT'] % 5 == 0].copy()
    spd_lim_pivot = accidents_spd_lim.pivot_table(index='POSTED_SPEED_LIMIT', columns='fatal_incap', values='CRASH_RECORD_ID',
                                              fill_value=0, aggfunc='count').reset_index()
    #spd_lim_pivot.drop('fatal_incap', axis=1, inplace=True)
    spd_lim_pivot.rename({0:'num_not_fatal', 1:'num_fatal'}, axis=1, inplace=True)
    spd_lim_pivot['total'] = spd_lim_pivot['num_not_fatal'] + spd_lim_pivot['num_fatal']
    spd_lim_pivot['prcnt_fatal'] = spd_lim_pivot['num_fatal'] / spd_lim_pivot['total']

    fig, ax = plt.subplots(figsize=(12,6))
    spd_arr = spd_lim_pivot['POSTED_SPEED_LIMIT'].values
    spd_prcnt_fatal_arr = spd_lim_pivot['prcnt_fatal'].values
    spd_total_arr_nrml = spd_lim_pivot['total'].values / sum(spd_lim_pivot['total'])

    ax.bar(spd_arr, spd_prcnt_fatal_arr , color='green', alpha=0.7, width=2)
    ax.set_title('Fatal Accidents by Posted Speed Limit', fontsize=26, fontweight='bold')
    ax.set_xlabel('Posted Speed Limit (mph)', fontsize=14)
    ax.set_ylabel('% - Total Accidents', fontsize=14)
    #plt.rcParams['font.family'] = 'garamond'

    plt.tight_layout();

def plot_fatal_accident_by_day_of_week(dataset):
    """
    Plots the percentage of accidents that resulted in fatality or incapacitation by the posted speed limit.

    Parameters
    ----------
    dataset: dataframe
        Dataset generated from "import_process_chi_traffic_accident_data" function.

    Return
    ------

    """
    day_pivot = dataset.pivot_table(index='CRASH_DAY_OF_WEEK', columns='fatal_incap', values='CRASH_RECORD_ID',
                                                  fill_value=0, aggfunc='count').reset_index()
    day_pivot.rename({0:'num_not_fatal', 1:'num_fatal'}, axis=1, inplace=True)
    day_pivot['total'] = day_pivot['num_not_fatal'] + day_pivot['num_fatal']
    day_pivot['prcnt_fatal'] = day_pivot['num_fatal'] / day_pivot['total']

    days_of_week=['','Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']

    fig, ax = plt.subplots(figsize=(12,6))
    day_arr = day_pivot['CRASH_DAY_OF_WEEK'].values
    day_prcnt_fatal_arr = day_pivot['prcnt_fatal'].values

    ax.plot(day_arr, day_prcnt_fatal_arr , color='green',  linewidth=3, label='% - Total')
    ax.set_title('Fatal Accidents by Day of the Week', fontsize=26, fontweight='bold')
    ax.set_xlabel('Day of the Week', fontsize=14)
    ax.set_ylabel('% - Total Accidents', fontsize=14)
    ax.set_xticklabels(days_of_week)

    plt.tight_layout()

def plot_accident_results_by_month(dataset):
    """
    Creates a two-axis bar-line chart that summarizes accidents and their results, i.e. fatal or non-fatal, by month.

    Parameters
    ----------
    dataset: dataframe
        Dataset generated from "import_process_chi_traffic_accident_data" function.

    Return
    -------

    """
    month_grpd = dataset.groupby(['CRASH_MONTH', 'fatal_incap']).agg({'fatal_incap':'count'})
    month_grpd.columns = ['count']
    month_grpd.reset_index(inplace=True)
    month_no_fatal_incap = month_grpd[month_grpd['fatal_incap'] == 0]
    month_fatal_incap = month_grpd[month_grpd['fatal_incap'] == 1]

    month_fatal_df = pd.DataFrame()
    month_fatal_df['month'] = pd.Series(range(1,13))
    month_fatal_df['num_not_fatal'] = np.array(month_grpd[month_grpd['fatal_incap'] == 0]['count'])
    month_fatal_df['num_fatal'] = np.array(month_grpd[month_grpd['fatal_incap'] == 1]['count'])
    month_fatal_df['total'] = month_fatal_df['num_not_fatal'] + month_fatal_df['num_fatal']
    month_fatal_df['prcnt_fatal'] = month_fatal_df['num_fatal'] / month_fatal_df['total']

    pos = list(range(len(month_fatal_df['month'])))
    width = 0.4
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, ax1 = plt.subplots(figsize=(14,7))

    ax1.bar(pos, month_fatal_df['num_not_fatal'], width, alpha=0.5, color='b', label='Not Fatal')
    ax1.bar([p + width for p in pos], month_fatal_df['num_fatal'], width, alpha=0.5, color='grey', label='Fatal')
    ax1.set_ylabel('Number of Accidents')
    ax1.set_xticks([p + 0.5 * width for p in pos])
    ax1.set_xticklabels(months)
    ax1.set_title('Traffic Accidents by Month', fontsize=26, fontweight='bold')

    ax1.set_xlim(-0.5, 12)

    ax1.legend(loc='upper left', facecolor='white', fontsize=10)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.grid(color=None, linestyle='None')
    ax1.set_facecolor('white')
    #plt.rcParams['font.family'] = 'garamond'

    # Share x-axis
    ax2=ax1.twinx()

    ax2.set_ylabel('% of Accidents Resulting in Fatalities')
    ax2.set_ylim(0,0.05)
    ax2.plot([p + width/2 for p in pos], month_fatal_df['prcnt_fatal'] , color='orange', linestyle='--', linewidth=3,
             label='% - Fatal')

    ax2.legend(bbox_to_anchor=(0, 0, 0.22, 1.0), facecolor='white', fontsize=10)
    ax2.grid(color=None, linestyle='None')
    plt.tight_layout();
