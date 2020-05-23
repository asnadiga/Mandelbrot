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


class Application(tk.Frame):
    
    def __init__(self, master, minX, minY, maxX, maxY, RES, MAXITERATIONS):
        
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.fractal = Mandelbrot(minX, minY, maxX, maxY, RES, MAXITERATIONS)
        
        self.imgFrame = tk.Frame(self, bg = "green", height = int((maxY-minY)/(maxX-minX)*RES), width = RES)
        self.img = None
        
        
        self.ctrlFrame = tk.Frame(self, height = 40, width = RES)
        self.zoomInButton = tk.Button(self.ctrlFrame,text = "zoom in", command = lambda : self.zoom(2))
        self.zoomOutButton = tk.Button(self.ctrlFrame,text = "zoom out", command = lambda : self.zoom(0.5))

        self.curMouseX = 0
        self.curMouseY = 0
        self.singleClick = False
        
        self.iterLab = tk.Label(master = self.ctrlFrame, text = "Max Number of Iterations:")
        self.iterEnt = tk.Entry(master = self.ctrlFrame)
        self.iterBut = tk.Button(master = self.ctrlFrame, text = "Apply", command = self.update_iterations)
        self.bs = tk.Frame(self)

        self.display()
        
    
        
    def display(self):
        self.master.title("Mandelbrot")
        self.pack(fill="both", expand=1)
        
        self.imgFrame.pack()

        self.ctrlFrame.pack()
        self.iterLab.pack(side="left")
        self.iterEnt.pack(side="left")
        self.iterBut.pack(side="left")
        
        dispArray = self.fractal.iterations()
        at = np.transpose(dispArray)
        pic =  ImageTk.PhotoImage(Image.fromarray((255*(self.fractal.MAXITERATIONS-at)/self.fractal.MAXITERATIONS)))
        if self.img == None:
            self.img = tk.Label(image = pic, master = self.imgFrame)
            self.img.image = pic
            self.img.bind("<Double-Button-1>", lambda event : self.mouse_event_handler(event,"d"))
            self.img.bind("<Button-3>", lambda event : self.zoom(0.5, event.x, event.y))
            self.img.bind("<Button-1>", lambda event : self.mouse_event_handler(event, "b1d"))
            self.img.bind("<ButtonRelease-1>", lambda event : self.mouse_event_handler(event,"b1u"))

        else:
            self.img.config(image = pic)
            self.img.image = pic
        self.img.pack(anchor="nw", fill="both", expand=1)


        
    
    def translate(self, event):
        if self.singleClick:
            cur = self.fractal.curArray[self.curMouseX][self.curMouseY]
            new = self.fractal.curArray[event.x][event.y]
            self.fractal.translate(cur.real-new.real, cur.imag-new.imag)
            self.display()
    
    def zoom(self, zoomAmt, x, y):
        zoomCenter = self.fractal.curArray[x][y]
        self.fractal.zoom(zoomAmt, zoomCenter)
        self.display()
        
    def update_mouse(self, event):
        if self.singleClick:
            self.curMouseX = event.x
            self.curMouseY = event.y
            print("click down: ",self.fractal.curArray[self.curMouseX][self.curMouseY])
    
    def test(self, event):
        print("click up:  ", self.fractal.curArray[event.x][event.y])

    
    def update_iterations(self):
        self.fractal.MAXITERATIONS = int(self.iterEnt.get())
        self.display()
    
    def mouse_event_handler(self,event,evT):
        print(evT)        
        if evT=="b1d":
            print("single click")
            self.singleClick = True
            self.bs.after(200,lambda : self.update_mouse(event))
        if evT=="d":
            self.singleClick = False
            self.zoom(2,event.x,event.y)
        if evT == "b1u":
            self.bs.after(200, lambda : self.translate(event))
            
           
def main():
    root = tk.Tk()
    tester = Application(root,-2.2, -1.2, 1.2, 1.2, 600, 50)
    root.mainloop()
    #tester.translate(-0.75,-0.75)
    #tester.display()
    #tester.zoom(0.5)
    #tester.display()
    

    
main()
        