import cv2
import numpy as np
from PIL import Image
from PIL import Image, ImageChops 
# Read an image
# img = cv2.imread('path_to_your_image.jpg')

# Check if the image has been successfully loaded
flash_image = cv2.imread ("E:\INTERNSHIP\flash.jpg")
nonflash_image = cv2.imread ("E:\INTERNSHIP\nonflash.jpg") 
diff_flash = flash_image - nonflash_image
bilateralFilter_flash_image = cv2.bilateralFilter(flash_image, 15, 0.4, 16)
bilateralFilter_nonflash_image = cv2.bilateralFilter(nonflash_image, 15, 0.4, 16)
BLdiff_flash = bilateralFilter_flash_image - bilateralFilter_nonflash_image
# Display the image
#cv2.imshow('Image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

 
  
# Apply bilateral filter with d = 15,  
# sigmaColor = sigmaSpace = 75. 

  
# Save the output. 
cv2.imwrite("Nonbilateraldiffimg.png",diff_flash) 
cv2.imwrite("bilateraldiffimg.png",BLdiff_flash) 

diff = diff_flash - BLdiff_flash
cv2.imwrite("diff.png",diff)