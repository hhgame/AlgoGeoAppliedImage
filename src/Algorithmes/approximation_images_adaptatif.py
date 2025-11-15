import numpy as np
import cv2

def approximation_image_adaptatif(image_path, n_points):
    """
    Approximation adaptative : points plus denses sur zones détaillées
    """
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    
    # probabilité proportionnelle à l'intensité des bords
    prob = edges.flatten().astype(float)
    if np.sum(prob) == 0:
        prob += 1  # éviter division par zéro
    prob /= np.sum(prob)
    indices = np.random.choice(h*w, n_points, p=prob)
    points = [(i%w, i//w) for i in indices]
    
    # Voronoi adaptatif
    img_voronoi = np.zeros_like(img)
    for y in range(h):
        for x in range(w):
            distances = [np.hypot(x-px, y-py) for px, py in points]
            idx = np.argmin(distances)
            img_voronoi[y,x] = img[points[idx][1], points[idx][0]]
    return img_voronoi

#if __name__ == "__main__":
#    img_v = approximation_image_adaptatif("images/input.jpg", 300)
#    cv2.imshow("Approximation Adaptative", img_v)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
