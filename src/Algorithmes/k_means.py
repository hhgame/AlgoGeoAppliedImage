import numpy as np

def k_means(points, k, max_iter=100):
    """
    Algorithme K-means classique
    points: np.array (n,2)
    k: nombre de clusters
    """
    n = len(points)
    indices = np.random.choice(n, k, replace=False)
    centers = points[indices]
    for _ in range(max_iter):
        # assignation
        clusters = [[] for _ in range(k)]
        for p in points:
            dists = np.linalg.norm(centers - p, axis=1)
            clusters[np.argmin(dists)].append(p)
        # mise à jour
        new_centers = np.array([np.mean(c, axis=0) if len(c)>0 else centers[i] for i,c in enumerate(clusters)])
        if np.allclose(centers, new_centers):
            break
        centers = new_centers
    return centers, clusters

#if __name__ == "__main__":
#    pts = np.random.rand(100,2)*100
#    centers, clusters = k_means(pts, 3)
#    print("Centres:", centers)
