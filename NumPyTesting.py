'''
The goal is to learn about how numpy can speed up operations that I will need in the project

Created on May 15, 2020

@author: Aniruddha Nadiga
'''

import numpy as np
import time


l = np.array([['a','b'],['1','2']])

print(l)
print()
print(np.append(l,np.flip(l,1)))
