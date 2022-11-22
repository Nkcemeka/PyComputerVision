import sys
from PIL import Image
import numpy as np

def file_reader():
    pic1_list = []
    pic3_list = []
    pic4_list = []
    with open("pic1.dat", 'r') as pic1, open("pic3.dat") as pic3,\
    open("pic4.dat") as pic4:
        for line in pic1:
            (a,b,c) = line.split(' ')
            #(a,b,c) = (b,a,c)
            pic1_list.append((eval(a), eval(b), eval(c)))
        for line in pic3:
            (a,b,c) = line.split(' ')
            #(a,b,c) = (b,a,c)
            pic3_list.append((eval(a), eval(b), eval(c)))
        for line in pic4:
            (a,b,c) = line.split(' ')
            #(a,b,c) = (b,a,c)
            pic4_list.append((eval(a), eval(b), eval(c)))
    return (pic1_list, pic3_list, pic4_list)



def camera_coord_gen(b, coords, right = False):
    """
        b: distance between camera coords
        coords: an array of (x,y,z) in world coordinates
        right: if true, it is a right camera
    """
    if right:
        coords_conv = coords[:,0] - (b/2)
        coords_conv = coords_conv.reshape((coords_conv.shape[0],1))
        coords_conv = np.hstack((coords_conv, coords[:,1:]))
    else:
        coords_conv = coords[:,0] + (b/2)
        coords_conv = coords_conv.reshape((coords_conv.shape[0],1))
        coords_conv = np.hstack((coords_conv, coords[:,1:]))
    
    return coords_conv

def world_pics(f, w_pix, w_cm, h_pix, h_cm, coords):
    w_mm = w_cm * 10 # width conv from cm to mm
    h_mm = h_cm *10 # height conv from cm to mm
    n1 = w_pix/w_mm # pixels per mm along x1 axis
    n2 = h_pix/h_mm # pixels per mm along x2 axis

    c1 = w_pix/2 - 1 # coordinates of principal point in pixels along x1 axis
    c2 = h_pix/2 - 1 # coordinates of pricnipal point in pixels along x2 axis


    # Matrix to convert world coordinate to PICS
    mat_pics = np.array([[n1*f, 0, c1, 0],
                         [0, n2*f, c2, 0],
                         [0, 0, 1, 0]])

    # Conversion to PICS
    world_point = np.hstack((coords, np.ones((coords.shape[0],1))))
    pics_coord = np.matmul(world_point, mat_pics.T) # round as pixels are integers not floats
    pics_coord = pics_coord/pics_coord[:,2].reshape((coords.shape[0],1))
    pics_coord = pics_coord.astype(int)
    pics_coord = pics_coord[:,:2] # selection of x and y columns
    pics_coord = np.flip(pics_coord, 1) # reversal of x and y columns for python use
    return pics_coord # y comes first and x comes second

def imag_proj(img_size, pics, b, f, w_pix, w_cm, h_pix, h_cm):
    img_l = np.zeros((img_size[1], img_size[0], 3))
    img_r = np.zeros((img_size[1], img_size[0], 3))
    pic1 = np.array(pics[0])
    pic3 = np.array(pics[1])
    pic4 = np.array(pics[2])

    # Projection on Left Image
    pic1_pix_left = camera_coord_gen(b, pic1)
    pic1_pics_coord_l = world_pics(f, w_pix, w_cm, h_pix, h_cm, pic1_pix_left)
    pic3_pix_left = camera_coord_gen(b, pic3)
    pic3_pics_coord_l = world_pics(f, w_pix, w_cm, h_pix, h_cm, pic3_pix_left)
    #print(pic3_pics_coord)
    pic4_pix_left = camera_coord_gen(b, pic4)
    pic4_pics_coord_l = world_pics(f, w_pix, w_cm, h_pix, h_cm, pic4_pix_left)

    # Projection on Right Image
    pic1_pix_right = camera_coord_gen(b, pic1, right=True)
    pic1_pics_coord_r = world_pics(f, w_pix, w_cm, h_pix, h_cm, pic1_pix_right)
    pic3_pix_right = camera_coord_gen(b, pic3, right=True)
    pic3_pics_coord_r = world_pics(f, w_pix, w_cm, h_pix, h_cm, pic3_pix_right)
    pic4_pix_right = camera_coord_gen(b, pic4, right=True)
    pic4_pics_coord_r = world_pics(f, w_pix, w_cm, h_pix, h_cm, pic4_pix_right)

    # Left Image showing
    #img[pic1_pics_coord][1] = 255 #np.array([0,255,0])
    for i in pic1_pics_coord_l:
        #print(i)
        if (i[0] < 512) & (i[1] < 1024) & np.all(i>=0):
            img_l[tuple(i)][1] = 255 # green
            #print("y")
    for i in pic4_pics_coord_l:
        if (i[0] < 512) & (i[1] < 1024) & np.all(i>=0):
            img_l[tuple(i)][2] = 255 # blue
            #print("y")
    for i in pic3_pics_coord_l:
        if (i[0] < 512) & (i[1] < 1024) & np.all(i>=0):
            img_l[tuple(i)][0] =255 #np.array([255,0,0]) # red
            #print("y")
    #img[pic3_pics_coord] = np.array([255,0,0])
    #img[pic4_pics_coord][2] = 255 #np.array([0,0,255])
    img_l = img_l.astype(np.uint8)
    img_pic_l = Image.fromarray(img_l)
    img_pic_l.show()

    # Right Image showing
    for i in pic1_pics_coord_r:
        if (i[0] < 512) & (i[1] < 1024) & np.all(i>0):
            img_r[tuple(i)][1] = 255 # green
    for i in pic4_pics_coord_r:
        if (i[0] < 512) & (i[1] < 1024) & np.all(i > 0):
            img_r[tuple(i)][2] = 255 # blue
    for i in pic3_pics_coord_r:
        if (i[0] < 512) & (i[1] < 1024) & np.all(i > 0):
            img_r[tuple(i)][0] =255 # red
    img_r = img_r.astype(np.uint8)
    img_pic_r = Image.fromarray(img_r)
    img_pic_r.show()

def main():
    # baseline denotes the distance between the 
    # center of projections of both cameras.
    b = 6.5*10 # baseline is 6.5cm or 65mm
    f = 3.5*10 # focal length is 3.5cm or 35mm
    w_pix = 1024 # width is 1024 pixels
    w_cm = 5 # width is 5cm/50mm
    h_cm = 2.5 # width is 2.5cm/25mm
    h_pix = 512 # height is 512 px
    img_size = (w_pix, h_pix) # This has not been reversed
    pics = file_reader()
    imag_proj(img_size, pics, b, f, w_pix, w_cm, h_pix, h_cm)
    #imag_proj(img_size, pics, b, f, h_pix, h_cm, w_pix, w_cm)



main()