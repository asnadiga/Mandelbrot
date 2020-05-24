'''
Created on May 19, 2020

@author: Aniruddha Nadiga
'''
from Mandelbrot import Mandelbrot
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import time
from PIL.ImageTk import PhotoImage


class Application(tk.Frame):
    
    def __init__(self, master, minX = -2.2, minY = -1.2, maxX = 1.2, maxY = 1.2, RES = 600, MAXITERATIONS=50):
        
        tk.Frame.__init__(self, master)
        self.master = master
        
        self.fractal = Mandelbrot(minX, minY, maxX, maxY, RES, MAXITERATIONS)
        
        self.imgFrame = tk.Frame(self, bg = "green", height = int((maxY-minY)/(maxX-minX)*RES), width = RES)
        self.img = None
        
        
        self.ctrlFrame = tk.Frame(self, height = 40, width = RES)
        self.zoomInButton = tk.Button(self.ctrlFrame,text = "zoom in", command = lambda : self.zoom(2))
        self.zoomOutButton = tk.Button(self.ctrlFrame,text = "zoom out", command = lambda : self.zoom(0.5))
        self.saveButton = tk.Button(self.ctrlFrame, text = "save", command = self.save_popup)

        self.curMouseX = 0
        self.curMouseY = 0
        self.singleClick = False
        
        self.iterLab = tk.Label(master = self.ctrlFrame, text = "Max Number of Iterations:")
        self.iterEnt = tk.Entry(master = self.ctrlFrame)
        self.iterBut = tk.Button(master = self.ctrlFrame, text = "Apply", command = self.update_iterations)
        self.bs = tk.Frame(self)

        self.colorAlg = tk.StringVar(self)
        self.colorAlg.set("Select Coloring Algorithm") 
        self.colorAlg.trace_add('write', lambda x,y,z: self.display())
        self.colorOption = tk.OptionMenu(self.ctrlFrame, self.colorAlg, "Normal", "Smoothed", "Glow")

        self.display()
        
    
        
    def display(self):
        self.master.title("Mandelbrot")
        self.pack(fill="both", expand=0)
        
        self.imgFrame.pack(expand=0)

        self.ctrlFrame.pack(expand=0)
        self.iterLab.pack(side="left")
        self.iterEnt.pack(side="left")
        self.iterBut.pack(side="left")
        self.colorOption.pack(side="left")
        self.saveButton.pack(side="right")
        
        pic = ImageTk.PhotoImage(self.get_image(self.colorAlg.get()))
        
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
        self.img.pack(anchor="nw", fill="both", expand=0)
        

    
    def get_image(self, algorithm, fractal = None):
        if fractal == None:
            fractal = self.fractal
        if ((algorithm == "Smoothed") or (algorithm == "Select Coloring Algorithm")):
            dispArray = fractal.iterations()
            at = np.transpose(dispArray)
            pic =  Image.fromarray((225*(at+1-np.log(np.log2(at+0.1))))/fractal.MAXITERATIONS)
            return pic
        if algorithm == "Normal":
            dispArray = fractal.iterations()
            at = np.transpose(dispArray)
            pic =  Image.fromarray((225*at/fractal.MAXITERATIONS))
            return pic

        if algorithm == "Glow":
            dispArray = fractal.glow_iterations()
            at = np.transpose(dispArray)
            pic =  Image.fromarray((225*at/2))
            return pic

    
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
    
    
    def update_iterations(self):
        self.fractal.MAXITERATIONS = int(self.iterEnt.get())
        self.display()
    
    def mouse_event_handler(self,event,evT):
        if evT=="b1d":
            self.singleClick = True
            self.bs.after(200,lambda : self.update_mouse(event))
        if evT=="d":
            self.singleClick = False
            self.zoom(2,event.x,event.y)
        if evT == "b1u":
            self.bs.after(200, lambda : self.translate(event))
            
           
    def save_popup(self):
        popup = tk.Tk()
        popup.title("Save")
        
        iterLab = tk.Label(master = popup, text = "Max Number of Iterations: ")
        iterLab.grid(row=0, column=0)
        iterEntry = tk.Entry(master = popup)
        iterEntry.grid(row=0, column=1)
        
        resLab = tk.Label(master = popup, text = "Resolution (number of pixels in x direction): ")
        resLab.grid(row = 1, column = 0)
        resEntry = tk.Entry(master = popup)
        resEntry.grid(row = 1, column = 1)
        
        extLab = tk.Label(master = popup, text = "<name>.<extension>")
        extLab.grid(row=2, column = 0)
        extEntry = tk.Entry(master = popup)
        extEntry.grid(row = 2, column = 1)
        
        algLab = tk.Label(master = popup, text = "Coloring Algorithm")
        algLab.grid(row=3, column = 0)
        alg = tk.StringVar(popup)
        alg.set("Normal")
        algChoice = tk.OptionMenu(popup, alg, "Normal", "Smoothed", "Glow")
        algChoice.grid(row=3, column = 1)
        
        
        saveBut = tk.Button(master = popup, text = "Save", 
                            command = lambda : self.save(popup, alg.get(), int(iterEntry.get()), int(resEntry.get()), extEntry.get()))
        saveBut.grid(row=4, column = 1)
        popup.mainloop()
    
    
    def save(self, popup, alg, iter, res, name):
        saveFrac = Mandelbrot(self.fractal.minX, self.fractal.minY, self.fractal.maxX, self.fractal.maxY, 
                              res, iter)
        pic = self.get_image(alg, saveFrac)
        pic = pic.convert('RGB')
        pic.save(name)
        popup.destroy()
def main():
    root = tk.Tk()
    tester = Application(root,0,0,16,9,1000)
    root.mainloop()

if __name__ == "__main__": 
    main()
        