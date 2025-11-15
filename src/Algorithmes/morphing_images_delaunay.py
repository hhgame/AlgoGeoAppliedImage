import numpy as np
import cv2
from delaunay_triangulation import delaunay_triangulation, draw_delaunay

def affine_transform(src, src_tri, dst_tri, size):
    """
    Transforme un triangle src_tri vers dst_tri
    """
    src_tri = np.float32(src_tri)
    dst_tri = np.float32(dst_tri)
    warp_mat = cv2.getAffineTransform(src_tri, dst_tri)
    dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
    return dst

def morph_images(img1, img2, alpha=0.5, n_points=50):
    h, w = img1.shape[:2]
    # points aléatoires pour Delaunay
    points = [(np.random.randint(0,w), np.random.randint(0,h)) for _ in range(n_points)]
    triangles = delaunay_triangulation(points)
    
    morphed = np.zeros_like(img1)
    
    for tri in triangles:
        pts1 = [points[i] for i in tri]
        pts2 = [(int(x*(1-alpha) + x*alpha), int(y*(1-alpha)+y*alpha)) for x,y in pts1]
        # calcul de la bounding box
        r = cv2.boundingRect(np.array(pts2, dtype=np.int32))
        size = (r[2], r[3])
        dst = affine_transform(img1, pts1, pts2, size)
        morphed[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = dst
    return morphed

#if __name__ == "__main__":
#    img1 = cv2.imread("images/input1.jpg")
#    img2 = cv2.imread("images/input2.jpg")
#    morphed = morph_images(img1, img2, alpha=0.5)
#    cv2.imshow("Morphing", morphed)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
