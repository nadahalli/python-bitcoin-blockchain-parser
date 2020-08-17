from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
from sklearn.metrics import precision_score, recall_score

dataset = read_csv('./t.csv', delimiter = ';', usecols = lambda column : column in ["created_block" , "value", "fanin", "fanout", "fanout_share", "total_value", "label"])

array = dataset.values

#X = preprocessing.scale(array[:,0:6])
X = array[:,0:6]

for row in X:
    print(row)
    break

Y = array[:,6]
for row in Y:
    print(row)
    break

X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=0.20, random_state=1)

model = LogisticRegression(solver='liblinear')
model.fit(X_train, Y_train)

Y_predict = model.predict(X_validation)

print('Precision: {0:0.2f}'.format(
      precision_score(Y_validation, Y_predict, average = 'micro')))
print('Recall: {0:0.2f}'.format(
      recall_score(Y_validation, Y_predict, average = 'micro')))



