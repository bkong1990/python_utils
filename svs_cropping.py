from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk
import openslide
from PIL import Image
import numpy as np
import glob
from tkMessageBox import *


if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)
    root.geometry("2000x1000")
    root.title("Overview")

    
    #Label(frame_new, text="magnified window").pack()
    
#    frame_new = Toplevel()
#    frame_new.title("Magnified Window")
#    xscroll = Scrollbar(frame_new, orient=HORIZONTAL)
#    xscroll.grid(row=1, column=0, sticky=E+W)
#    yscroll = Scrollbar(frame_new)
#    yscroll.grid(row=0, column=1, sticky=N+S)
#    global canvas_new
#    canvas_new = Canvas(frame_new, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
#    canvas_new.grid(row=0, column=0, sticky=N+S+E+W)
#    xscroll.config(command=canvas_new.xview)
#    yscroll.config(command=canvas_new.yview)
#    #canvas_new.pack(fill=BOTH,expand=1)
#    canvas_new.config(width=1500, height=1000)
#    frame_new.geometry("1500x1000")
    
    top = Toplevel()
    frame_new = Frame(top, bd=2, relief = SUNKEN)
    frame_new.grid_rowconfigure(0, weight=1)
    frame_new.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame_new, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame_new)
    yscroll.grid(row=0, column=1, sticky=N+S)
    global canvas_new
    canvas_new = Canvas(frame_new, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas_new.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas_new.xview)
    yscroll.config(command=canvas_new.yview)
    #canvas_new.pack(fill=BOTH,expand=1)
    canvas_new.config(width=1500, height=1500)
    frame_new.pack(fill=BOTH,expand=1)
    top.geometry("1500x1000")
    top.title("Magnified Window")
    
######################################################################   
    
    # list of the svs files
    IMG_DIR = "G:/TCGA/Squam/"
    SAVE_DIR = "G:/TCGA_crops/Squam/"
    svs_list = glob.glob(IMG_DIR+'*.svs')
    Type = "Squam"
    #svs_list = ['C:/Users/bkong/Desktop/test.svs']   
    global f
    global index
    global crop_indx
    global ind_x
    global ind_y
    global img_ind
    img_ind = 1
    crop_indx = 1
    index = 0
    f = openslide.OpenSlide( svs_list[index] )
    
    
    print "Processing the %dth image" %(index+1)
    # show the overview image in main window
    level_ct = f.level_count
    thumb_size = f.level_dimensions[level_ct-1]
    thumb = f.read_region( (0,0), level_ct-1, thumb_size)
    img = ImageTk.PhotoImage(thumb)
    image_on_canvas = canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    canvas.image=img
    
    
    global selection_size
    selection_size = 2000   # must be even
    # show the corresponding image in the new window
    level0 = f.read_region( (0,0), 0, (selection_size,selection_size) )
    img = ImageTk.PhotoImage(level0)
    global image_on_canvas_new
    image_on_canvas_new = canvas_new.create_image(0,0,image=img,anchor="nw")
    canvas_new.config(scrollregion=canvas_new.bbox(ALL))
    canvas_new.image = img
    
    
    def next_image(canvas,image_on_canvas):
        #File = askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
        #img = ImageTk.PhotoImage(Image.open(File))
        #canvas.itemconfigure(image_on_canvas,image = img)
        #canvas.image=img
        global index
        global f
        global img_ind
        global crop_indx
        crop_indx = 1
        index += 1
        img_ind += 1
        print "Processing the %dth image" %(index+1)
        
        f = openslide.OpenSlide( svs_list[index] )
        level_ct = f.level_count
        thumb_size = f.level_dimensions[level_ct-1]
        thumb = f.read_region( (0,0), level_ct-1, thumb_size)
        img = ImageTk.PhotoImage(thumb)
        canvas.itemconfigure(image_on_canvas,image = img)
        canvas.image=img

    # get corresponding area in the large image and show this area
    def switch_view(event):
        #outputting x and y coords to console
        global f
        global image_on_canvas_new
        global canvas_new
        global selection_size
        global ind_x
        global ind_y
        
        level_ct = f.level_count
        thumb_size = f.level_dimensions[level_ct-1]
        big_img_size = f.level_dimensions[0]
        ratio = float(big_img_size[0])/thumb_size[0]
        canvas = event.widget
        center_x = canvas.canvasx(event.x)
        center_y = canvas.canvasy(event.y)
        #print canvas.find_closest(center_x,center_y)
        ind_x = int(ratio * center_x - selection_size / 2)
        ind_y = int(ratio * center_y - selection_size / 2)
        
        if ind_x < 0 or ind_y < 0 or ind_x + selection_size >= big_img_size[0] or ind_y + selection_size >= big_img_size[1]:
            showerror("Error Location", "Sorry, You shouldn't crop this region!")
        else:
            level0 = f.read_region( (ind_x,ind_y), 0, (selection_size,selection_size) )
            img = ImageTk.PhotoImage(level0)
            canvas_new.itemconfigure(image_on_canvas_new,image = img)
            canvas_new.image = img
        
    def save_crop(event):
        global f
        global selection_size
        global ind_x
        global ind_y
        global crop_indx
        
        level0 = f.read_region( (ind_x,ind_y), 0, (selection_size,selection_size) ) 
        level0.save(SAVE_DIR+Type+"%d_%d.tif"%(img_ind,crop_indx))       
        crop_indx += 1
        
    #mouseclick event
    canvas.bind("<Button 1>",switch_view)
    canvas_new.bind("<Double-Button-1>",save_crop)
    #button.bind("<Button-1>",next_image(1)) 
    
    button = Button(root, text='Next Image', width=25, command=lambda: next_image(canvas,image_on_canvas))  
    button.pack(side = RIGHT) 

    root.mainloop()