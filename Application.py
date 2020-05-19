'''
Created on May 19, 2020

@author: Aniruddha Nadiga
'''
from Mandelbrot import Mandelbrot
import numpy as np
import numexpr as ne
import time
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk


class Application:
    
    def __init__(self, minX, minY, maxX, maxY, RES, MAXITERATIONS):
        self.fractal = Mandelbrot(minX, minY, maxX, maxY, RES, MAXITERATIONS)
        
        
        self.window = tk.Tk()
        self.imgFrame = tk.Frame()
        self.ctrlFrame = tk.Frame()
        self.canvas = tk.Canvas(self.imgFrame, width = int(RES), height = int(((maxY-minY)/(maxX-minX))*RES)+40)
        
        
        
        
        
    def display(self):
        dispArray = self.fractal.iterations()
        at = np.transpose(dispArray)
        img =  ImageTk.PhotoImage(image=Image.fromarray(((255/self.fractal.MAXITERATIONS)*at)), master = self.imgFrame)
        self.canvas.create_image(0,0, anchor="nw", image=img)
        self.canvas.pack()
        self.imgFrame.pack()
        self.window.mainloop()
        
        #plt.imshow(at, cmap='hot')
        #plt.show()
    
    
    def translate(self, transX, transY):
        self.fractal.translate(transX, transY)
        
    
    def zoom(self, zoomAmt):
        self.fractal.zoom(zoomAmt)
        
def main():
    tester = Application(-2.2, -1.2, 1.2, 1.2, 600, 50)
    tester.display()
    #tester.translate(-0.75,-0.75)
    #tester.display()
    #tester.zoom(0.5)
    #tester.display()
    

    
main()
        