# -*- coding: utf-8 -*-
"""Proyecto_M5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OI31K2O99_PJxgtEjCeVMZz8pRjRc4BF

#Churn Prediction

##Módulo 5: Caso Práctico individual
###Alumno: 131044

![churn](http://chaotic-flow.com/wp-content/uploads/2017/09/saas-churn-leaky-bucket.png)

Este proyecto corresponde al módulo de Data Science del Master en Big Data Management. Por lo tanto, **el objetivo es el siguiente:** Poder predecir quien va a causar baja como cliente de una Telco en función de sus servicios contratados, tiempo en la compañía, facturación y tipos de contratos. 

Los datos a utilizar proceden de Kaggle (https://www.kaggle.com/blastchar/telco-customer-churn) y contienen información sobre clientes, productos y servicios contratados, información contractual, información método de pago y facturación, información permanencia clientes e información abandono de clientes.

La predicción se llevará a cabo estudiando previamente el dataset mediante un análisis exploratorio y la posterior elección del algoritmo ás adecuado para la solución del problema.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import re
from google.colab import files
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

"""##  ACCESO A LOS DATOS

se han cargado en google collaboratory por lo que simplemente llamándolos con  la función read_csv() de pandas ya los tendríamos accesibles
"""

#uploaded = files.upload()

churn_raw = pd.read_csv("churn.csv",sep=";",decimal=".")
churn_raw.head()

"""Después de un primer vistazo de los datos, revisamos si hay valores nulos y por tanto si requiere una limpieza el dataset"""

churn_raw.info()   #dtypes

"""Ya que la función is.na() de R, detecta tanto los valores nulos como las celdas vacías, se ha decidido hacer una doble comprobación en R, ya que este tipo de valores caussarán errores en los siguientes pasos del proyecto.

**Input:** dataset %>% summarise_all(funs(sum(is.na(.))))

**output:**
TotalCharges = 11
Resto de Variables = 0

R detecta 11 NAs en la columna "TotalCharges" mientras que en Python no existe ningún valor nulo en esta viariable. Por  lo tanto,  pordríamos asumir que esos NAs corresponden a celdas vacías. En este caso, esos 11 clientes son nuevos y no tienen ninguna cuota pagada,ya que ternure para esos valores es 0 por lo tanto tendría sentido que estén vacíos aun, pero para que no nos de errores en los siguientes pasos se le asigna el valor 0.
"""

#churn_raw.TotalCharges = pd.to_numeric(churn_raw.TotalCharges, errors='coerce')
#churn_raw.info()

churn_raw.describe(percentiles=[0.2,0.4,0.6,0.8], include=['object','float','int'])

churn_raw = churn_raw.set_index('customerID')

churn_num = churn_raw[['SeniorCitizen', 'tenure', 'MonthlyCharges','TotalCharges']].copy()
churn_num.head()
columns = ['gender','Partner','Dependents','PhoneService','MultipleLines','InternetService','OnlineSecurity',
           'OnlineBackup','DeviceProtection','TechSupport','StreamingTV','StreamingMovies','Contract',
           'PaperlessBilling','PaymentMethod','Churn']
churn_categorical = churn_raw[columns].copy()
churn_categorical.head()

df = pd.get_dummies(data=churn_categorical, sparse=False, columns=columns)
churn_cat = df.drop(['gender_Male','Partner_No','Dependents_No','PhoneService_No','PaperlessBilling_No','Churn_No','MultipleLines_No',
                    'MultipleLines_No phone service','OnlineSecurity_No internet service','OnlineBackup_No internet service',
                     'DeviceProtection_No internet service','TechSupport_No internet service','StreamingTV_No internet service',
                     'StreamingMovies_No internet service','OnlineSecurity_No','OnlineBackup_No','DeviceProtection_No','TechSupport_No',
                     'StreamingTV_No','StreamingMovies_No'], axis =1)

churn_cat.head()

churn_num.hist(figsize=[10,10])

churn_cat.hist(figsize=[15,10])

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8),(ax9,ax10,ax11,ax12),(ax13,ax14,ax15,ax16)) = plt.subplots(4,4, figsize=(20,35))  # 1 row, 2 columns

churn_categorical.gender.value_counts().plot(kind='bar',title='Gender', ax=ax1)
churn_categorical.Partner.value_counts().plot(kind='bar',title='Partner', ax=ax2)
churn_categorical.Dependents.value_counts().plot(kind='bar',title='Dependents', ax=ax3)
churn_categorical.PhoneService.value_counts().plot(kind='bar',title='PhoneService', ax=ax4)
churn_categorical.MultipleLines.value_counts().plot(kind='bar',title='MultipleLines', ax=ax5)
churn_categorical.InternetService.value_counts().plot(kind='bar',title='InternetService', ax=ax6)
churn_categorical.OnlineSecurity.value_counts().plot(kind='bar',title='OnlineSecurity', ax=ax7)
churn_categorical.OnlineBackup.value_counts().plot(kind='bar',title='OnlineBackup', ax=ax8)
churn_categorical.DeviceProtection.value_counts().plot(kind='bar',title='DeviceProtection', ax=ax9)
churn_categorical.TechSupport.value_counts().plot(kind='bar',title='TechSupport', ax=ax10)
churn_categorical.StreamingTV.value_counts().plot(kind='bar',title='StreamingTV', ax=ax11)
churn_categorical.StreamingMovies.value_counts().plot(kind='bar',title='StreamingMovies', ax=ax12)
churn_categorical.Contract.value_counts().plot(kind='bar',title='Contract', ax=ax13)
churn_categorical.PaperlessBilling.value_counts().plot(kind='bar',title='PaperlessBilling', ax=ax14)
churn_categorical.PaymentMethod.value_counts().plot(kind='bar',title='PaymentMethod', ax=ax15)
churn_categorical.Churn.value_counts().plot(kind='bar',title='Churn', ax=ax16)


plt

df = churn_raw.groupby(['gender','Churn']).mean().reset_index().pivot(index='Churn',columns='gender',values='TotalCharges')
df.plot(kind='bar', title='Total charges vs Churn')

df = churn_raw.groupby(['SeniorCitizen','Churn']).mean().reset_index().pivot(index='Churn',columns='SeniorCitizen',values='TotalCharges')
df.plot(kind='bar', title='Total charges vs Churn')

df = churn_raw.groupby(['gender','Churn']).mean().reset_index().pivot(index='Churn',columns='gender',values='tenure')
df.plot(kind='bar', title='tenure vs Churn')

df = churn_raw.groupby(['SeniorCitizen','Churn']).mean().reset_index().pivot(index='Churn',columns='SeniorCitizen',values='tenure')
df.plot(kind='bar', title='Tenure vs Churn')

churn = churn_num.join(churn_cat)
#churn.head()

# %matplotlib inline

# calculate the correlation matrix
corr = churn.corr()

# plot the heatmap

plt.figure(figsize = (16,10))

ax = sns.heatmap(corr, xticklabels=corr.columns,yticklabels=corr.columns, linewidths=.2)

plt

# %matplotlib inline
# calculate the correlation matrix
corr = churn_num.drop(['SeniorCitizen'], axis=1).corr()

# plot the heatmap
plt.figure(figsize = (10,6))

ax = sns.heatmap(corr, xticklabels=corr.columns,yticklabels=corr.columns)

plt

"""**[MACHINE LEARNING](https://)**"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from scipy.spatial import ConvexHull

labels = np.array(churn['Churn_Yes'])
dffeatures = churn.drop('Churn_Yes',axis=1)
feature_list = list(churn.columns)
features =np.array(dffeatures)
dffeatures.head()

#random forest
  
#@title Random Forest Implementation
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.3, random_state = 42)
rf = RandomForestClassifier(n_estimators = 20, random_state = 42)
rf.fit(train_features, train_labels);
predictions = rf.predict(test_features)

print("Train Accuracy :: " + str(accuracy_score(train_labels, rf.predict(train_features))))
print("Test Accuracy  :: " + str(accuracy_score(test_labels, predictions)))

#Feature importance

featureImportance = pd.concat([pd.Series(feature_list), pd.Series(rf.feature_importances_)],axis=1)
featureImportance

#Random Forest reducing variables
labels_reduced = np.array(churn['Churn_Yes'])
dffeatures = churn[['tenure', 'MonthlyCharges','TotalCharges','InternetService_Fiber optic','gender_Female',
                    'Contract_Two year','Contract_One year']].copy()
feature_list_reduced = list(churn.columns)
features_reduced =np.array(dffeatures)
dffeatures.head()

#
train_features, test_features, train_labels, test_labels = train_test_split(features_reduced, labels_reduced, test_size = 0.3, random_state = 42)
rf = RandomForestClassifier(n_estimators = 15, random_state = 42)
rf.fit(train_features, train_labels);
predictions = rf.predict(test_features)

print("Train Accuracy :: " + str(accuracy_score(train_labels, rf.predict(train_features))))
print("Test Accuracy  :: " + str(accuracy_score(test_labels, predictions)))

#logistic regresion
lr = LogisticRegression(random_state = 42)
lr.fit(train_features, train_labels);
predictions = lr.predict(test_features)

print("Train Accuracy :: " + str(accuracy_score(train_labels, lr.predict(train_features))))
print("Test Accuracy  :: " + str(accuracy_score(test_labels, predictions)))

#@title Grid Search and Cross-Validation
param_grid = {
    'bootstrap': [True],
    'max_depth': [50, 60, 80],
    'max_features': [3,4,5,6,7],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [3, 5, 10, 100]
}
rf = RandomForestClassifier(random_state = 42)
# Instantiate the grid search model
grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, cv = 5, n_jobs = -1, verbose = 2)
grid_search.fit(train_features, train_labels)
grid_search.best_params_

#title Model Accuracy Metrics
best_grid = grid_search.best_estimator_
predictions = best_grid.predict(test_features)

print("Train Accuracy :: " + str(accuracy_score(train_labels, best_grid.predict(train_features))))
print("Test Accuracy  :: " + str(accuracy_score(test_labels, predictions)))

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve

probs = best_grid.predict_proba(test_features)

fpr, tpr, threshold = roc_curve(test_labels, probs[:,1])
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()

#@title Making Prediction Over Entire Dataset

dfEvaluate = churn[['tenure', 'MonthlyCharges','TotalCharges','InternetService_Fiber optic','gender_Female',
                    'Contract_Two year','Contract_One year']].copy()
#churn.copy()

evalFeatures = dfEvaluate #.drop('Churn_Yes', axis = 1)

eature_list_eval = list(evalFeatures.columns)
evalFeatures = np.array(evalFeatures)

#Make Predictions
evalPredictions = best_grid.predict(evalFeatures)
evalPredictions = best_grid.predict(evalFeatures)
dfEvaluate['PredictedChurn'] = evalPredictions

dfchurn = churn[['Churn_Yes']].copy()
df = dfEvaluate.join(dfchurn)
df.head()

check = df.drop(['tenure', 'MonthlyCharges','TotalCharges','InternetService_Fiber optic','gender_Female',
                    'Contract_Two year','Contract_One year'],axis = 1)
check.head()
check['result'] = np.where(df['PredictedChurn'] == df['Churn_Yes'], 'Correct', 'InCorrect')
check['True_positive'] = np.where((df['PredictedChurn'] == 1) & (df['Churn_Yes'] ==1), 1, 0)
check['False_positive'] = np.where((df['PredictedChurn'] == 1) & (df['Churn_Yes'] ==0), 1, 0)
check['True_negative'] = np.where((df['PredictedChurn'] == 0) & (df['Churn_Yes'] ==0), 1, 0)
check['False_negative'] = np.where((df['PredictedChurn'] == 0) & (df['Churn_Yes'] ==1), 1, 0)
print('True positives =', (check.True_positive.sum()/7043).round(4))
print('False positives =',(check.False_positive.sum()/7043).round(4))
print('True negatives =',(check.True_negative.sum()/7043).round(4))
print('False negatives =',(check.False_negative.sum()/7043).round(4))

dfprecision = check.groupby(['result']).agg({'result': 'count'})
dfprecision

dfprecision['result'][0]/(dfprecision['result'][0]+dfprecision['result'][1]) * 100