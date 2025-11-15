import numpy as np
import cv2
from itertools import combinations

def Cercle_CentreEtRayon(P1, P2, P3):
    A, B, C = np.array(P1), np.array(P2), np.array(P3)
    D = 2*(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
    if D == 0:
        return np.array([0,0]), np.inf
    Ux = ((np.sum(A**2)*(B[1]-C[1]) + np.sum(B**2)*(C[1]-A[1]) + np.sum(C**2)*(A[1]-B[1])))/D
    Uy = ((np.sum(A**2)*(C[0]-B[0]) + np.sum(B**2)*(A[0]-C[0]) + np.sum(C**2)*(B[0]-A[0])))/D
    center = np.array([Ux, Uy])
    radius = np.linalg.norm(center - A)
    return center, radius

def cross_product_sign(P, A, B):
    """
    Produit vectoriel (A->B) x (A->P)
    """
    return (B[0]-A[0])*(P[1]-A[1]) - (B[1]-A[1])*(P[0]-A[0])

def intersectionV(P1, P2, triangles, marque):
    """
    Détermine si l'arête P1P2 est valide pour alpha-shape
    P1, P2: points de l'arête
    triangles: liste des triangles contenant cette arête
    marque: 1 si un seul triangle, 2 si deux triangles
    """
    if marque == 1:
        # un seul triangle
        T = triangles[0]
        P3 = [p for p in T if not np.array_equal(p,P1) and not np.array_equal(p,P2)][0]
        C, _ = Cercle_CentreEtRayon(P1,P2,P3)
        cp1 = cross_product_sign(C, P1, P2)
        cp2 = cross_product_sign(P3, P1, P2)
        if (cp1>0 and cp2>0) or (cp1<0 and cp2<0):
            return True
        else:
            return False
    elif marque == 2:
        # deux triangles
        T1, T2 = triangles
        P3 = [p for p in T1 if not np.array_equal(p,P1) and not np.array_equal(p,P2)][0]
        P4 = [p for p in T2 if not np.array_equal(p,P1) and not np.array_equal(p,P2)][0]
        C1, _ = Cercle_CentreEtRayon(P1,P2,P3)
        C2, _ = Cercle_CentreEtRayon(P1,P2,P4)
        cp1 = cross_product_sign(C1, P1, P2)
        cp2 = cross_product_sign(C2, P1, P2)
        if (cp1>0 and cp2>0) or (cp1<0 and cp2<0):
            return False
        else:
            return True
    return False

def alphaMin_Max(P1, P2, P3):
    center, radius = Cercle_CentreEtRayon(P1, P2, P3)
    alpha_min = np.linalg.norm(np.array(P1)-np.array(P2))/2
    alpha_max = radius
    return alpha_min, alpha_max

def alpha_shape_2d(S, alpha):
    """
    Algorithme Alpha-shape 2D
    Entrée:
        S : liste de points [(x,y), ...]
        alpha : rayon
    Sortie:
        arêtes : liste de tuples ((x1,y1),(x2,y2))
    """
    edges = set()
    points = np.array(S)
    n = len(points)
    
    # dictionnaire pour stocker les triangles par arête
    edge_triangles = dict()
    
    for i,j,k in combinations(range(n),3):
        P1,P2,P3 = points[i], points[j], points[k]
        C, radius = Cercle_CentreEtRayon(P1,P2,P3)
        if radius <= alpha:
            for a,b in [(i,j),(j,k),(k,i)]:
                edge = tuple(sorted((a,b)))
                if edge not in edge_triangles:
                    edge_triangles[edge] = []
                edge_triangles[edge].append([P1,P2,P3])
    
    for edge, triangles in edge_triangles.items():
        P1, P2 = points[edge[0]], points[edge[1]]
        marque = 1 if len(triangles)==1 else 2
        if intersectionV(P1,P2,triangles, marque):
            edges.add(edge)
    
    arêtes = [(points[a], points[b]) for a,b in edges]
    return arêtes

def draw_alpha_shape(points, arêtes, width=400, height=400):
    img = np.ones((height, width, 3), dtype=np.uint8)*255
    for p1,p2 in arêtes:
        cv2.line(img, tuple(p1.astype(int)), tuple(p2.astype(int)), (0,0,255), 1)
    for x,y in points:
        cv2.circle(img, (int(x), int(y)), 3, (0,255,0), -1)
    return img

#if __name__ == "__main__":
#    S = [(50,50),(150,80),(120,200),(200,150),(250,50),(300,120)]
#    alpha = 80
#    arêtes = alpha_shape_2d(S, alpha)
#    img = draw_alpha_shape(np.array(S), arêtes)
#    cv2.imshow("Alpha-shape 2D", img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
