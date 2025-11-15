import numpy as np
from k_means import k_means

def k_means_plus_plus(points, k, max_iter=100):
    """
    Initialisation K-means++ + K-means
    """
    n = len(points)
    centers = []
    centers.append(points[np.random.randint(n)])
    
    for _ in range(1, k):
        dist_sq = np.array([min([np.linalg.norm(p-c)**2 for c in centers]) for p in points])
        prob = dist_sq / np.sum(dist_sq)
        cumulative_prob = np.cumsum(prob)
        r = np.random.rand()
        for i, cp in enumerate(cumulative_prob):
            if r < cp:
                centers.append(points[i])
                break
    centers = np.array(centers)
    
    # Continue avec K-means
    return k_means(points, k, max_iter)

#if __name__ == "__main__":
#    pts = np.random.rand(100,2)*100
#    centers, clusters = k_means_plus_plus(pts, 3)
#    print("Centres:", centers)
