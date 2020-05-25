# Protecting Chicago's Streets

![VisionZero](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/VisionZero_Horizontal_.png)

## Table of Contents

1) Executive Summary
2) VisionZero
3) Data Processing and Feature Engineering
4) Exploratory Data Analysis
5) Model Evaluation and Selection
6) Further Investigation

## Executive Summary
According to the Center of Disease Control (CDC), more than 1.3 million lives were lost on roadways throughout the world in 2019. This number equates to 3,700 daily deaths, which is nearly the same number of people who died in Chernobyl. One Chernobyl, sans radioactive waste, occurs every day.

How can city officials and local governments improve the safety of pedestrians, cyclists, and drivers?

By constructing a model that can predict whether a traffic accident results in a fatality/severe injury or no/minimum injury, I hope to identify areas that provide the greatest opportunity for safety enhancement.

The selected model achieved a recall equal to 0.76 and an AUC score of 0.81. In comparison, the preliminary baseline models resulted in recall scores ranging from 0.58 to 0.62.

I based the models’ merits on recall because the dataset was imbalanced and minimizing false negative was integral to an informative model. In this analysis, a false negative signifies incorrectly predicting no one is severely harmed/killed when, in fact, the crash resulted in incapacitation/fatality. Therefore, a type II error is significantly more problematic than a type I error.

## VisionZero
In 2017, then mayor Rahm Emanuel inaugurated Vision Zero Chicago with the goal of eliminating all traffic fatalities and severe injuries by 2026. To do so, city officials and organizations are implementing policies, investing in technologies, and modifying Chicago's landscape.

The basic logic of Vision Zero is that any traffic collision that results in death or serious injury is not an unavoidable “accident,” but a tragedy that could be prevented through smarter engineering, education, and enforcement. It is inspired by a successful road safety program enacted in Sweden over 20 years ago.

Many major U.S. metropolitan areas - e.g. New York, Los Angeles, and Austin - have adopted the program.

## Data Processing and Feature Engineering
The data source is the Chicago Police Department's (CPD) electronic crash reporting system (E-Crash) at CPD; it excludes any personally identifiable information, e.g. vehicle make and model. The accidents occurred from September 1, 2017 to February 29, 2020. The dataset is comprised of more than 290,000 crashes.

Most of the crash parameters - including street condition data, primary cause, and weather condition - are recorded by the reporting officer based on the best available information at the time of the incident.
The dataset is imbalanced, less than 2.0% of the accidents resulted in a fatality or severe injury. (Hopefully, the datasets imbalance increases overtime.) I applied under sampling to resolve it because the computation costs to evaluate/train various models and different sets of features was high.

I recognize that one of undersampling’s setback is information loss. To understand the magnitude of the risk, early on, I executed a couple variations of Logistic Regression and XGBoost applying over- and under-sampling. The different in results were negligible.

As mentioned, the bulk of the features are categorical. Also, many of the features had more than 20 possible values. By applying one-hot encoding, exploring the data, and reviewing the results of many variation of each model, I narrowed in on the most informative feature.

Being mindful of ensemble method’s feature importance limitations, I obtain significant use from it as an exploratory approach in identifying which independent variables provided the greatest information gain in compared to other in their “model cohort”. Combining this process and exploratory data analysis is what the led to the significant increase in recall.

## Exploratory Data Analysis

I analyzed if a car’s speed, which in this dataset is assumed as the posted speed limit, examining the bar chart below, we see an increasing trend in the percentage of total accidents that resulted in a fatality/severe injury as the posted speed limit increases.

![Speed Limit](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/fatal_speed_lim.png)

Additionally, I reviewed the relationship between time of day and results of the accident. In total, more accidents occur during the day; meanwhile, the percentage of accidents that are fatal is greater at night and early morning. However, one should not conclude that nights/early mornings are more dangerous as many more accidents have happened during the day. Hypothesis testing is required to determine if there is statistical different in the likelihood of an accident being fatal differs during the hours of sunlight and moonlight.

![Hourly Accidents](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/hourly_trend.png)

I also investigated whether there were reoccurring traits at scenes of fatal accidents. The absence of a traffic control device – e.g. traffic light, cross walk and stop sign - regularly appeared as one of the most important features when I applied the ensemble models. Nearly 50% of fatal accidents occurred in an area where there was no traffic device. Like the “time-of-day” analysis, hypothesis testing is required to accurately assess whether a lack of a traffic device control impacts the outcome of a crash.

I also noticed frequent references to parameters associated with intersections, e.g. traffic signal and failure to yield at a right-of-way. I researched the subject on the internet. According to the American Association of State Highway and Transportation Officials (AASHTO), which develops the Highway Safety Manual, roundabouts reduces accidents where people are severely harmed or killed by 78 to 82% when compared to conventional intersections that have stop signs or traffic signals.

![Device Controls](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/device_control_dis.png)
![Primary Cause](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/primary_cause.png)

## Model Evaluation and Selection

Once I identified/engineered the optimal independent variables, I used RandomizedSearchCV to optimize and compare four models: 1) Gradient Bost; 2) Logistic Regression; 3) Random Forest; and 4) XGBoost.

As previously discussed, recall was the primary metric used to assess model performance. Gradient Boost marginally outperformed XGBoost with scores of XXX and XXX, respectively. Gradient Boost produced XXX less false negative than XGBoost.

![Confusion Matrix](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/gdbt_confusion_matrix.png)

The optimal model acquired the most information from features claim what was the initial point of contact, e.g. pedestrian and parked vehicle. Intuitively, the logic is reasonable. If the initial contact was a parked car, then the likelihood of a non-lethal accident is high. On the other hand, if a vehicle’s first contact is a pedestrian, the probability of a life-threatening injury is great.

Except for time of day and the posted speed limit, the 15 most informative features are one-hot encoded.

![Feature Importance](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/gbdt_feat_import.png)

The difference in performance among gradient boost, logistic regression and XGBoost was minimal. The ROC curve demonstrates that the similar performance among three of the four models. Gradient boost and XGBoost achieved equal AUC scores of 0.813.

![ROC Curve](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/roc_curve.png)

## Conclusion / Further Exploration

Based on the analysis, I believe two areas that Chicago’s government should explore, if not already, to achieve the city’s goal of eradicating accidents resulting in fatality/severe injuries are intersections and pedestrian/bicycle safety control

Chicago could look across the pond to Europe. Barcelona’s superblocks have been lauded for enhancing pedestrian safety and city’s world-renown street culture. 

Regarding cyclists’ protection, bike-friendly cities, like Copenhagen, have redesigned the street. Bikes lanes are protected from the traffic by parked cars. Also, the lanes are slightly elevated. If a car enters a bike lane, the bump is expected to reduce the vehicle’s velocity. The picture below is from Copenhagen.

![Copenhagen](https://github.com/Morgan-Sell/Chicago-Traffic-Risk/blob/master/images/copenhagen_bike_lane.jpeg)
