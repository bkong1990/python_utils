import glob
import os
import numpy as np
import shutil
import skimage.io
	
def purge_images(input_dir, split, save_dir):
  if not os.path.exists(save_dir+split):
    os.makedirs(save_dir+split)
  crop_img_dir = save_dir+split+'/image/'
  if not os.path.exists(crop_img_dir):
    os.makedirs(crop_img_dir)
  crop_mask_dir = save_dir+split+'/mask/'
  if not os.path.exists(crop_mask_dir):
    os.makedirs(crop_mask_dir)
    
  img_files = glob.glob(input_dir+'mask/*.tif')
  for file_name in img_files:
    mask = skimage.io.imread(file_name)
    if np.sum(mask==255)==mask.shape[0]*mask.shape[1]:
      pass
    else:
      basename = os.path.basename(file_name)
      shutil.copy(input_dir+'image/'+basename, crop_img_dir+basename)      
      shutil.copy(input_dir+'mask/'+basename, crop_mask_dir+basename)
    
if __name__ == '__main__':
  # all the variables need to be changed
  TRAIN_DIR = 'C:/Users/bkong/Desktop/crop_fast/train/'
  TEST_DIR = 'C:/Users/bkong/Desktop/crop_fast/test/'
  SAVE_DIR = 'C:/Users/bkong/Desktop/crop_fast_purged/'
  
  print "Purging training examples..."
  purge_images(TRAIN_DIR,'train',SAVE_DIR)
  print "Purging testing examples..."
  purge_images(TEST_DIR,'test',SAVE_DIR)
  print "Done..."