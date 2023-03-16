#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 22 May 2019

@author: M Roux
"""

#%%
import matplotlib.pyplot as plt
from skimage import data, filters
from skimage import io as skio
from scipy import ndimage
import mrlab as mr

# POUR LA MORPHO
import skimage.morphology as morpho  
import skimage.feature as skf
from scipy import ndimage as ndi
import numpy as np

#%%
def tophat(im,rayon):
    se=morpho.square(rayon)
    ero=morpho.erosion(im,se)
    dil=morpho.dilation(ero,se)
    tophat=im-dil
    return tophat
    
fig, ax = plt.subplots(nrows=2, ncols=3)

ima = skio.imread('spot.tif');
rayon=7
top=tophat(ima,rayon)

low = 1
high = 7


lowt = (top > low).astype(int)
hight = (top > high).astype(int)
hyst = filters.apply_hysteresis_threshold(top, low, high)


ax[0, 0].imshow(ima, cmap='gray')
ax[0, 0].set_title('Original image')

ax[0, 1].imshow(top, cmap='magma')
ax[0, 1].set_title('Tophat filter')

ax[1, 0].imshow(lowt, cmap='magma')
ax[1, 0].set_title('Low threshold')

ax[1, 1].imshow(hight, cmap='magma')
ax[1, 1].set_title('High threshold')

ax[0, 2].imshow(hyst, cmap='magma')
ax[0, 2].set_title('Hysteresis')

ax[1, 2].imshow(hight + hyst, cmap='magma')
ax[1, 2].set_title('High + Hysteresis')

skio.imsave('out_hyst.tif', hight+hyst)


for a in ax.ravel():
    a.axis('off')

plt.tight_layout()

plt.show()

# %% Cumul avec la méthode de Deriche


alpha=0.2
seuilnorme=4
ima=skio.imread('out_hyst.tif')



gradx=mr.dericheGradX(mr.dericheSmoothY(ima,alpha),alpha)
grady=mr.dericheGradY(mr.dericheSmoothX(ima,alpha),alpha)

contours=np.uint8(mr.maximaDirectionGradient(gradx,grady))

plt.figure('Contours')
plt.imshow(255*contours)
norme=np.sqrt(gradx*gradx+grady*grady)

valcontours=(norme>seuilnorme)*contours
      
plt.figure('Contours normés')
plt.axis("off")
plt.imshow(255*valcontours)
 