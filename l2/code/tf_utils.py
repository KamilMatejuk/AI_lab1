import tensorflow as tf
import os
from io_utils import get_data_from_idx_labels_file, get_data_from_idx_images_file

class Model:
    def __init__(self, id: str):
        self.id = id
        self.checkpoint_dir = os.path.join(
            os.path.abspath(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            ), 'checkpoints', id)
        self.checkpoint_path = os.path.join(self.checkpoint_dir, 'checkpoint')
        os.system(f'mkdir -p {self.checkpoint_dir}')
        # default
        self.model = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                tf.keras.layers.Dense(128, activation='relu'),
                tf.keras.layers.Dense(10)], name=self.id)
        self.optimizer = 'adam'
        self.loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        
    
    def set_layers(self, layers: list):
        # input and output always the same
        self.model = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                *layers,
                tf.keras.layers.Dense(10)
            ], name=self.id)
    
    def set_optimizer(self, optimizer: str):
        self.optimizer = optimizer
    
    def set_loss(self, loss: tf.keras.losses.Loss):
        self.loss = loss
    
    def create(self):
        self.model.compile(
            optimizer=self.optimizer,
            loss=self.loss,
            metrics=['accuracy'])
        if os.path.isfile(self.checkpoint_path):
            self.model.load_weights(self.checkpoint_path)
    
    def show(self):
        self.model.summary()
    
    def train(self, ds_train_images, ds_train_labels, epochs, batch_size):
        cp_callback = tf.keras.callbacks.ModelCheckpoint(
            filepath=self.checkpoint_path,
            save_weights_only=True,
            verbose=0)
        self.history = self.model.fit(ds_train_images, ds_train_labels,
              epochs=epochs,
              batch_size=batch_size,
              callbacks=[cp_callback])
        # print(self.history)
    
    def test(self, ds_test_images, ds_test_labels):
        self.model.evaluate(ds_test_images,  ds_test_labels, verbose=2)
