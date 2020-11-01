'''
This code is to generate synthetic images with random background for scene text detection and recognition, using keras-ocr package.
'''
import datetime
import string
import math
import os
import argparse

import tqdm
import matplotlib.pyplot as plt
import tensorflow as tf
import sklearn.model_selection
import numpy as np
import cv2

import keras_ocr
import pdb

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data', type=str, default='synthetic', help='directory to store downloaded data')
    parser.add_argument(
        '--image', type=str, default='images', help='directory to store synthesized images')
    parser.add_argument(
        '--label', type=str, default='labels', help='directory to store synthesized polygon labels for each synthesized image')
    parser.add_argument('--word', type=str, default='words', help='directory to store word labels for each synthesized image')
    parser.add_argument('--patch', type=str, default='patches', help='directory to store word patches with its name as word label')
    parser.add_argument('--num', type=int, default=1, help='number of synthetic images to be generated')

    opt = parser.parse_args()
    print(opt)

    data_dir = opt.data
    image_dir = opt.image
    label_dir = opt.label
    word_dir = opt.word
    patch_dir = opt.patch
    num_images = opt.num

    # make output folders
    try:
        os.makedirs(data_dir)
    except OSError:
        pass
    try:
        os.makedirs(image_dir)
    except OSError:
        pass
    try:
        os.makedirs(label_dir)
    except OSError:
        pass
    try:
        os.makedirs(word_dir)
    except OSError:
        pass
    try:
        os.makedirs(patch_dir)
    except OSError:
        pass

    alphabet = string.printable[:-6] # 94 valid char
    #recognizer_alphabet = ''.join(sorted(set(alphabet.lower())))
    fonts = keras_ocr.data_generation.get_fonts(
        alphabet=alphabet,
        cache_dir=data_dir
    )
    backgrounds = keras_ocr.data_generation.get_backgrounds(cache_dir=data_dir)

    text_generator = keras_ocr.data_generation.get_text_generator(alphabet=alphabet)
    print('The first generated text is:', next(text_generator))

    image_generators = keras_ocr.data_generation.get_image_generator(
                           height=640,
                           width=640,
                           text_generator=text_generator,
                           font_groups={
                               alphabet: fonts
                           },
                           backgrounds=backgrounds,
                           font_size=(60, 120),
                           margin=50,
                           rotationX=(-0.05, 0.05),
                           rotationY=(-0.05, 0.05),
                           rotationZ=(-5, 5)
                        )

    for idx in range(num_images):
        image, lines = next(image_generators)
        image_overlay = image.copy()
        for line in lines:
            num_char = len(line)
            word = ""
            polygon_pair = []
            polygon_xy_pair = []
            for i in range(num_char):
                word += line[i][1]
                polygon = line[i][0]
                polygon_xy_pair.append([int(polygon[0][0]), int(polygon[0][1])])
                polygon_xy_pair.append([int(polygon[1][0]), int(polygon[1][1])])

                polygon_pair.append(int(polygon[0][0]))
                polygon_pair.append(int(polygon[0][1]))
                polygon_pair.append(int(polygon[1][0]))
                polygon_pair.append(int(polygon[1][1]))
            for i in range(num_char-1, -1, -1):
                polygon = line[i][0]
                polygon_xy_pair.append([int(polygon[2][0]), int(polygon[2][1])])
                polygon_xy_pair.append([int(polygon[3][0]), int(polygon[3][1])])

                polygon_pair.append(int(polygon[2][0]))
                polygon_pair.append(int(polygon[2][1]))
                polygon_pair.append(int(polygon[3][0]))
                polygon_pair.append(int(polygon[3][1]))

            with open(os.path.join(label_dir, str(idx)+'.txt'), 'a') as f:
                poly_string = ','.join([str(s) for s in polygon_pair])
                f.writelines(poly_string+'\n')
            with open(os.path.join(word_dir, str(idx)+'.txt'), 'a') as f:
                f.writelines(word+'\n')

            pts = np.array(polygon_xy_pair, np.int32)
            #pts = pts.reshape((-1,1,2))
            #cv2.polylines(image_overlay,[pts],True,(0,255,0), 8)
            xmin, ymin, xmax, ymax = min(pts[:,0]), min(pts[:,1]), max(pts[:,0]), max(pts[:,1])
            patch = image[ymin:ymax+1, xmin:xmax+1, :]
            plt.imsave(os.path.join(patch_dir, str(word)+'.png'), patch)

        plt.imsave(os.path.join(image_dir, str(idx)+'.png'), image)
        #plt.imshow(image_overlay)
        #plt.show()