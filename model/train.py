import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

df = pd.read_csv("weather_data.csv")
df.drop(columns="max_temp",inplace=True)
X = df.drop(columns="class")
y = df["class"]

clf1 = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
clf1.fit(X,y)

pickle.dump(clf1,open('model.pickle','wb'))

