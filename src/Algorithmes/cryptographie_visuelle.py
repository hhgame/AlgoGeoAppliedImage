import numpy as np
import cv2

def split_image(image_path):
    """
    Cryptographie visuelle simple : split image en deux shares
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    share1 = np.random.randint(0, 2, (h, w), dtype=np.uint8) * 255
    share2 = img ^ share1
    return share1, share2

def combine_shares(share1, share2):
    return share1 ^ share2

#if __name__ == "__main__":
#    share1, share2 = split_image("images/input.jpg")
#    combined = combine_shares(share1, share2)
#    cv2.imshow("Share 1", share1)
#    cv2.imshow("Share 2", share2)
#    cv2.imshow("Combined", combined)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
