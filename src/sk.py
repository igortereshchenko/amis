import numpy as np
from sklearn.svm import SVC
from random import randint, random


def get_dataset():
    views_list = []
    comments_list = []
    likes_list = []

    scores_list = []

    for _ in range(10000):
        views = randint(0, 50)
        comments = randint(0, 50)
        likes = randint(0, 50)

        if any(criterion > 10 for criterion in [views, comments, likes]):
            score_range = np.random.choice(4, 1, p=[0.05, 0.2, 0.4, 0.35])[0]
        elif comments > 15:
            score_range = np.random.choice(4, 1, p=[0.05, 0.15, 0.5, 0.3])[0]
        elif views > 40:
            score_range = np.random.choice(4, 1, p=[0.05, 0.15, 0.4, 0.4])[0]
        elif likes > 25:
            score_range = np.random.choice(4, 1, p=[0.05, 0.15, 0.6, 0.2])[0]
        elif views + comments + likes > 10:
            score_range = np.random.choice(4, 1, p=[0, 0.3, 0.4, 0.3])[0]
        else:
            score_range = np.random.choice(4, 1, p=[0, 0.5, 0.35, 0.15])[0]

        if score_range == 0:
            score = randint(0, 25)
        elif score_range == 1:
            score = randint(26, 50)
        elif score_range == 2:
            score = randint(51, 75)
        elif score_range == 3:
            score = randint(76, 100)

        views_list.append(views)
        comments_list.append(comments)
        likes_list.append(likes)

        scores_list.append(score)

    inputs = []
    outputs = []
    for v, c, l, s in zip(
        views_list, comments_list, likes_list, scores_list
    ):
        inputs.append([v, c, l])
        outputs.append(s)

    return inputs, outputs


X, y = get_dataset()


clf = SVC(gamma='auto')
clf.fit(X, y)
SVC(gamma='auto')
print(clf.predict([[50, 50, 50]]))
