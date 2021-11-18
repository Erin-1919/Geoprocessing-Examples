import os
os.chdir(r'G:\UCalgary Research\NRCan_NationalDEM\Experiment_DEM_Oct\NRCan_python_Oct\Result\vege_img_25')

import cv2
im1_s = cv2.imread('vege_img_25_1.png')

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

#im1_s = cv2.resize(im1, dsize=(0, 0), fx=0.5, fy=0.5)
im_tile = concat_tile([[im1_s, im1_s, im1_s, im1_s],
                       [im1_s, im1_s, im1_s, im1_s],
                       [im1_s, im1_s, im1_s, im1_s]])
cv2.imwrite('test.png', im_tile)
