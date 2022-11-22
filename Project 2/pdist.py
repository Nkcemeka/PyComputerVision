import sys
from PIL import Image
import numpy as np

def swap_coord(coord):
    """
        Swap the coordinates of the
        matrix.
    """
    coord_new = []
    for i in coord:
        new_coord = i[::-1]
        coord_new.append(new_coord)
    return coord_new

def dict_coord(coord):
    """
        Returns all the needed coordinates in a dictionary
        
        coord0: contains (c1,d1) and is 1st item in the list
        coord1: contains (c2,d2) and is 2nd item in the list
        coord2: contains (c3,d3) and is 3rd item in the list
        coord3: contains (c4,d4) and is 4th item in the list
    """

    (a1, b1) = coord[0]
    (a2, b2) = coord[1]
    (a3, b3) = (coord[2][0], b1)
    (a4, b4) = (coord[3][0], b2) 

    coord_persp = dict()
    coord_persp['1'] = [(a1,b1), coord[0]]
    coord_persp['2'] = [(a2,b2), coord[1]]
    coord_persp['3'] = [(a3,b3), coord[2]]
    coord_persp['4'] = [(a4,b4), coord[3]]

    return coord_persp

def dict_coord2(coord):
    """
        Returns all the needed coordinates in a dictionary
        for the second image
        
        coord0: contains (c1,d1) and is 1st item in the list
        coord1: contains (c2,d2) and is 2nd item in the list
        coord2: contains (c3,d3) and is 3rd item in the list
        coord3: contains (c4,d4) and is 4th item in the list
    """

    # Randomly chosen points
    # (a1, b1) = (730, 498)
    # (a2, b2) = (730,739)
    # (a3, b3) = (576, 498)
    # (a4, b4) = (576, 739)

    (a1, b1) = (691, 591)
    (a2, b2) = (691,613)
    (a3, b3) = (547, 591)
    (a4, b4) = (547, 613)

    # (a1, b1) = (691, 591)
    # (a2, b2) = (691,610)
    # (a3, b3) = (547, 591)
    # (a4, b4) = (547, 610)

    coord_persp = dict()
    coord_persp['1'] = [(a1,b1), coord[0]]
    coord_persp['2'] = [(a2,b2), coord[1]]
    coord_persp['3'] = [(a3,b3), coord[2]]
    coord_persp['4'] = [(a4,b4), coord[3]]

    return coord_persp

def mat_h(coord_persp):
    """
        Generates the matrix needed to 
        evaluate H
    """
    mat_h = []
    for i in list(coord_persp.keys()):
        i_num = int(i)
        (a,b) = coord_persp[i][0]
        (c,d) = coord_persp[i][1]
        mat_h.append([c, d, 1, 0, 0, 0, -a*c, -a*d])
        mat_h.append([0, 0, 0, c, d, 1,-b*c, -b*d])
    return np.array(mat_h)

def point_h(coord_persp):
    """
        Generates list of chosen points
        in processed image to get H.
    """
    point_h = []
    for i in list(coord_persp.keys()):
        point_h.append(coord_persp[i][0][0])
        point_h.append(coord_persp[i][0][1])
    return np.array(point_h)

def proc_pos(img_array):
    """
        Transforming the perspective of
        the image.
    """
    rows = img_array.shape[0]
    cols = img_array.shape[1]

    position_coord = []

    for row in range(rows):
        for col in range(cols):
            position_coord.append((row,col,1))
    
    return np.array(position_coord)

def persp_proc(img_arr, dist_pos, dist_img):
    """
        Generates the processed image
        img_array: initilaized processed image array
        dist_pos: coordinates of distorted image
        dist_img: distorted image
    """

    rows = img_arr.shape[0]
    cols = img_arr.shape[1]

    for row in range(rows):
        for col in range(cols):
            pos_a = dist_pos[row][col][0]
            pos_b = dist_pos[row][col][1]
            if (pos_a>=rows or pos_a<0) or (pos_b>=cols or pos_b <0):
                continue
            else:
                img_arr[row][col] = dist_img[pos_a][pos_b]
               
    
    img = img_arr.astype(np.uint8)
    img = Image.fromarray(img)
    return img



def correct_persp(img, coord2=False):
    """
        Function to fix perspective distortion
    """ 
    img_array = np.asarray(img, np.float64) # convert image to an array

    # Extraction of rows and columns of distorted image
    dist_rows = img_array.shape[0] # number of rows in distorted image
    dist_cols = img_array.shape[1] # number of cols in distorted image
    hmat = np.zeros(8) # column vector of h matrix with length 8

    # Assigning coordinates of points to use
    #coord = [(7,799),(576,799),(236,239),(337,239)]
    #coord = [(47,620),(595,615),(177,348),(429,348)]
    #coord = [(8,800), (577,800), (237, 240),(339,240)] image 1


    if coord2:
        #coord = [(562,659), (743,756), (566, 525),(745,573)] # image 2
        coord = [(663,714), (742,758), (667,552), (745,573)]
        coord = swap_coord(coord)
        coord_persp = dict_coord2(coord)
    else:
        # Run image 1 instead
        #coord = [(8,800), (577,800), (237, 240),(339,240)]  # image 1
        #coord = [(47,619),(595,614),(229,240),(362,240)]
        coord = [(229,240),(362,240),(47,619),(595,614)]
        coord = swap_coord(coord)
        coord_persp = dict_coord(coord)

    # calculation of h matrix
    h_point = point_h(coord_persp) # list of points to get h
    
    inv_8 = np.linalg.inv(mat_h(coord_persp)) #inverse of 8*8 matrix to get h
    hmat = np.matmul(inv_8, h_point) # generating h as a column vector

    hmat = np.append(hmat, 1).reshape((3,3)) # adding 1 to h matrix and reshaping


    # Getting coordinates of points in distorted image
    h_inv = np.linalg.inv(hmat) # calculation of hinv
    proc_position  = proc_pos(img_array) # Getting all the positions in processed image

    # Getting coordinates in dist. image
    dist_pos = np.matmul(h_inv, proc_position.T) 
    dist_pos = dist_pos.T 

    # dividing by 3rd coordinate to turn coords. back to homogenous coordinate with 1 at the end
    dist_pos = dist_pos/(dist_pos[:,2].reshape((dist_pos.shape[0],1)))
    dist_pos = np.rint(dist_pos[:,:-1]) #rounding the values to nearest integer
    dist_pos = dist_pos.reshape(dist_rows,dist_cols,2) # reshaping to a more suitable form
    dist_pos = dist_pos.astype(int)

    #processed image
    proc_imgarray = img_array.copy()
    proc_imgarray.fill(0) # making the processed image black

    # Generating Corrected Perspective Image
    proc_img = persp_proc(proc_imgarray, dist_pos, img_array)
    proc_img.show()
    return proc_img


def main():
    """
        Corrects the perspective for
        two images.
    """
    if len(sys.argv)!=5:
        print("usage is: %s first_input_image second_input_img \
            first_output_img second_output_img"%(sys.argv[0]))
        sys.exit()
    
    # Importation of colored images
    img1 = Image.open(sys.argv[1])
    img2 = Image.open(sys.argv[2])

    # Correcting Perspective
    correct_img1 = correct_persp(img1)
    correct_img2 = correct_persp(img2, coord2=True) # To use coord2 coordinates

    # Save Corrected images
    correct_img1.save(sys.argv[3])
    correct_img2.save(sys.argv[4])



    
main()