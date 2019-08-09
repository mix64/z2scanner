#!/usr/bin/env python3

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

train = pd.read_json('train.json')
test = pd.read_json('test.json')

tree = DecisionTreeClassifier(max_depth=15, random_state=0)
tree.fit(train.drop(['MD5', 'MAL'], axis=1), train['MAL'])
predict = tree.predict(test.drop(['MD5', 'MAL'], axis=1))
tp, fn, fp, tn = confusion_matrix(predict, test['MAL']).ravel()

print("Accuracy(train)    : %1.3f" % tree.score(
    train.drop(['MD5', 'MAL'], axis=1), train['MAL']))
print("Accuracy(test)     : %1.3f" % ((tp+tn)/(tp+fp+tn+fn)))
print("True Positive Rate : %1.3f" % (tp/(tp+fn)))
print("False Negative Rate: %1.3f" % (fn/(tp+fn)))
print("False Positive Rate: %1.3f" % (fp/(fp+tn)))
print("False Negative Rate: %1.3f" % (tn/(fp+tn)))
print("Precision          : %1.3f" % (tp/(tp+fp)))
print("\tPos_p\tNeg_p\nPos_t\t%5d\t%5d\nNeg_t\t%5d\t%5d" % (tp, fn, fp, tn))

for label, score in zip(train.drop(['MD5', 'MAL'], axis=1), tree.feature_importances_):
    print("%s : %1.3f" % (label, score))

"""
# Save
from joblib import dump, load
dump(tree, 'tree.joblib')
newtree = load('tree.joblib')

# Show 
from sklearn.tree import export_graphviz
import pydot
export_graphviz(tree, out_file="tree.dot")
(graph,) = pydot.graph_from_dot_file('tree.dot')
graph.write_png('tree.png')
"""
