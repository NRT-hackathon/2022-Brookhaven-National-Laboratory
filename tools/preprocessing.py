import cv2
from imutils import paths
import numpy as np
import os
import re

def parse_images_cv2(img_path, height, width):
  '''Given an image path, height, and width, return a resized float32 of the image.'''
  img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB).astype(np.float32)/255.0
  img_rsz = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
  return img_rsz

def get_filename_data(FILE_PATH, ext="jpeg", quiet=True):
  '''Find the x and y coordinates and labels (i.e. distance to the focal plane) 
  of the images in FILE_PATH by parsing image filenames. Assumes files are named
  with the format:
  <TITLE>_ix<X_COORD>_iy<Y_COORD>_<DIST_TO_FOCAL_PLANE>.<FILE_EXT>
  
  * FILE_PATH: a path string to a directory of files to process
  * ext: the file extension of files in FILE_PATH to process
  * quiet=False will print out a warning when filenames do not adhere to this
      standard, but processing of subsequent images will continue.'''

  # Store image labels (i.e. distances to focal plane).
  labels = []
  # Store image positions. Each image stack will be at a set of X and Y 
  # coordinates to be parsed from the filename.
  all_coords = []
  img_path_list = list(paths.list_files(FILE_PATH, validExts=ext))
  
  for img_path in img_path_list:
    # Extract the image label from the filename
    img_bname = os.path.basename(img_path)
    img_fname, _ = os.path.splitext(img_bname)
    img_fname_split = re.split('_| ',img_fname)
    found_label = False
    tried_multiple = False
    for s in reversed(img_fname_split):
      try:
        label = np.abs(float(s))
        found_label = True
      except ValueError:
        if not quiet:
          print("Unable to parse filename {}. Tried to read {} as label.".format(img_bname,s))
        tried_multiple = True
        continue
      if found_label and tried_multiple:
        if not quiet:
          print("Found label:",s)
        break
      if found_label:
        break
    labels.append(label)
    # Extract the image coordinates from the filename
    coords = [c for c in img_path.split("_") if "ix" in c or "iy" in c]
    coor = "_".join(coords)
    all_coords.append(coor)
  labels = np.array(labels)
  all_coords = np.array(all_coords)
  return labels, all_coords, img_path_list

def get_clean_infocus_coords(all_coords, labels, img_paths, height, width, 
                              intensity_thresh=0.50, eap_thresh=0.10): 
  '''Get coordinates of "clean" (i.e. not noise) images.

  * all_coords: all the x and y coordinate strings for the images being processed
  * labels: the image labels (i.e. distances to the focal plane)
  * intensity_thresh: the filtered image pixel intensity required to consider a 
      pixel to belong to an edge
  * eap_thresh: the edge area percentage threshold required to consider an 
      image "clean"'''

  # In-focus image path positions in the list of image paths
  infocus_img_pos = np.where(labels==0)[0]
  # X/Y coordinate strings of physical locations of in-focus images
  infocus_coords = all_coords[infocus_img_pos]
  # Convert filename list of in-focus images to numpy array for list indexing.
  infocus_paths = np.array(img_paths)[infocus_img_pos]
  # Store X and Y coordinates of "clean" image stacks
  clean_infocus_coords = []
  for img_path, pos in zip(infocus_paths, infocus_coords):
    img_pixel_vals = parse_images_cv2(img_path, height, width)[:,:,0]
    pixels_above_threshold = len(np.where(img_pixel_vals >= 
                                          intensity_thresh)[0])
    edge_percentage = pixels_above_threshold / height / width
    if edge_percentage >= eap_thresh:
      clean_infocus_coords.append(pos)
  return clean_infocus_coords

def get_clean_data(clean_infocus_coords, all_coords, labels, img_paths):
  '''Return the paths to images in "clean" image stacks.
  
  * clean_infocus_coords: coordinate strings for the in-focus images in a stack
  * all_coords: image coordinate strings for all images being processed
  * labels: the image labels (i.e. distances to the focal plane)
  * img_paths: file path strings to all images being processed
  '''

  clean_stack_pos_list = []
  for cs in clean_infocus_coords:
    clean_position = np.where(all_coords==cs)[0]
    for pos in clean_position:
      clean_stack_pos_list.append(pos)
  # Convert path list to numpy array to enable list indexing.
  img_paths = np.array(img_paths)
  clean_paths = img_paths[clean_stack_pos_list]
  clean_labels = labels[clean_stack_pos_list]
  return clean_labels, clean_paths

def get_capped_data(labels, img_paths, cap=20):
  '''Put a cap on the maximum allowable distance to the focal plane. Reject images 
   that are at a distance above this cap.
  
   * labels: the image labels (i.e. distances to the focal plane)
   * img_paths: file path strings for images
   * cap: the limit on an image's allowable maximum absolute distance to the 
      focal plane (in micrometers)
   '''
  
  # Do not include the focal distance larger than cap
  capped_labels = labels[np.where(np.abs(labels)<=cap)[0]]
  capped_paths = img_paths[np.where(np.abs(labels)<=cap)[0]]
  return capped_labels, capped_paths

def main():
  '''Driver function for preprocessing. Given a path to a directory of high pass
  filtered images, will return the labels (i.e. distances to the focal plane)
  and file paths of clean image data with distances capped at distance_cap.'''

  # Set default variable values
  FILE_PATH = "../sample_data/level1_jpeg/"
  extension = "jpeg"
  img_height = 1200
  img_width = 1920
  intensity_thresh = 0.50
  eap_thresh = 0.10
  distance_cap = 20

  labels, all_coords, img_paths = get_filename_data(FILE_PATH, ext="jpeg", quiet=False)
  clean_infocus_coords = get_clean_infocus_coords(all_coords, labels, img_paths, 
                                                  img_height, img_width, 
                                                  intensity_thresh=intensity_thresh, 
                                                  eap_thresh=eap_thresh)
  clean_labels, clean_paths = get_clean_data(clean_infocus_coords, all_coords, 
                                             labels, img_paths)
  capped_labels, capped_paths = get_capped_data(clean_labels, clean_paths, 
                                                cap=distance_cap)
  return

if __name__ == "__main__":
  main()
