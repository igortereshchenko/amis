from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from neural_network_model.db.connection import conn


def clustering_axes():
    cursor = conn.cursor()

    cursor.execute(
        'select question_text from orm_question;'
    )
    data = [r[0] for r in cursor.fetchall()]

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data)
    true_k = 3
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    model.predict(X)
    pca = PCA(n_components=3, random_state=0)
    reduced_features = pca.fit_transform(X.toarray())
    reduced_cluster_centers = pca.transform(model.cluster_centers_)

    return reduced_features[:, 0], reduced_features[:, 1], reduced_features[:, 2]


# clustering_axes()