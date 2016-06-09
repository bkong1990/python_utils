import glob
import os
import numpy as np
import skimage.io
import warnings

# CROP_HEIGHT and CROP_WIDTH should be odd number
def pad_image(img, CROP_WIDTH, CROP_HEIGHT):
  IMG_HEIGHT = img.shape[0]
  IMG_WIDTH = img.shape[1]

  padded_img = np.zeros((IMG_HEIGHT+CROP_HEIGHT-1, IMG_WIDTH+CROP_WIDTH-1,3)).astype(np.uint8)
  padded_img[CROP_HEIGHT/2:IMG_HEIGHT+CROP_HEIGHT/2,CROP_WIDTH/2:IMG_WIDTH+CROP_WIDTH/2,:] = img    # fill the middle
  padded_img[CROP_HEIGHT/2:IMG_HEIGHT+CROP_HEIGHT/2,0:CROP_WIDTH/2,:] = img[:,CROP_WIDTH/2:0:-1,:]  # pad the left
  padded_img[CROP_HEIGHT/2:IMG_HEIGHT+CROP_HEIGHT/2,IMG_WIDTH+CROP_WIDTH/2:IMG_WIDTH+CROP_WIDTH,:] = img[:,IMG_WIDTH-2:IMG_WIDTH-CROP_WIDTH/2-2:-1,:]    # pad the right
  padded_img[:CROP_HEIGHT/2,:,:] = padded_img[CROP_HEIGHT-1:CROP_HEIGHT/2:-1,:,:]    # pad the top
  padded_img[IMG_HEIGHT+CROP_HEIGHT/2:IMG_HEIGHT+CROP_HEIGHT,:,:] = padded_img[IMG_HEIGHT+CROP_HEIGHT/2-2:IMG_HEIGHT-2:-1,:,:]    # pad the bottom

  return padded_img


def generate_crops(file_names,split,filename,CROP_SIZE,IMG_SIZE,pos_neighbor,neg_neighbor,save_dir):
  # make the corresponding directories
  if not os.path.exists(save_dir+split):
    os.makedirs(save_dir+split)
  crop_img_dir = save_dir+split+'/image/'
  if not os.path.exists(crop_img_dir):
    os.makedirs(crop_img_dir)
  crop_mask_dir = save_dir+split+'/mask/'
  if not os.path.exists(crop_mask_dir):
    os.makedirs(crop_mask_dir)
  
  for file_count in range(len(file_names)):
    print "Processing the %d/%d image" %(file_count+1,len(file_names))
	# read image and the corresponding ground truth
    img_file_name = file_names[file_count]
    gt_file_name = img_file_name[:-4] + '.txt'
    img = skimage.io.imread(file_names[file_count])
    gts = np.loadtxt(gt_file_name,delimiter = '\t')
	
	# size of the original image
    IMG_HEIGHT = img.shape[0]
    IMG_WIDTH = img.shape[1]
    num_col_crop = int(np.ceil(IMG_WIDTH/float(IMG_SIZE)))
    num_row_crop = int(np.ceil(IMG_HEIGHT/float(IMG_SIZE)))
    padded_img = pad_image(img,CROP_SIZE,CROP_SIZE)	# pad image boundaries
    
    for row_cnt in range(num_row_crop):
      for col_cnt in range(num_col_crop):
        img_crop = np.zeros((IMG_SIZE+CROP_SIZE-1,IMG_SIZE+CROP_SIZE-1,3)).astype(np.uint8) #prelocate memory for image crops
        mask_crop = np.ones((IMG_SIZE,IMG_SIZE,1)).astype(np.uint8)*255						#prelocate memory for mask image
        #print "Row:%d, Col:%d" %(row_cnt,col_cnt)
        # starting and ending pixel number
        start_row = row_cnt*IMG_SIZE
        end_row = (row_cnt+1)*IMG_SIZE+CROP_SIZE-1
        start_col = col_cnt*IMG_SIZE
        end_col = (col_cnt+1)*IMG_SIZE+CROP_SIZE-1
        #print end_row,end_col,IMG_HEIGHT+CROP_SIZE,IMG_WIDTH+CROP_SIZE
        if end_row > IMG_HEIGHT+CROP_SIZE: # if image is not divisable by IMG_HEIGHT
          end_row = IMG_HEIGHT+CROP_SIZE-1
        if end_col > IMG_WIDTH+CROP_SIZE:
          end_col = IMG_WIDTH+CROP_SIZE-1
          #print end_col,col_cnt*IMG_SIZE
        img_crop[:end_row-row_cnt*IMG_SIZE,:end_col-col_cnt*IMG_SIZE,:] = padded_img[start_row:end_row,start_col:end_col,:]
        crop_name = crop_img_dir + os.path.basename(img_file_name)[:-4] + '_R%d_C%d.tif' %(row_cnt,col_cnt)
        with warnings.catch_warnings():
          warnings.simplefilter("ignore")
          skimage.io.imsave(crop_name, img_crop)
		
        # find all the ground truth in this area
        gts_mask = []
        for j in range(gts.shape[0]):
          gt_y = gts[j,1]
          gt_x = gts[j,0]
          gt_offset_y = gt_y-1-row_cnt*IMG_SIZE
          gt_offset_x = gt_x-1-col_cnt*IMG_SIZE
          if gt_offset_x>=-neg_neighbor and gt_offset_x < IMG_SIZE+neg_neighbor and gt_offset_y>=-neg_neighbor and gt_offset_y<IMG_SIZE+neg_neighbor:
            gts_mask.append([gt_offset_y,gt_offset_x])
        
        mask_name = crop_mask_dir + os.path.basename(img_file_name)[:-4] + '_R%d_C%d.tif' %(row_cnt,col_cnt)
        for j in range(len(gts_mask)):
          for cnt_x in range(-neg_neighbor,neg_neighbor+1):
            for cnt_y in range(-neg_neighbor,neg_neighbor+1):
              pix = 255
              if np.sqrt(cnt_x*cnt_x+cnt_y*cnt_y)<=neg_neighbor:
                pix = 1
              if np.sqrt(cnt_x*cnt_x+cnt_y*cnt_y)<=pos_neighbor:
                pix = 0
              if gts_mask[j][0] + cnt_y>=0 and gts_mask[j][0] + cnt_y<IMG_SIZE and gts_mask[j][1] + cnt_x>=0 and gts_mask[j][1] + cnt_x<IMG_SIZE:
                mask_crop[gts_mask[j][0] + cnt_y,gts_mask[j][1] + cnt_x] = pix
        with warnings.catch_warnings():
          warnings.simplefilter("ignore")    
          skimage.io.imsave(mask_name,mask_crop)
	

if __name__ == '__main__':
  # all the variables need to be changed
  TRAIN_DIR = 'C:/Users/bkong/Desktop/data/train/'
  TEST_DIR = 'C:/Users/bkong/Desktop/data/test/'
  SAVE_DIR = 'C:/Users/bkong/Desktop/crop/'
  train_split = 'train'
  test_split = 'test'
  CROP_SIZE = 101	# size of input for patch network
  IMG_SIZE = 500	# size of output for efficient network
  pos_neighbor = 5
  neg_neighbor = 10
  
  
  # get all the training and testing images
  train_img_files = glob.glob(TRAIN_DIR+'*.tif')
  test_img_files = glob.glob(TEST_DIR+'*.tif')
  
  print "generate crops and masks for training images..."
  generate_crops(train_img_files,train_split,'train.txt',CROP_SIZE,IMG_SIZE,pos_neighbor,neg_neighbor,SAVE_DIR)
  print "generate crops and masks for testing images..."
  generate_crops(test_img_files,test_split,'test.txt',CROP_SIZE,IMG_SIZE,pos_neighbor,neg_neighbor,SAVE_DIR)
  print "Done."
