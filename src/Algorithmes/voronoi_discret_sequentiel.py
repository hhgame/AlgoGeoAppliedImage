import numpy as np
import cv2

def voronoi_discret_sequentiel(points, width, height):
    """
    Calcul séquentiel du diagramme de Voronoi discret.
    Utilisation de numpy pour accélérer par vecteur.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)
    colors = np.array([np.random.randint(0, 255, 3) for _ in points])

    yy, xx = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    for i, (px, py) in enumerate(points):
        if i == 0:
            dist = np.hypot(xx - px, yy - py)[..., None]
            min_dist = dist
            nearest = np.full((height, width), i)
        else:
            dist = np.hypot(xx - px, yy - py)
            mask = dist < min_dist[..., 0]
            nearest[mask] = i
            min_dist[mask] = dist[mask, None]

    for i, color in enumerate(colors):
        img[nearest == i] = color

    return img

#if __name__ == "__main__":
#    points = [(50, 50), (150, 100), (100, 200)]
 #   img = voronoi_discret_sequentiel(points, 300, 300)
  #  cv2.imshow("Voronoi Séquentiel", img)
   # cv2.waitKey(0)
    #cv2.destroyAllWindows()
