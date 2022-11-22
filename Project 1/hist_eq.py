import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def histogram(img_array_gray):
    """
        Computes the histogram of a grayscale image
    """
    hist_array = np.empty(256) # creates memory for histogram of image array
    for i in range(256):
        count = (img_array_gray == i).sum() # counts number of pixel intensity i
        hist_array[i] = count # stores number of pixel intensity i in hist_array
    return hist_array

def plot_hist(hist_array, hist_name = 'hist_img.png'):
    """
        Plots an histogram array for visualization
        hist_name: Optional argument which serves as the name of the saved histogram plot
    """
    plt.bar(range(256), hist_array, align='edge', width=1.0) # plots histogram array for visualization purposes
    plt.xlabel("Pixel Intensities")
    plt.ylabel("Frequency of Pixel Intensities")
    plt.title("Graph Plot of Frequency Distribution against Pixel Intensity")
    # Saving of Histograms to Output Files
    plt.savefig(hist_name)
    plt.show()
    

def hist_eq(p, hist_array, img_array):
    """
        Histogram equalizes a grayscale image array.
        p: parameter needed for equalization
        hist_array: histogram of grayscale image to be equalized
        img_array: grayscale image array
    """
    table_intensity = np.zeros(256) # Creating an intensity table to map input intensities to output intensities
    t = p # setting t to p to using incomputing histogram eq
    curr_sum = 0 # temporary sum of number of pixels processed
    out_val = 1 # initial output intensity

    # Mapping of input to output intensities
    for i in range(1,255):
        curr_sum += hist_array[i]
        if curr_sum >= t:
            out_val = round(curr_sum/p) # new output value
            t = out_val*p
            table_intensity[i] = out_val
        else:
            table_intensity[i] = out_val
        
    
    img_arr_out = np.full(img_array.shape,-1) # output array filled with -1, which will contain the histogram equalized array

    # Histogram equalizing the image
    for i in range(1,255):
        indices = np.where(img_array==i) # Extracting location where the pixel is equals to i
        index_rows = indices[0]
        index_cols = indices[1]

        for index_row, index_col in zip(index_rows, index_cols):
            if img_arr_out[index_row][index_col] == -1: # This means if the pixel position there has not been changed, change it
                img_arr_out[index_row][index_col] = table_intensity[i]
    
    eq_img_arr = img_arr_out.astype(np.uint8) # histogram equalized image array converted to an 8 bit integer
    return eq_img_arr

def main():
    """
        Performing histogram equalization
        on imported images.
    """

    if len(sys.argv)!=5:
        print("usage is: %s first_input_image second_input_img \
            first_output_img second_output_img"%(sys.argv[0]))
        sys.exit()

    # Image importation and conversion
    img_clr1 = Image.open(sys.argv[1]) # Opens first color image
    img_clr2 = Image.open(sys.argv[2]) # Opens second color image

    # Grayscale Image Conversion
    img_gray1 = img_clr1.convert('L') # Converts first color image to grayscale image
    img_gray2 = img_clr2.convert('L') # Converts second color image to grayscale image

    # Image to Array Conversion
    img_array_gray1 = np.asarray(img_gray1, np.float64) # converts first gray scale image to an array
    img_array_gray2 = np.asarray(img_gray2, np.float64) # converts first gray scale image to an array

    # Visualization of Original Grayscale Image before Histogram Eq
    img_gray1.show() # initial image of the first grayscale image before equalization
    img_gray2.show() # initial image of the second grayscale image before equalization

    # Saving of Original Grayscale Images
    img_gray1.save('img_gray1.jpg')
    img_gray2.save('img_gray2.jpg')

    # Original Image Histogram
    hist_array1 = histogram(img_array_gray1) # Histogram of first grayscale image
    plot_hist(hist_array1, hist_name='low-contrast-hist-original.png') # Plot histogram of frist grayscale image to see image histogram

    hist_array2 = histogram(img_array_gray2) # Histogram of second grayscale image
    plot_hist(hist_array2, hist_name='prof-Barry-hist-original.png') # Plot histogram of second grayscale image to see image histogram

    # Getting of parameters for histogram EQ
    sum_range1 = hist_array1[1:255].sum() # number of pixels with intensities in the range 1 to 254 for first grayscale image
    p1 = sum_range1/254 # ideal number of pixels for each intensity level for first grayscale image

    sum_range2 = hist_array2[1:255].sum() # number of pixels with intensities in the range 1 to 254 for second grayscale image
    p2 = sum_range2/254 # ideal number of pixels for each intensity level for second grayscale image

    # Computation of Histogram EQ
    eq_img_arr1 = hist_eq(p1, hist_array1, img_array_gray1) # Histogram equalization of first grayscale image
    eq_img_arr2 = hist_eq(p2, hist_array2, img_array_gray2) # Histogram equalization of second grayscale image

    # Visualization of Histogram Equalized Image
    eq_img1 = Image.fromarray(eq_img_arr1) # Image generation of equalized grayscale image for the first image
    eq_img1.show()

    eq_img2 = Image.fromarray(eq_img_arr2) # Image generation of equalized grayscale image for the second image
    eq_img2.show()

    # Histogram Visualization of Histogram Equalized Image
    hist_histeq1 = histogram(eq_img_arr1) # Image generation of equalized grayscale histogram for the first image
    plot_hist(hist_histeq1, hist_name='low-contrast-hist.png')

    hist_histeq2 = histogram(eq_img_arr2) # Image generation of equalized grayscale histogram for the second image
    plot_hist(hist_histeq2, hist_name='prof-Barry-hist.png')

    # Saving of Equalized Images to Output Files
    eq_img1.save(sys.argv[3])
    eq_img2.save(sys.argv[4])
    

main()



