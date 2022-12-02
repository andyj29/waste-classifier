import glob
import os
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from IPython.display import display


base_path = r'/Users/phongnguyen/Documents/waste-classification/datasets'
img_list = glob.glob(os.path.join(base_path, '*/*.jpg'))


class Generator:
    @staticmethod
    def generate_train_data_flow():
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            shear_range=0.1,
            zoom_range=0.1,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            vertical_flip=True,
            validation_split=0.1
        )

        train_data_flow = train_datagen.flow_from_directory(
            base_path,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            subset='training',
            seed=0
        )

        return train_data_flow

    @staticmethod
    def generate_test_data_flow():
        test_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.1
        )

        test_data_flow = test_datagen.flow_from_directory(
            base_path,
            target_size=(224, 224),
            batch_size=32,
            class_mode='categorical',
            subset='validation',
            seed=0
        )

        return test_data_flow


class Utils:
    @staticmethod
    def convert_from_pb_to_h5(pb_folder_path, h5_path):
        try:
            model = tf.keras.models.load_model(pb_folder_path)
        except OSError:
            print('Can not open {pb_folder_path} folder')
        print(model.summary())
        tf.keras.models.save_model(model, h5_path)

    @staticmethod
    def plot_results(figsize, _range, labels, predictions, test_x, test_y):
        try:
            plt.figure(figsize=figsize)

            for i in range(_range):
                plt.subplot(4, 4, i+1)
                plt.title('pred:%s / truth:%s' % (labels[np.argmax(predictions[i])], labels[np.argmax(test_y[i])]))
                plt.imshow(test_x[i])
                plt.show()

            predicted = []
            actual = []

            for i in range(16):
                predicted.append(labels[np.argmax(predictions[i])])
                actual.append(labels[np.argmax(test_y[i])])

            df = pd.DataFrame(predicted, columns=["predicted"])
            df["actual"] = actual
            display(df)
        except (KeyError, ValueError):
            print('Invalid arguments')


   
