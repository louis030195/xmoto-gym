# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os

"""
Load score images
"""
def load_data():
    pass

"""
Create the keras model
"""
def create_model():
    model = keras.Sequential()
    # Must define the input shape in the first layer of the neural network
    model.add(keras.layers.Conv2D(filters=64, kernel_size=2, padding='same', activation='relu', input_shape=(24,24,3))) 
    model.add(keras.layers.MaxPooling2D(pool_size=2))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=2))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(256, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(10, activation='softmax'))
    return model

"""
Extract digits images from an image of the score
https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/
"""
def extract_digits(score_image):
    # find contours in the thresholded image, then initialize the
    # digit contours lists
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    digitCnts = []

    # loop over the digit area candidates
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        # if the contour is sufficiently large, it must be a digit
        if w >= 15 and (h >= 30 and h <= 40):
            digitCnts.append(c)

    return digitCnts

"""
With the full score image, split it into single digit, classify, rebuild the number,
return the full number
"""
def score_value(score_image):
    digits = extract_digits(score_image)

    # Get latest weights
    model = create_model()
    model.load_weights(tf.train.latest_checkpoint("training_1/cp.ckpt"))

    # Classify the digits
    predictions = []
    for digit in digits:
        predictions.append(model.predict(digit))

    # Rebuild the full number
    full_number = ''
    for digit in predictions:
        full_number += str(digit) 
    return int(full_number)

def train_model():
    (X, y) = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    checkpoint_dir = os.path.dirname("training_1/cp.ckpt")

    # Create checkpoint callback
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
                                                    save_weights_only=True,
                                                    verbose=1)
    model = create_model()
    
    model.compile(optimizer=tf.train.AdamOptimizer(), 
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=5,
                validation_data = (X_test,y_test),
                callbacks = [cp_callback])

    test_loss, test_acc = model.evaluate(X_test, y_test)
    print('Test accuracy:', test_acc)

    # Save entire model to a HDF5 file (manual saving)
    # model.save('my_model.h5')