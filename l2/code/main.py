#### START: hide tensorflow output
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
#### END: hide tensorflow output

import matplotlib.pyplot as plt
from tf_utils import Model
from io_utils import get_mnist_data

# def show_image(image):
#     plt.figure()
#     plt.imshow(image)
#     plt.colorbar()
#     plt.grid(False)
#     plt.show()

# def show_multiple_images(images, labels):
#     plt.figure(figsize=(10,10))
#     for i in range(25):
#         plt.subplot(5,5,i+1)
#         plt.xticks([])
#         plt.yticks([])
#         plt.grid(False)
#         plt.imshow(images[i], cmap=plt.cm.binary)
#         plt.xlabel(labels[i])
#     plt.show()

# TODO
# wczytywanie danych z foldera ze zdjęciami
# pokazanie wczytanych zdjęć
# wybranie parametrów do sprawdzenia
# wizualizacja uczenia


if __name__ == '__main__':
    ds_train_images, ds_train_labels, ds_test_images_1, ds_test_labels_1 = get_mnist_data()
    # ds_test_images_2, ds_test_labels_2 = get_photos_data('my_1') # my dataset 1
    # ds_test_images_3, ds_test_labels_3 = get_photos_data('my_2') # my dataset 2
    
    m = Model('default')
    m.set_layers([tf.keras.layers.Dense(128, activation='relu')])
    m.set_optimizer('adam')
    m.set_loss(tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))
    m.create()
    m.show()
    m.train(ds_train_images, ds_train_labels, 10, 16)
    m.test(ds_test_images_1, ds_test_labels_1) # test mnist data
    # m.test(ds_test_images_2, ds_test_labels_2) # test my data
    # m.test(ds_test_images_3, ds_test_labels_3) # test collegue data
    