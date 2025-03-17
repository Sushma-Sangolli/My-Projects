import cv2
import numpy as np
from PIL import Image
from PIL import Image, ImageChops 

import cv2

flash_image = cv2.imread(r'E:\INTERNSHIP\sushma\flash.jpg')
nonflash_image = cv2.imread(r'E:\INTERNSHIP\sushma\nonflash.jpg')

if flash_image is None or nonflash_image is None:
    print("Error: One or both images could not be read.")
else:
    # Proceed with further processing
    diff_flash = flash_image - nonflash_image

#diff_flash = flash_image - nonflash_image

bilateralFilter_flash_image = cv2.bilateralFilter(flash_image, 15, 0.4, 16)
bilateralFilter_nonflash_image = cv2.bilateralFilter(nonflash_image, 15, 0.4, 16)
BLdiff_flash = bilateralFilter_flash_image - bilateralFilter_nonflash_image
  
cv2.imwrite(r'E:\INTERNSHIP\Nonbilateraldiffimg.png', diff_flash)
cv2.imwrite(r'E:\INTERNSHIP\Bilateraldiffimg.png', BLdiff_flash)
cv2.imwrite(r'E:\INTERNSHIP\sushma\flash.jpg', flash_image)
cv2.imwrite(r'E:\INTERNSHIP\sushma\nonflash.jpg', nonflash_image)


    # Display the images
cv2.imshow('Non flash image Bilateral Mask', diff_flash)
cv2.imshow('Bilateral mask Image', BLdiff_flash)
cv2.imshow('with flash image',flash_image)
cv2.imshow('without flash image',nonflash_image)
    # Wait for a key press and then close all windows
diff = diff_flash - BLdiff_flash
cv2.imwrite('diff.png',diff)
cv2.imshow('Difference Image', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()