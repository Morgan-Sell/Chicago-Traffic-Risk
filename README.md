# Improving Chicago's Streets

![VisionZero]

## Table of Contents

1) Executive Summary
2) VisionZero
3) Data
4) Exploratory Data Analysis
5) Model Evaluation and Selection
6) Further Investigation

## Executive Summary
Accoding to the Center of Disease Control (CDC), more than 1.3 million deaths occured on roadways throughout the world in 2019. This number equates to 3,700 daily deaths, which is nearly the same number of people who died in Chernobyl. One Chernobyl, sans radioactive waste, occurs every day.

How can city officials improve the safety of pedestrians, cyclists, and drivers?

By constructing a model that can predict whether a traffic accident results in a fatality/severe injury or no/minmum injury, I hope to identify areas provide the greatest opportunity for safety enhancement.

The selected model achieved a recall equal to 0.76 and an AUC score of 0.81. In comparison, the recall scores of the baselines models ranged from 0.58 to 0.62.

I focused on recall because the dataset was imbalanced and minimizing false negative was integral to an informative model. In this analysis, a false negative singifies incorrectly predicting no one is severely harmed/killed when, in fact, the crash resulted in incapacitation/fatality. 

## VisionZero
In 2017, then mayor Rahm Emanual inauguruated Vision Zero Chicago with the goal of eliminating all traffic fatalities and severe injuries by 2026. To do so, city officials and organizations are implementing policies, investing in technologies, and modifying Chicago's landscape.

The basic logic of Vision Zero is that any traffic collision that results in death or serious injury is not an unavoidable “accident,” but a tragedy that could be prevented through smarter engineering, education, and enforcement. It is inspired by a successful road saftey program enacted in Sweden over 20 years ago.

Many major U.S. metropolitan areas - e.g. New York, Los Angeles, and Austin - have adopted the program.

## Data Processing and Feature Engineering
The data source is the Chicago Police Department's (CPD) electronic crash reporting system (E-Crash) at CPD. It excludes any personally identifiable information, like vehicle make and model. The accidents occured from September 1, 2017 to February 29, 2020. The dataset is comprised of more than 290,000 crashes. 

Most of the crash parameters, including street condition data, primary cause, and weather condition, are recorded by the reporting officer based on the best available information at the time of the incident.

The dataset was imbalanced, less than 2.0% of the accidents resulted in a fatality or severe injury. I applied undersampling to resolve it. Using simple baseline models, I examined the magnitude of information loss comparing by comparing preliminary results from both under- and over-sampled datasets. The models using oversamplig performed marginally better; however, to execute the model was both computationally and time expensive, concluding undersampling was more than sufficient.

The majority of the independent variables were categorical. Examples included the initial point of the crash, the traffical control device and its condition, and day of the week. 

The modeling was an interative proceess derived of one-hot encoding and analyzing feature importance of various ensemble models. My initial  




## Exploratory Data AnalysisI



## Model Evaluation and Selection

## Further Investigation