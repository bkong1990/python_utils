# python_utils

# svs_cropping.py
svs_cropping is a GUI util to crop ROIs from .svs files. Since .svs files are mostly huge, you don't want to load them once into the memory. 

How to install?
- This util is based on openslide, so install openslide first.

How to use this util?
- In this util, two windows are initialized. The main window is an overview of the .svs file and the second window is a local view of the image.
- To use this file, change IMG_DIR, SAVE_DIR, Type and selection_size. Also, modify img_ind to change the starting id of your image files. 

# generate_fast_examples.py
generate_fast_examples.py is a util to generate training & validation examples for efficient patch convolutional neural networks

How to use this util?
change the following variables:
- TRAIN_DIR
- TEST_DIR
- SAVE_DIR
- train_split
- test_split
- CROP_SIZE
- IMG_SIZE
- pos_neighbor
- neg_neighbor

# purge_fast_examples.py
This util is for efficient cnn. After generating the training examples, some of the images don't contain any desired label (all pixels are 255), which is purged out by this util.

How to use?
change the following directory:
- TRAIN_DIR 
- TEST_DIR 
- SAVE_DIR

# weighted_selection.py
Sometimes, we need to selected items from a list associated with weights
