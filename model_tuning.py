from sklearn.model_selection import LeaveOneOut
from sklearn.ensemble import RandomForestClassifier

def random_forest_loo(n_estimators, X, Y):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    
    loo = LeaveOneOut()
    rf = RandomForestClassifier(n_estimators=n_estimators)


    for train, test in loo.split(X, y=Y):
        X_train = X[train, :]
        X_test = X[test, :]

        Y_train = Y[train]
        Y_test = Y[test][0]

        rf.fit(X_train, Y_train)
        Y_pred = rf.predict(X_test)[0]

        if Y_test == 1 and Y_pred == 1:
            tp += 1
        elif Y_test == 0 and Y_pred == 0:
            tn += 1
        elif Y_test == 1 and Y_pred == 0:
            fn += 1
        elif Y_test == 0 and Y_pred == 1:
            fp += 1
            
    accuracy = (tp + tn) / (tp + tn + fn + fp)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 1 / ((1/precision) + (1/recall))
    
    return accuracy, precision, recall, f1