import numpy as np
import cv2
from multiprocessing import Pool

def assign_pixel(args):
    x, y, points = args
    distances = [np.hypot(x - px, y - py) for px, py in points]
    return np.argmin(distances)

def voronoi_discret_parallele(points, width, height):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    colors = [tuple(np.random.randint(0, 255, 3).tolist()) for _ in points]

    coords = [(x, y, points) for y in range(height) for x in range(width)]
    with Pool() as pool:
        nearest_flat = pool.map(assign_pixel, coords)

    nearest = np.array(nearest_flat).reshape((height, width))
    for i, color in enumerate(colors):
        img[nearest == i] = color

    return img

#if __name__ == "__main__":
#    points = [(50, 50), (150, 100), (100, 200)]
 #   img = voronoi_discret_parallele(points, 300, 300)
  #  cv2.imshow("Voronoi Parallèle", img)
   # cv2.waitKey(0)
    #cv2.destroyAllWindows()
