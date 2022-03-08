import imutils
import cv2
import numpy as np
from face_enhancement import FaceEnhancement

import os
import matplotlib.pyplot as plt

def get_model_from_path():
    model_2 = {'name':'GPEN-BFR-512', 'size':512, 'channel_multiplier':2, 'narrow':1}
    
    faceenhancer = FaceEnhancement(use_sr=True, out_size=model_2['size'], model=model_2['name'], channel_multiplier=model_2['channel_multiplier'], narrow=model_2['narrow'])

    return faceenhancer

def style_transfer(image_lr, model):
    cv2.imwrite("image.png",image_lr) 
    #image_lr = cv2.bitwise_not(image_lr)
    og_image =  image_lr.copy()
    image_hr, _, _ = model.process(image_lr)
    #print("HELLO+")
    og_image = cv2.resize(og_image, image_hr.shape[:2][::-1])
    
    final_image = np.hstack((og_image, image_hr))

    return final_image

    

