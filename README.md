# microscope-autofocus
This code repository accompanies the paper "Autofocusing optical microscope using artificial neural network for large-area, high-magnification scanning" by Shizhao Lu and Evan MacBride. This project was prepared for the CHEG/CISC 867 course at the University of Delaware in Spring 2022. Our project mentor was Dr. Houk Jang of Brookhaven National Laboratory.

## Project Overview
Microscopy imaging is an important part of soft materials engineering. It can provide insight into the relationships between materials’ structures and their properties. Microscopy images must be in focus to provide high quality information. A microscope should focus quickly and with fine-grained control, but traditional, iterative autofocus methods are time consuming. This project investigated machine learning methods in an attempt to improve autofocus performance to support soft materials engineering. Given a set of images labeled with their distances to the focal plane, we trained machine learning models to predict the distance to the focal plane of new, out-of-focus test images. Rather than developing new machine learning algorithms, the emphasis of our work was on preprocessing and data cleaning through selection of microscopy images.

## How to use this repository
For a walkthrough of our machine learning workflow, open [Walkthrough.ipynb](https://github.com/evanmacbride/microscope-autofocus/blob/main/notebooks/Walkthrough.ipynb) (found in the [notebooks folder](https://github.com/evanmacbride/microscope-autofocus/tree/main/notebooks)) and click “Open in Colab.” Follow the directions given in the notebook. Additionally, all notebooks used to create the project, refine preprocessing methods, take performance measurements, etc. are available in the [notebook archive](https://github.com/evanmacbride/microscope-autofocus/tree/main/notebooks/archive). Each of these notebooks can also easily be launched in Google Colab by clicking the "Open in Colab" badge. Change to the new Google Colab and select Runtime > Run all to run the notebook.

You will need some microscopy images to train and test the models. Sample microscopy images provided by Dr. Houk Jang are available in the [sample_data](https://github.com/evanmacbride/microscope-autofocus/tree/main/sample_data) folder. To easily use the sample_data images in the Walkthrough notebook from within Google Colab, you can copy the images to a directory in your Google Drive. The results shown in the Walkthrough notebook were generated with images from the “level 1” folder in sample_data.
