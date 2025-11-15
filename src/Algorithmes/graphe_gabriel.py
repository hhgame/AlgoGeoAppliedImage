import numpy as np
import cv2
from itertools import combinations

def point_in_disk(P, A, B):
    """
    Vérifie si le point P est à l'intérieur du disque de diamètre AB
    """
    center = (A + B) / 2
    radius = np.linalg.norm(A - B) / 2
    return np.linalg.norm(P - center) < radius

def graphe_gabriel(S):
    """
    Construction du Graphe de Gabriel (GG)
    Entrée:
        S: liste de points [(x,y), ...]
    Sortie:
        edges: liste d'arêtes [(p1,p2), ...]
    """
    points = np.array(S)
    n = len(points)
    edges = []
    
    for i,j in combinations(range(n),2):
        A, B = points[i], points[j]
        keep = True
        for k in range(n):
            if k == i or k == j:
                continue
            P = points[k]
            if point_in_disk(P, A, B):
                keep = False
                break
        if keep:
            edges.append((A,B))
    return edges

def draw_graphe_gabriel(points, edges, width=400, height=400):
    """
    Affichage du Graphe de Gabriel
    """
    img = np.ones((height, width,3), dtype=np.uint8)*255
    for p1,p2 in edges:
        cv2.line(img, tuple(p1.astype(int)), tuple(p2.astype(int)), (0,0,255), 1)
    for x,y in points:
        cv2.circle(img, (int(x), int(y)), 3, (0,255,0), -1)
    return img

#if __name__ == "__main__":
#    S = [(50,50),(150,80),(120,200),(200,150),(250,50),(300,120)]
#    edges = graphe_gabriel(S)
#    img = draw_graphe_gabriel(np.array(S), edges)
#    cv2.imshow("Graphe de Gabriel", img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
