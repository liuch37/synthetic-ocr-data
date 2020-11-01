# A synthetic OCR data generatior
This repository is to generate synthetic data for scene text detection and recognition from open source tools.

## Script command example
``
python synthetic_generator.py --data ./synthetic --image ./synthetic/images/ --label ./synthetic/labels/ --word ./synthetic/words/ --patch ./synthetic/patches --num 10
``

--data: Directory to store downloaded data (fonts and background images).

--image: Directory to store synthesized images.

--label: Directory to store synthesized polygon word labels for each synthesized image, line by line.

--word: Directory to store word text labels for each synthesized image, line by line.

--patch: Directory to store word patches with word text as its image file name.

--num: Number of synthetic images to be generated.

*Other parameters e.g., font size, word line rotation angle,...etc can be tuned inside main generator function.

## Image generated examples
![synthetic image 1](https://github.com/liuch37/synthetic-ocr-data/blob/main/misc/image1.png)

![synthetic image 2](https://github.com/liuch37/synthetic-ocr-data/blob/main/misc/image2.png)

## Word patch generated examples
![synthetic patch 1](https://github.com/liuch37/synthetic-ocr-data/blob/main/misc/patch1.png)

![synthetic patch 2](https://github.com/liuch37/synthetic-ocr-data/blob/main/misc/patch2.png)

## References
[1] https://github.com/faustomorales/keras-ocr
