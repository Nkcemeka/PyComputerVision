import sys
from PIL import Image
import numpy as np


def gray_conv(img_array, matrix_multiply):
    """
        This function converts a colored image to
        a grayscale image
    """

    # Change each RGB value to a Y value by doing a matrix multiplication
    image_gray_array= np.matmul(img_array, matrix_multiply.T)[:,:,0] #The index 0, which is the last index selects the y values
    image_conv = image_gray_array.astype(np.uint8) # convert the grayscale image array to an 8 bit integer to scale between 0 and 255
    image_gray = Image.fromarray(image_conv) # Produce the grayscale image from the grayscale image array
    return image_gray

def main():
    """
        Converts an image to a grayscale image and performs
        histogram equalization.
    """

    if len(sys.argv)!=5:
        print("usage is: %s first_input_image second_input_img \
            first_output_img second_output_img"%(sys.argv[0]))
        sys.exit()
    
    # Importation of the first and second image
    image_color1 = Image.open(sys.argv[1]) # Import the first colored image
    image_color2 = Image.open(sys.argv[2]) # Import the second colored image

    # Conversion of the first and second image into an array
    image_array1 = np.asarray(image_color1, np.float64) # Convert the first colored image into an array
    image_array2 = np.asarray(image_color2, np.float64) # Convert the second colored image into an array
    matrix_multiply = np.array([[.299, .587, .114],
    [-.14713, -.28886, .436], [.615, -.51499, -.10001]]) # matrix used to convert RGB to YUV
    grayscale_img1 = gray_conv(image_array1, matrix_multiply) # convert first colored image to a grayscale image
    grayscale_img2 = gray_conv(image_array2, matrix_multiply) # convert first colored image to a grayscale image

    # Saving of the images into image files
    grayscale_img1.save(sys.argv[3])
    grayscale_img2.save(sys.argv[4])

    # Showing the images for the user to see
    grayscale_img1.show() # show the first grayscale image
    grayscale_img2.show() # show the second grayscale image



main()