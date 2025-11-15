import numpy as np
import cv2

def circumcircle(triangle):
    """
    Calcul du centre et rayon du cercle circonscrit à un triangle
    triangle: array de shape (3,2)
    """
    A, B, C = triangle
    D = 2*(A[0]*(B[1]-C[1]) + B[0]*(C[1]-A[1]) + C[0]*(A[1]-B[1]))
    if D == 0:
        return (0,0), np.inf
    Ux = ((np.sum(A**2)*(B[1]-C[1]) + np.sum(B**2)*(C[1]-A[1]) + np.sum(C**2)*(A[1]-B[1])))/D
    Uy = ((np.sum(A**2)*(C[0]-B[0]) + np.sum(B**2)*(A[0]-C[0]) + np.sum(C**2)*(B[0]-A[0])))/D
    center = np.array([Ux, Uy])
    radius = np.linalg.norm(center - A)
    return center, radius

def delaunay_triangulation(points):
    """
    Triangulation de Delaunay par force brute
    points: liste de tuples (x,y)
    Retour: liste de triangles (3 indices)
    """
    points = np.array(points)
    n = len(points)
    triangles = []

    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                tri = points[[i,j,k]]
                center, radius = circumcircle(tri)
                # Vérifie qu'aucun autre point n'est à l'intérieur
                inside = False
                for l in range(n):
                    if l in [i,j,k]:
                        continue
                    if np.linalg.norm(points[l] - center) < radius:
                        inside = True
                        break
                if not inside:
                    triangles.append((i,j,k))
    return triangles

def draw_delaunay(points, triangles, width=400, height=400):
    img = np.ones((height, width, 3), dtype=np.uint8)*255
    points = np.array(points)
    for tri in triangles:
        pts = points[list(tri)].astype(np.int32)
        cv2.polylines(img, [pts], isClosed=True, color=(0,0,255), thickness=1)
    for x,y in points:
        cv2.circle(img, (int(x), int(y)), 3, (0,255,0), -1)
    return img

#if __name__ == "__main__":
#    pts = [(50, 50), (150, 100), (100, 200), (200, 50), (250, 150)]
#    tris = delaunay_triangulation(pts)
 #   img = draw_delaunay(pts, tris)
  #  cv2.imshow("Delaunay maison", img)
   # cv2.waitKey(0)
    #cv2.destroyAllWindows()
