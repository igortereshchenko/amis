import pandas as pd
import matplotlib.pyplot as plt


df = pd.DataFrame({
    'x': [12, 20, 28, 18, 29, 33, 24, 45, 45, 52, 51, 52, 55, 53, 55, 61, 64, 69, 72],
    'y': [39, 36, 30, 52, 54, 46, 55, 59, 63, 70, 66, 63, 58, 23, 14, 8, 19, 7, 24]
})
colmap = {1: 'r', 2: 'g', 3: 'b'}

from sklearn.cluster import KMeans

print(df)
kmeans = KMeans(n_clusters=3)
kmeans.fit(df)

print(df)

labels = kmeans.predict(df)
print(labels)
centroids = kmeans.cluster_centers_
print(centroids)

fig = plt.figure(figsize=(5, 5))

colors = list(map(lambda x: colmap[x+1], labels))

plt.scatter(df['x'], df['y'], color=colors, alpha=0.5, edgecolor='k')

for idx, centroid in enumerate(centroids):
    print(idx)
    plt.scatter(*centroid, color=colmap[idx+1])
plt.xlim(0, 80)
plt.ylim(0, 80)
plt.show()