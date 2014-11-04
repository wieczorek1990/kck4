'''
Created on 11-11-2011
Wizualizacja danych z tabletu
@author: luke
'''
import pyx
from pyx.style import *
import pprint
import Tkinter, Tkconstants, tkFileDialog
import Image, ImageDraw, ImageTk

import DataHTD
import colors
 
class App(Tkinter.Frame):
    #Okno i jego obwodka
    width = 800
    height = 600
    scale = 0.9
    xpad = (1.0 - scale) * width / 2
    ypad = (1.0 - scale) * height / 2
    l = []
    def __init__(self, parent):
        self.parent = parent
        
        menu = Tkinter.Menu(parent)
        parent.config(menu=menu)
        filemenu = Tkinter.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load", command=self.load)
        filemenu.add_command(label="Save", command=self.save)
        
        self.status = Tkinter.Label(parent, text="", bd=1, relief=Tkconstants.SUNKEN, anchor=Tkconstants.W)
        self.status.pack(side=Tkconstants.BOTTOM, fill=Tkconstants.X)
        
        image = Image.new("RGB", (self.width, self.height), "white")
        tkimage = ImageTk.PhotoImage(image)
        label = Tkinter.Label(parent, image=tkimage)
        label.image = tkimage
        label.pack()
        self.label = label
 
    def set_status(self, string):
        self.status.config(text=string)
        self.status.update_idletasks()
        
    def load(self):
        filename = tkFileDialog.askopenfilename(filetypes=[("HTD", ".htd")])
        self.set_status("Loading...")
        if not filename:
            return
        htd = DataHTD.DataHTD(filename)
        
        pp = pprint.PrettyPrinter()
        #pp.pprint(htd.packages)
        
        minx = maxx = htd.packages[0][1]
        miny = maxy = htd.packages[0][2]
        #minc = maxc = htd.packages[0][3]
        for i in range(htd.noPackage - 1):
            if htd.packages[i][1] < minx:
                minx = htd.packages[i][1]
            elif htd.packages[i][1] > maxx:
                maxx = htd.packages[i][1]
            if htd.packages[i][2] < miny:
                miny = htd.packages[i][2]
            elif htd.packages[i][2] > maxy:
                maxy = htd.packages[i][2]
            '''if htd.packages[i][3] < minc:
                minc = htd.packages[i][3]
            elif htd.packages[i][3] > maxc:
                maxc = htd.packages[i][3]'''
        scalex = float(maxx - minx) / float(self.width)
        scaley = float(maxy - miny) / float(self.height)
        #scalec = float(maxc - minc) / float(255)
        #print minx, maxx, miny, maxy, minc, maxc
        #print scalex, scaley, scalec
        for i in range(htd.noPackage):
            #self.l.append([(htd.packages[i][1] - minx) / scalex, (htd.packages[i][2] - miny) / scaley, (htd.packages[i][3] - minc) / scalec])
            self.l.append([(htd.packages[i][1] - minx) / scalex, (htd.packages[i][2] - miny) / scaley, int(float(htd.packages[i][3] * 255) / 1000.0)])
        #pprint.pprint(self.l)

        #Rysowanie
        image = Image.new("RGB", (self.width, self.height), "white")
        draw = ImageDraw.Draw(image)
        for i in range(len(self.l) - 1):
            c = colors.get_color((self.l[i][2] + self.l[i + 1][2]) / 2.0)
            draw.line((self.scale * self.l[i][0] + self.xpad, self.scale * self.l[i][1] + self.ypad, self.scale * self.l[i + 1][0] + self.xpad, self.scale * self.l[i + 1][1] + self.ypad), fill=c)
        tkimage = ImageTk.PhotoImage(image)
        self.label.configure(image=tkimage)
        self.label.image = tkimage
        self.set_status("Loading complete.")
        
    def save(self):
        #Zapisz do pliku pdf
        filename = tkFileDialog.asksaveasfilename(filetypes=[("PDF", ".pdf")])
        self.set_status("Saving...")
        if not filename:
            return
        can = pyx.canvas.canvas()
        for i in range(len(self.l) - 1):
            c0 = colors.get_color((self.l[i][2] + self.l[i + 1][2]) / 2.0)
            c = pyx.color.rgb(float(c0[0] / 255), float(c0[1] / 255), float(c0[2] / 255))
            can.stroke(pyx.path.line(self.l[i][0], self.l[i][1], self.l[i + 1][0], self.l[i + 1][1]),
                          [linestyle.solid, linewidth(0.5), c])
        can.writePDFfile(filename)
        self.set_status("Saving complete.")
        
#Okno aplikacji
root = Tkinter.Tk()
root.title("Tablet")
app = App(root)
root.mainloop()
