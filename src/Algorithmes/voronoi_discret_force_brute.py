import numpy as np
import cv2

def voronoi_discret_force_brute(points, width, height):
    """
    Calcul du diagramme de Voronoi discret par force brute.
    
    Args:
        points (list of tuples): Liste de points (x, y)
        width (int): largeur de l'image
        height (int): hauteur de l'image
        
    Returns:
        np.ndarray: Image de Voronoi
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)
    colors = [tuple(np.random.randint(0, 255, 3).tolist()) for _ in points]

    for y in range(height):
        for x in range(width):
            distances = [np.hypot(x - px, y - py) for (px, py) in points]
            idx = np.argmin(distances)
            img[y, x] = colors[idx]

    return img

#if __name__ == "__main__":
 #   points = [(50, 50), (150, 100), (100, 200)]
  #  img = voronoi_discret_force_brute(points, 300, 300)
   # cv2.imshow("Voronoi Force Brute", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
