import os
import math
import numpy as np
from PIL import Image


def get_int(file, number_of_bytes):
    return int.from_bytes(
        file.read(number_of_bytes), 
        byteorder='big',
        signed=False)

def get_data_from_idx_labels_file(filename: str):
    with open(filename, 'rb') as f:
        magic_number = get_int(f, 4)
        number_of_items = get_int(f, 4)
        data = np.empty(number_of_items)
        for i in range(number_of_items):
            data[i] = get_int(f, 1)
        return data

def get_data_from_idx_images_file(filename: str):
    with open(filename, 'rb') as f:
        magic_number = get_int(f, 4)
        number_of_images = get_int(f, 4)
        number_of_rows = get_int(f, 4)
        number_of_cols = get_int(f, 4)
        data = np.empty((number_of_images, number_of_rows, number_of_cols))
        for i in range(number_of_images):
            for r in range(number_of_rows):
                for c in range(number_of_cols):
                    data[i, r, c] = get_int(f, 1)
    return data

def get_mnist_data():
    data_dir = os.path.join(
            os.path.abspath(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            ), 'dataset', 'mnist')
    print('Downloading MNIST dataset ...')
    ds_train_labels = get_data_from_idx_labels_file(os.path.join(data_dir, 'train-set-labels.idx'))
    print(f'Downloaded training labels {ds_train_labels.shape}')
    ds_train_images = get_data_from_idx_images_file(os.path.join(data_dir, 'train-set-images.idx'))
    print(f'Downloaded training images {ds_train_images.shape}')
    ds_test_labels  = get_data_from_idx_labels_file(os.path.join(data_dir, 'test-set-labels.idx'))
    print(f'Downloaded test labels {ds_test_labels.shape}')
    ds_test_images  = get_data_from_idx_images_file(os.path.join(data_dir, 'test-set-images.idx'))
    print(f'Downloaded test images {ds_test_images.shape}')
    ds_train_images = ds_train_images / 255.0
    ds_test_images  = ds_test_images  / 255.0
    return (ds_train_images, ds_train_labels, ds_test_images, ds_test_labels)

def extract_data_from_photo(img_path: str):
    # read pixels
    im = Image.open(img_path, 'r')
    w, h = im.size
    pixels = [[0 for _ in range(w)] for _ in range(h)]
    i = 0
    for pixel in im.getdata():
        # convert to grayscale
        p = np.mean(pixel)
        # normalize
        p = p/255.0
        # enhance black white difference
        p = (p-0.5) * 4 + 0.5
        p = min(max(p, 0), 1)
        # save
        pixels[int(i/h)][int(i%h)] = p
        i += 1
    # find binding box
    # top border
    try:
        for row_index_top, row in enumerate(pixels):
            for pixel in row:
                if pixel < 0.1:
                    raise ValueError('Found bounding box')
    except ValueError: pass
    # bottom border
    try:
        for row_index_bottom, row in enumerate(pixels[::-1]):
            for pixel in row:
                if pixel < 0.1:
                    raise ValueError('Found bounding box')
    except ValueError: pass
    # left border
    try:
        for col_index_left in range(len(pixels[0])):
            for i in range(len(pixels)):
                if pixels[i][col_index_left] < 0.1:
                    raise ValueError('Found bounding box')
    except ValueError: pass
    # right border
    try:
        for col_index_right in range(len(pixels[0])-1, 0, -1):
            for i in range(len(pixels)):
                if pixels[i][col_index_right] < 0.1:
                    raise ValueError('Found bounding box')
    except ValueError: pass
    if col_index_left < col_index_right:
        if row_index_top < len(pixels) - row_index_bottom:
            pixels = [[p for p in row[col_index_left:col_index_right]] for row in pixels[row_index_top:len(pixels)-row_index_bottom]]
    # convert to size (20 x 20)
    w = len(pixels[0])
    h = len(pixels)
    scale = math.ceil(max(w, h) / 20)
    scaled_pixels = []
    w = math.ceil(w/scale)
    h = math.ceil(h/scale)
    for i in range(h):
        for j in range(w):
            subset = [[p for p in row[scale*j:scale*(j+1)-1]] for row in pixels[scale*i:scale*(i+1)-1]]
            scaled_pixels.append(max(sum(subset, [])))
    # enhance black white difference
    enhanced_pixels = []
    for p in scaled_pixels:
        p = (p-0.8) * 4 + 0.8
        p = min(max(p, 0), 1)
        enhanced_pixels.append(p)
    
    # fill to size (28 x 28)
    empty_pixels = [[1.0 for _ in range(28)] for _ in range(28)]
    i = 0
    while i < h:
        j = 0
        while j < w:
            empty_pixels[int((28-h)/2) + i][int((28-w)/2) + j] = enhanced_pixels[w*i+j]
            j += 1
        i += 1
    
    return empty_pixels
    # new_im = Image.new('L', (28, 28))
    # new_im.putdata([int(p * 255) for p in sum(empty_pixels, [])])
    # new_im.save('test.png')

def get_photos_data(folder: str):
    data_dir = os.path.join(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                ), 'dataset', folder)
    print(f'Preparing data from {data_dir}')
    ds_images = []
    ds_labels = []
    for img in os.listdir(data_dir):
        if img.endswith('.jpg') or img.endswith('.png'):
            ds_images.append(extract_data_from_photo(os.path.join(data_dir, img)))
            ds_labels.append(int(img.split('_')[0]))
    return (np.array(ds_images).astype('float32'),
            np.array(ds_labels).astype('float32'))


if __name__ == '__main__':
    images, labels = get_photos_data('my_1')
    print(images.shape)
    print(labels.shape)
    
    import matplotlib.pyplot as plt
    plt.figure()
    plt.imshow(images[0])
    plt.colorbar()
    plt.grid(False)
    plt.xlabel(labels[0])
    plt.show()