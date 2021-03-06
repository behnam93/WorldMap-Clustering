!pip install rasterio

import matplotlib.pyplot as plt
import numpy as np
from urllib import request
import os
from zipfile import ZipFile
import rasterio
from rasterio.plot import show
from sklearn.cluster import KMeans

filename , _ = request.urlretrieve('https://naciscdn.org/naturalearth/10m/raster/GRAY_HR_SR_OB.zip','GRAY_HR_SR_OB.zip')

with ZipFile(filename, 'r') as zip:
  zip.printdir()
  print('Extracting all the files now...')
  zip.extractall('drive/MyDrive/Data/NaturalEarth')
  print('done!')

image = rasterio.open('drive/MyDrive/Data/NaturalEarth/GRAY_HR_SR_OB.tif')

image.meta

image_arr = image.read()

plt.figure(figsize=(20,18))
show(image, cmap='gray')
plt.show()

plt.imshow(image_arr[0][:9000,9000:][2500:7800,500:6200])

hormoz_image = image_arr[0][:9000,9000:][2500:7800,500:6200][:2200,:]

hormoz_image.shape

X = []
for i in range(0, hormoz_image.shape[0]):
  for j in range(0, hormoz_image.shape[1]):
    if i == 0 or j == 0 or i == hormoz_image.shape[0] - 1 or j == hormoz_image.shape[1] - 1:
      p = abs(hormoz_image[i][j])
      X.append([
                p,p,p,p,p,p,p,p,p
      ])
    else:
      f1 = abs(hormoz_image[i][j])
      f2 = abs(hormoz_image[i -1][j])
      f3 = abs(hormoz_image[i + 1][j])
      f4 = abs(hormoz_image[i][j - 1])
      f5 = abs(hormoz_image[i][j + 1])
      f6 = abs(hormoz_image[i - 1][j - 1])
      f7 = abs(hormoz_image[i + 1][j - 1])
      f8 = abs(hormoz_image[i - 1][j + 1])
      f9 = abs(hormoz_image[i + 1][j + 1])
      X.append([
                f1,f2,f3,f4,f5,f6,f7,f8,f9
      ])

hormoz_cls = np.empty(np.shape(hormoz_image))

hormoz_flattern = hormoz_image.reshape(-1)

from sklearn.feature_extraction import image

cm = image.img_to_graph(hormoz_image)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=2, init='k-means++')
kmeans.fit(X)

labels = kmeans.labels_

np.unique(labels, return_counts=True)

labels_im = np.full(hormoz_image.shape, -1.)

hormoz_cls = hormoz_image.astype(bool)
labels_im[hormoz_cls] = labels

plt.imshow(image_arr[0][:9000,9000:][2500:7800,500:6200][:2200,:])

plt.matshow(labels_im)
