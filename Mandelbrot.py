'''
Created on May 15, 2020

@author: Aniruddha Nadiga
'''
import numpy as np
import numexpr as ne
from _tracemalloc import start
import time

class Mandelbrot:


    def __init__(self, minX, minY, maxX, maxY, RES, MAXITERATIONS):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        self.RES = RES/(maxX-minX)
        self.MAXITERATIONS = MAXITERATIONS
        
        self.curArray = self.make_array()


    def make_array(self):
        a  = np.array([[complex(i/self.RES,j/self.RES) for j in range(int(self.maxY*self.RES), int(self.minY*self.RES),-1)] for i in range(int(self.minX*self.RES),int(self.maxX*self.RES),1)])
        return a
    
    
    def iterations(self):
        
        a = self.curArray
        z = a
        numIter = np.ones(self.curArray.shape)
        
        for i in range(self.MAXITERATIONS):
            b = ne.evaluate("abs(z).real<2").astype(int)
            numIter = numIter + b    
            z = np.where(b==1, ne.evaluate("z*z+a"), z) 
        
        return numIter
    
    
    def glow_iterations(self):
        a = self.curArray
        z = a
        minNorm = abs(z)
        
        for i in range(self.MAXITERATIONS):
            b = ne.evaluate("abs(z).real<2").astype(int)    
            z = np.where(b==1, ne.evaluate("z*z+a"), z) 
            minNorm = np.where(b==1, np.where(abs(z)<minNorm, abs(z), minNorm), minNorm)
        
        return minNorm
    
  
    def translate(self, transX, transY):
        self.minX = self.minX+transX
        self.minY = self.minY+transY
        self.maxX = self.maxX+transX
        self.maxY = self.maxY+transY
        
        trans = complex(transX,transY)
        self.curArray = self.curArray + trans
        
        
    def zoom(self,zoomAmt, zoomCenter):
        self.curArray = ((self.curArray-zoomCenter)*(1/zoomAmt))+zoomCenter
        self.minX = self.curArray[0][0].real
        self.maxX = self.curArray[self.curArray.shape[0]-1][self.curArray.shape[1]-1].real
        self.minY = self.curArray[self.curArray.shape[0]-1][self.curArray.shape[1]-1].imag
        self.maxY = self.curArray[0][0].imag
    
    
