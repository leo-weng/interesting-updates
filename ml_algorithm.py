import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC, LinearSVC
from sklearn import svm, linear_model
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

def get_sql_data():
    # input_file = open('allsubreddits.txt','r')
    # output_file = open('testquery.txt','w')

    connection = sqlite3.connect("data.db")
    # cursor
    crsr = connection.cursor()

    sql = """
            SELECT num_clicked, total_time
            FROM (
                SELECT s.id, s.url, COUNT(c.clicked_URL) AS num_clicked,
                    SUM(c.time_passed) AS total_time
                FROM (SELECT * FROM Clicks LIMIT 1000000) AS c
                LEFT JOIN Subreddits AS s
                ON c.clicked_URL = s.id
                WHERE c.clicked_URL <= 1082444
                GROUP BY s.id
            );
        """

    total_clicked = []
    total_times = []
    for row in crsr.execute(sql):
        total_clicked.append(row[0])
        total_times.append(row[1])

    d = {'total_times': total_times, 'total_clicked': total_clicked}
    df = pd.DataFrame(data=d)
    # for i in range(len(total_clicked)):
    #     output_file.write(total_clicked[i] + " " + total_times[i] + "\n")
    return df


def run_regression_model(dataset):
    # print (dataset.head())
    # print(dataset.describe())
    # dataset.plot(style='o')
    # plt.show()

    X = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, 1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    # regressor = LinearRegression()
    # regressor.fit(X_train, y_train)
    # print(regressor.intercept_)
    # print(regressor.coef_)
    # y_pred = regressor.predict(X_test)
    # df = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
    # print(df)
    # print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
    # print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
    # print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    for i in range(len(y_pred)):
        print(y_pred[i], y_test[i])
    # feature_imp = pd.Series(clf.feature_importances_).sort_values(ascending=False)
    # print(feature_imp)
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))


if __name__ == '__main__':
    df = get_sql_data()
    run_regression_model(df)
