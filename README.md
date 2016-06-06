# python_utils

# svs_cropping.py
svs_cropping is a GUI util to crop ROIs from .svs files. Since .svs files are mostly huge, you don't want to load them once into the memory. 

How to install?
- This util is based on openslide, so install openslide first.

How to use this util?
- In this util, two windows are initialized. The main window is an overview of the .svs file and the second window is a local view of the image.
- To use this file, change IMG_DIR, SAVE_DIR, Type and selection_size. Also, modify img_ind to change the starting id of your image files. 
