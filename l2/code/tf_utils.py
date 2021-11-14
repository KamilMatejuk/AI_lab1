import os
import tensorflow as tf
import matplotlib.pyplot as plt

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
        self.history = None
        
    
    def set_layers(self, layers: list):
        # input and output always the same
        self.model = tf.keras.Sequential([
                tf.keras.layers.Flatten(input_shape=(28, 28)),
                *layers,
                tf.keras.layers.Dense(10)
            ], name=self.id)
    
    def set_optimizer(self, optimizer: str):
        self.optimizer = optimizer
    
    def create(self, load_from_checkpoint = True):
        self.model.compile(
            optimizer=self.optimizer,
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])
        if load_from_checkpoint and os.path.isfile(self.checkpoint_path):
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
    
    def save_train_history(self, filedir):
        if self.history is not None:
            # loss
            loss = self.history.history['loss']
            loss_color = 'red'
            plt.plot([i+1 for i in range(len(loss))], loss, color=loss_color)
            plt.xlabel('epochs')
            plt.ylabel('loss')
            figure = plt.gcf()
            figure.set_size_inches(10, 3)
            plt.savefig(f'{filedir}/loss', dpi=100)
            plt.clf()
            plt.close()
            # accuracy
            accuracy = self.history.history['accuracy']
            accuracy_color = 'blue'
            plt.plot([i+1 for i in range(len(accuracy))], accuracy, color=accuracy_color)
            plt.xlabel('epochs')
            plt.ylabel('accuracy')
            figure = plt.gcf()
            figure.set_size_inches(10, 3)
            plt.savefig(f'{filedir}/accuracy', dpi=100)
            plt.clf()
            plt.close()
            # both
            fig, ax1 = plt.subplots()
            ax1.set_xlabel('epochs')
            ax1.set_ylabel('loss', color=loss_color)
            ax1.plot([i+1 for i in range(len(loss))], loss, color=loss_color)
            ax1.tick_params(axis='y', labelcolor=loss_color)
            ax2 = ax1.twinx()
            ax2.set_ylabel('accuracy', color=accuracy_color)
            ax2.plot([i+1 for i in range(len(accuracy))], accuracy, color=accuracy_color)
            ax2.tick_params(axis='y', labelcolor=accuracy_color)
            fig.tight_layout()
            figure = plt.gcf()
            figure.set_size_inches(10, 3)
            plt.savefig(f'{filedir}/loss_and_accuracy', dpi=100)
            plt.clf()
            plt.close()
    
    def test(self, ds_test_images, ds_test_labels):
        loss, accuracy = self.model.evaluate(ds_test_images,  ds_test_labels, verbose=0)
        return (loss, accuracy)
