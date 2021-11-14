#### START: hide tensorflow output
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
tf.autograph.set_verbosity(0)
#### END: hide tensorflow output

import json
import matplotlib.pyplot as plt
from tf_utils import Model
from io_utils import get_mnist_data, get_photos_data


def save_multiple_images(images, labels, filepath):
    plt.figure(figsize=(5, 6))
    for i in range(30):
        plt.subplot(5,6,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i])
        plt.xlabel(labels[i])
    plt.savefig(filepath)
    plt.clf()
    plt.close()


if __name__ == '__main__':
    ### collect data
    ds_train_images, ds_train_labels, ds_test_images_1, ds_test_labels_1 = get_mnist_data()
    ds_test_images_2, ds_test_labels_2 = get_photos_data('my_1') # my dataset 1
    ds_test_images_3, ds_test_labels_3 = get_photos_data('my_2') # my dataset 2
    ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed = get_photos_data('my_1', preprocess=True) # my dataset 1
    ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed = get_photos_data('my_2', preprocess=True) # my dataset 2
    
    ### save data preview
    preview_path = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                ), 'dataset', 'preview')
    os.system(f'mkdir -p {preview_path}')
    save_multiple_images(ds_test_images_2,
                         ds_test_labels_2,
                         f'{preview_path}/my_1.png')
    save_multiple_images(ds_test_images_2_preprocessed,
                         ds_test_labels_2_preprocessed,
                         f'{preview_path}/my_1_preprocessed.png')
    save_multiple_images(ds_test_images_3,
                         ds_test_labels_3,
                         f'{preview_path}/my_2.png')
    save_multiple_images(ds_test_images_3_preprocessed,
                         ds_test_labels_3_preprocessed,
                         f'{preview_path}/my_2_preprocessed.png')
    
    options = [
        #### layers
        # {
        #     'name': 'dense64relu_adam_10_8',
        #     'layers': [tf.keras.layers.Flatten(input_shape=(28, 28)),
        #                tf.keras.layers.Dense(64, activation='relu')]
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        # {
        #     'name': 'dense128relu_adam_10_8',
        #     'layers': [tf.keras.layers.Flatten(input_shape=(28, 28)),
        #                tf.keras.layers.Dense(128, activation='relu')],
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        # {
        #     'name': 'dense256relu_adam_10_8',
        #     'layers': [tf.keras.layers.Flatten(input_shape=(28, 28)),
        #                tf.keras.layers.Dense(256, activation='relu')],
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        # {
        #     'name': 'dense196relu_dense49relu_adam_10_8',
        #     'layers': [tf.keras.layers.Flatten(input_shape=(28, 28)),
        #                tf.keras.layers.Dense(196, activation='relu'),
        #                tf.keras.layers.Dense(49, activation='relu')],
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        # {
        #     'name': 'dense392relu_dense98relu_dense24relu_adam_10_8',
        #     'layers': [tf.keras.layers.Flatten(input_shape=(28, 28)),
        #                tf.keras.layers.Dense(392, activation='relu'),
        #                tf.keras.layers.Dense(98, activation='relu'),
        #                tf.keras.layers.Dense(24, activation='relu')],
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        # {
        #     'name': 'conv2d32relu_maxpool2d_adam_10_8',
        #     'layers': [tf.keras.layers.Conv2D(32, kernel_size=5, activation='relu', input_shape=(28, 28, 1)),
        #                tf.keras.layers.MaxPool2D(),
        #                tf.keras.layers.Flatten()],
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        # {
        #     'name': 'conv2d32relu_maxpool2d_conv2d32relu_maxpool2d_adam_10_8',
        #     'layers': [tf.keras.layers.Conv2D(32, kernel_size=5, activation='relu', input_shape=(28, 28, 1)),
        #                tf.keras.layers.MaxPool2D(),
        #                tf.keras.layers.Conv2D(32, kernel_size=4, activation='relu'),
        #                tf.keras.layers.MaxPool2D(),
        #                tf.keras.layers.Flatten()],
        #     'optimizer': 'adam',
        #     'epochs': 10,
        #     'bs': 8
        # },
        {
            'name': 'conv2d32relu_maxpool2d_conv2d32relu_maxpool2d_conv2d32relu_maxpool2d_adam_10_8',
            'layers': [tf.keras.layers.Conv2D(32, kernel_size=5, activation='relu', input_shape=(28, 28, 1)),
                       tf.keras.layers.MaxPool2D(),
                       tf.keras.layers.Conv2D(32, kernel_size=4, activation='relu'),
                       tf.keras.layers.MaxPool2D(),
                       tf.keras.layers.Conv2D(32, kernel_size=3, activation='relu'),
                       tf.keras.layers.MaxPool2D(),
                       tf.keras.layers.Flatten()],
            'optimizer': 'adam',
            'epochs': 10,
            'bs': 8
        },
    ]
    ### run tests
    results_path = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                ), 'results')
    os.system(f'mkdir -p {results_path}')
    for o in options:
        os.system(f'mkdir -p {results_path}/{o["name"]}')
        m = Model(o['name'])
        m.set_layers(o['layers'])
        m.set_optimizer(o['optimizer'])
        # m.create(load_from_checkpoint=False)
        m.create(load_from_checkpoint=True)
        m.show()
        # m.train(ds_train_images, ds_train_labels, o['epochs'], o['bs'])
        # m.save_train_history(f'{results_path}/{o["name"]}')
        with open(f'{results_path}/{o["name"]}/config', 'w+') as f:
            del o['layers']
            f.write(json.dumps(o, indent=4, sort_keys=True) + '\n')
            loss, accuracy = m.test(ds_test_images_1, ds_test_labels_1)
            f.write(f'MNIST             -> loss: {loss:.5f} accuracy {accuracy:.5f}\n')
            loss, accuracy = m.test(ds_test_images_2, ds_test_labels_2)
            f.write(f'MY_1              -> loss: {loss:.5f} accuracy {accuracy:.5f}\n')
            loss, accuracy = m.test(ds_test_images_3, ds_test_labels_3)
            f.write(f'MY_2              -> loss: {loss:.5f} accuracy {accuracy:.5f}\n')
            loss, accuracy = m.test(ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed)
            f.write(f'MY_1_PREPROCESSED -> loss: {loss:.5f} accuracy {accuracy:.5f}\n')
            loss, accuracy = m.test(ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed)
            f.write(f'MY_2_PREPROCESSED -> loss: {loss:.5f} accuracy {accuracy:.5f}\n')

    