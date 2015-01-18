import numpy as np
from images2gif import writeGif
from PIL import Image
import os

def draw_circle(center,r,data):
    #r is in pixels/index units
    #if the centerpoint of a given pixel is fewer than "r" pixels from the
    #centerpoint of the circle, color that pixel
    l,w,d=np.shape(data)
    r2=r*r
    x_max=1+int(center[0]+r)
    y_max=1+int(center[1]+r)
    x=int(center[0]-r)
    while x < x_max:
        if x >= 0 and x < l:
            y=int(center[1]-r)
            while y < y_max:
                if y >= 0 and y < w:
                    if float(x-center[0])**2 + float(y-center[1])**2 < r2:
                        data[x,y]=[255,255,255]
                y+=1
        x+=1
    return data

def make_gif():
    radius=1
    image_filenames=[]
    image_list=[]
    plotsize=800
    data = np.zeros( (plotsize,plotsize,3), dtype=np.uint8)
    file = open('coordinates_output','r')
    counter=0    
    print( "starting visualization")
    for line in file.readlines():
        data = np.zeros( (plotsize,plotsize,3), dtype=np.uint8)
        array=line.split();
        coordinates=[]
        r=[]
        i=0
        while i < len(array):
            r.append(float(array[i]))
            coordinates.append( [ float(array[i+1]), float(array[i+2]) ])
            i+=3
        n=len(coordinates)
        i=0
        while i < n:
            center = coordinates[i]
            data = draw_circle([center[0]*plotsize,center[1]*plotsize],r[i]*radius,data)
            i+=1
        #img = Image.fromarray(data, 'RGB')
        image_list.append(Image.fromarray(data, 'RGB'))
        #image_filenames.append('image'+str(counter)+'.png')
        #img.save('image'+str(counter)+'.png')
        counter+=1
    file.close()
    

    writeGif('galaxy.gif', image_list, duration=0.05)
    for fn in image_filenames:
        os.remove(fn)


