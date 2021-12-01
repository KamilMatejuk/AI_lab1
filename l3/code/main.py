import os
import sys
import traceback
from mypool import MyPool
from cluster import Clustering
from io_utils import get_mnist_data, get_photos_data


ds_train_images, ds_train_labels, ds_test_images_1, ds_test_labels_1 = get_mnist_data()


def run_for_k(k: int):
    try:
        ### run tests
        results_path = os.path.join(
                    os.path.dirname(
                        os.path.dirname(
                            os.path.abspath(__file__)
                        )
                    ), 'results', f'{k}-clusters')
        os.system(f'mkdir -p {results_path}')
        
        cluster = Clustering(k, results_path, verbose=('-v' in sys.argv))
        # divide into clusters (5 tries)
        cluster.train(ds_train_images, ds_train_labels, 5, 40)
        # save mean values, inertion etc
        cluster.save()
        # show accuracy (matrix k x 10)
        cluster.test_accuracy()
        # show centroids
        cluster.show_centroids('centroids_end.png')
        
        ### collect data
        ds_test_images_2, ds_test_labels_2 = get_photos_data('my_1')
        ds_test_images_3, ds_test_labels_3 = get_photos_data('my_2')
        ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed = get_photos_data('my_1', preprocess=True)
        ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed = get_photos_data('my_2', preprocess=True)
        tests = [
            (ds_test_images_1, ds_test_labels_1, 'test 1'),
            (ds_test_images_2, ds_test_labels_2, 'test 2'),
            (ds_test_images_2_preprocessed, ds_test_labels_2_preprocessed, 'test 2 preprocessed'),
            (ds_test_images_3, ds_test_labels_3, 'test 3'),
            (ds_test_images_3_preprocessed, ds_test_labels_3_preprocessed, 'test 3 preprocessed'),
        ]
        for t in tests:
            # show accuracy (matrix k x 10)
            cluster.test_accuracy(*t)
    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    with MyPool(2) as pool:
        pool.map(run_for_k, (7, 8, 9, 11, 12))
    # run_for_k(7)