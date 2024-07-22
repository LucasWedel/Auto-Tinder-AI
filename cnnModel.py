import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def load_data(train_directory, validation_directory):
    def load_images_from_directory(directory):
        X = []
        y = []
        for label, sub_dir in enumerate(['0', '1']):
            subdir_path = os.path.join(directory, sub_dir)
            for image_file in os.listdir(subdir_path):
                image_path = os.path.join(subdir_path, image_file)
                image = cv2.imread(image_path)
                image = cv2.resize(image, (224, 224))
                image = preprocess_input(image)
                X.append(image)
                y.append(label)
        return np.array(X), np.array(y)

    train_data, train_labels = load_images_from_directory(train_directory)
    validation_data, validation_labels = load_images_from_directory(validation_directory)

    return train_data, train_labels, validation_data, validation_labels

train_directory = r'C:\Users\lucas\OneDrive\Documents\UNI Software\Tinders\Billeder_training'
validation_directory = r'C:\Users\lucas\OneDrive\Documents\UNI Software\Tinders\Billeder_validation'

train_data, train_labels, validation_data, validation_labels = load_data(train_directory, validation_directory)

base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

base_model.trainable = False

inputs = tf.keras.Input(shape=(224, 224, 3))
x = base_model(inputs, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(512, activation='relu')(x)
x = layers.Dropout(0.5)(x)
outputs = layers.Dense(1, activation='sigmoid')(x)
model = models.Model(inputs, outputs)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest')

train_datagen.fit(train_data)

history = model.fit(train_datagen.flow(train_data, train_labels, batch_size=32),
                    steps_per_epoch=len(train_data) // 32,
                    epochs=10,
                    validation_data=(validation_data, validation_labels))

base_model.trainable = True
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history_fine_tune = model.fit(train_data, train_labels, epochs=10, validation_data=(validation_data, validation_labels))

test_loss, test_acc = model.evaluate(validation_data, validation_labels)
print('Test accuracy:', test_acc)

model.save(r'C:\Users\lucas\OneDrive\Documents\UNI Software\Tinders\saved_model_h5.h5')
