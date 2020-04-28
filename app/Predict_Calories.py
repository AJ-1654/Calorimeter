#!/usr/bin/env python
# coding: utf-8

# In[6]:


from __future__ import absolute_import, division, print_function

import tensorflow as tf
import h5py
import tensorflow.keras.backend as K
from keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras import regularizers
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.regularizers import l2

from tensorflow import keras
from tensorflow.keras import models
from tensorflow.keras.applications.inception_v3 import preprocess_input

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img


# In[7]:


K.clear_session()
path = "C:/Users/Dell"
model_best = load_model(path + '/trainedmodel_30class.hdf5',compile = False)


# In[8]:


food_list = ['apple_pie', 'bread_pudding', 'cheese_plate', 'cheesecake', 'chicken_curry', 'chicken_quesadilla',
             'chocolate_cake', 'chocolate_mousse', 'cup_cakes', 'donuts', 'french_fries', 'french_toast', 'fried_rice',
             'garlic_bread', 'grilled_cheese_sandwich', 'hot_dog', 'ice_cream', 'lasagna', 'macaroni_and_cheese',
             'nachos', 'omelette', 'onion_rings', 'pancakes', 'pizza', 'ramen', 'red_velvet_cake','samosa', 
             'spring_rolls', 'tacos', 'waffles']

calorie_dict = {'apple_pie': 237, 'bread_pudding': 153, 'cheese_plate': 371, 'cheesecake': 321, 
                'chicken_curry': 110, 'chicken_quesadilla': 239, 'chocolate_cake': 371, 'chocolate_mousse': 225,
                'cup_cakes': 305, 'donuts': 452, 'french_fries': 312, 'french_toast': 229, 'fried_rice': 163,
                'garlic_bread': 350, 'grilled_cheese_sandwich': 350, 'hot_dog': 290, 'ice_cream': 207, 'lasagna': 135,
                'macaroni_and_cheese': 164, 'nachos': 306, 'omelette': 154, 'onion_rings': 411, 'pancakes': 227,
                'pizza': 266, 'ramen': 436, 'red_velvet_cake': 367, 'samosa': 91, 'spring_rolls': 154,
                'tacos': 226, 'waffles': 291}
def predict_class(img):
    img = image.load_img(img, target_size=(299, 299))
    img = image.img_to_array(img)                    
    img = np.expand_dims(img, axis=0)         
    img = preprocess_input(img)                                      

    pred = model_best.predict(img)
    index = np.argmax(pred)
    food_list.sort()
    pred_value = food_list[index]    
    return pred_value

def predict_cal(item):
    return calorie_dict[item]
    


# In[5]:





# In[ ]:




