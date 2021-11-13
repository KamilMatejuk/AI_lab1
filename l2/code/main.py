#### START: hide tensorflow output
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
#### END: hide tensorflow output

import matplotlib.pyplot as plt
from tf_utils import Model
from io_utils import get_mnist_data, get_photos_data

# def show_image(image):
#     plt.figure()
#     plt.imshow(image)
#     plt.colorbar()
#     plt.grid(False)
#     plt.show()

def show_multiple_images(images, labels):
    plt.figure(figsize=(10,10))
    for i in range(30):
        plt.subplot(5,6,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        im = plt.imshow(images[i])
        plt.colorbar(im)
        plt.xlabel(labels[i])
    plt.show()

# TODO
# wybranie parametrów do sprawdzenia
# wizualizacja uczenia


if __name__ == '__main__':
    ds_train_images, ds_train_labels, ds_test_images_1, ds_test_labels_1 = get_mnist_data()
    # raw data
    ds_test_images_2, ds_test_labels_2 = get_photos_data('my_1') # my dataset 1
    ds_test_images_3, ds_test_labels_3 = get_photos_data('my_2') # my dataset 2
    # preprocessed data
    ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed = get_photos_data('my_1', preprocess=True) # my dataset 1
    ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed = get_photos_data('my_2', preprocess=True) # my dataset 2
    
    # show_multiple_images(ds_test_images_2, ds_test_labels_2)
    # show_multiple_images(ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed)
    # show_multiple_images(ds_test_images_3, ds_test_labels_3)
    # show_multiple_images(ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed)
    # exit()
    
    m = Model('default')
    m.set_layers([tf.keras.layers.Dense(128, activation='relu')])
    m.set_optimizer('adam')
    m.set_loss(tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))
    m.create()
    m.show()
    # m.train(ds_train_images, ds_train_labels, 10, 16)
    m.test(ds_test_images_1, ds_test_labels_1) # test mnist data
    # raw data
    m.test(ds_test_images_2, ds_test_labels_2) # test my data
    m.test(ds_test_images_3, ds_test_labels_3) # test collegue data
    # preprocessed
    m.test(ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed) # test my data
    m.test(ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed) # test collegue data
    