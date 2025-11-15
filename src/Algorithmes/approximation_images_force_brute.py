import numpy as np
import cv2
from voronoi_discret_force_brute import voronoi_discret_force_brute

def approximation_image_force_brute(image_path, n_points):
    """
    Approximation d'image par diagramme de Voronoi (force brute)
    Args:
        image_path: chemin de l'image
        n_points: nombre de points générateurs
    Returns:
        img_voronoi: image approximée
    """
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    points = [(np.random.randint(0,w), np.random.randint(0,h)) for _ in range(n_points)]
    
    # Calcul du Voronoi
    img_voronoi = np.zeros_like(img)
    for y in range(h):
        for x in range(w):
            distances = [np.hypot(x-px, y-py) for px, py in points]
            idx = np.argmin(distances)
            img_voronoi[y,x] = img[points[idx][1], points[idx][0]]
    return img_voronoi

#if __name__ == "__main__":
#    img_v = approximation_image_force_brute("images/input.jpg", 200)
#    cv2.imshow("Approximation Force Brute", img_v)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
