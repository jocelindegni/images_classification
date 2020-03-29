# Import dependencies
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model, model_from_json
import numpy as np
import pandas as pd
import os
import cv2
from imutils import paths
import matplotlib.pyplot as plt
import shutil


# Functions for predictions
def prediction(imagePaths):
    """
        input: path of directory of contain image for classification
        output: 
    """
    label = {0: 'budget', 1: 'file_folder',
             2: 'form', 3: 'handwritten',
             4: 'invoice', 5: 'specification'}

    # Loading the model
    json_file = open('model_holistic.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights('model_holistic.h5')

    classes = []
    proba = []
    filename = []

    # imagePaths = list(paths.list_images(path))

    # if is directory
    for image_ in imagePaths:
        img = cv2.imread(image_)
        img = cv2.resize(img, (256, 256))
        img = np.reshape(img, [1, 256, 256, 3]) / 255.
        prediction = model.predict(img)
        prediction = prediction.tolist()
        maxprob = prediction[0].index(max(prediction[0]))
        if maxprob in label:
            l = (label[maxprob])
        classes.append(l)
        name = image_.split('/')[-1]
        proba.append(max(prediction[0]))
        filename.append(name)
    data = pd.DataFrame({'filename': filename,
                         'classes': classes,
                         'probability': proba})
    # data_json = data.to_json(orient='records')[1:-1].replace('},{', '} {')
    print('prediction is done with suscessfull')
    return data


# putting in emerging folders
def create_folder_by_class(df, path):
    """  Creating directory by classes
        df is the dataframe result from prediction
    """
    for classes in df.classes.values:
        try:
            os.mkdir('./static/image_classified')
        except:
            pass
        try:
            os.mkdir('./static/image_classified' + '/' + classes)
        except:
            pass
        for filename in df[df['classes'] == classes]['filename'].values:
            shutil.move(path + '/' + filename, os.path.join('./static/image_classified/' + classes + '/', filename))
            # save_file_in_classdir(classes,filename)
    print('Classification is finished is finished...')


# Creating output for visualization
def count_total_file(DIR):
    l = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return l


def classified_folder_needed(df):
    """
        dict used in route @classified_folder
        df: output of classification result
    """
    tot = []
    ad = []

    for i in [c for c in list(df.classes.unique()) if not c.startswith('.')]:
        total = count_total_file(DIR='./static/image_classified/' + i)
        added = df[df['classes'] == i].shape[0]
        ad.append(added)
        tot.append(total)
    df_dict = pd.DataFrame({'total': tot, 'add': ad},
                           index=[c for c in list(df.classes.unique()) if not c.startswith('.')])
    df_dict = df_dict.T
    dict_df = df_dict.to_dict()
    return dict_df


# run for classification
def main(imagePaths):
    df = prediction(imagePaths)
    create_folder_by_class(df, imagePaths)
    df = classified_folder_needed(df)
    return df
