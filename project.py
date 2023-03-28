from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser, messagebox
from tkinter.filedialog import asksaveasfilename
from PIL import ImageGrab, ImageTk 
import webbrowser

color = 'white'
i = 1
trace=0

class Paint:

    def __init__(self, root):
        self.root = root
        self.root.title('Lets Paint')
        self.root.geometry('1000x750')
        self.root.configure(background='white')
        self.root.resizable(True, True)

        self.pen_color = 'black'

        self.color_frame = LabelFrame(
            self.root,
            font=('arial', 15, 'bold'),
            bd=5,
            relief=GROOVE,
            bg='white',
            )
        self.color_frame.place(x=5, y=5, width=88, height=330)

        Colors = [
            #1
            '#B8255F',
            '#DB4035',
            '#FF9933',
            '#FAD000',
            '#AFB83B',
            '#7ECC49',
            '#299438',
            '#6ACCBC',
            '#158FAD',
            '#14AAF5',
            '#85200C',
            '#FFFF00',

            #2
            '#96C3EB',
            '#4073FF',
            '#884DFF',
            '#AF38EB',
            '#EB96EB',
            '#E05194',
            '#FF8D85',
            '#808080',
            '#B8B8B8',
            '#CCAC93',
            '#783F04',
            '#000000'
            ]
        i = j = 0
        for color in Colors:

            Button(
                self.color_frame,
                bg=color,
                command=lambda col=color: self.select_color(col),
                width=4,
                bd=2,
                relief=RIDGE,
                ).grid(row=i, column=j)
            i += 1
            if i == 12: 
                i = 0
                j = 1

        self.erase_button = Button(
            self.root,
            text='Eraser',
            bd=4,
            relief=RIDGE,
            width=8,
            command=self.eraser,
            bg='white',
            )
        self.erase_button.place(x=100, y=5)

        self.clear_sreen_button = Button(
            self.root,
            text='Clear',
            bd=4,
            relief=RIDGE,
            width=8,
            command=lambda : self.canvas.delete('all'),
            bg='white',
            )
        self.clear_sreen_button.place(x=180, y=5)

        self.save_button = Button(
            self.root,
            text='Save',
            bd=4,
            relief=RIDGE,
            width=8,
            command=self.save_paint,
            bg='white',
            )
        self.save_button.place(x=260, y=5)

        self.canvas_color_button = Button(
            self.root,
            text='Canvas',
            bd=4,
            relief=RIDGE,
            width=8,
            command=self.canvas_color,
            bg='white',
            )
        self.canvas_color_button.place(x=340, y=5)

        self.shape_rectangle = Button(
            self.root,
            text='Rectangle',
            bd=4,
            relief=RIDGE,
            width=8,
            command=self.rectangle,
            bg='white',
        )
        self.shape_rectangle.place(x=420, y=5)

        self.shape_oval = Button(
            self.root,
            text='Oval',
            bd=4,
            relief=RIDGE,
            width=8,
            command=self.oval,
            bg='white',
        )
        self.shape_oval.place(x=500, y=5)

        self.shape_line = Button(
            self.root,
            text='Line',
            bd=4,
            relief=RIDGE,
            width=8,
            command=self.line,
            bg='white',
        )
        self.shape_line.place(x=580, y=5)

        self.lnk=Button(
            self.root,
            text='Developed By Jasleen Kaur',
            bd=4,
            relief=FLAT,
            width=30,
            command= self.openlink,
            bg='beige',
        )
        self.lnk.place(x=700,y=5)

        self.pen_size_scale_frame = LabelFrame(
            self.root,
            text='ADJUST SIZE',
            bd=5,
            relief=GROOVE,
            bg='white',
            font=('arial', 8, 'bold'),
            )
        self.pen_size_scale_frame.place(x=5, y=350, height=210, width=88)

        self.pen_size = Scale(
            self.pen_size_scale_frame,
            orient='vertical',
            from_=50,
            to=0,
            command=None,
            length=170,
            )
        self.pen_size.set(10)
        self.pen_size.grid(row=0, column=1, padx=25)

        self.canvas = Canvas(
            self.root,
            bg='white',
            bd=5,
            relief='groove',
            height=500,
            width=1000,
            )
        self.canvas.place(x=100, y=50, anchor="nw")

        self.canvas.bind('<B1-Motion>', self.paint)
        self.old_x = None
        self.old_y = None
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, event):
        global pen_color
        if self.old_x and self.old_y:

            # self.canvas.config(cursor='plus')
			
            self.canvas.create_line(
                self.old_x,
                self.old_y,
                event.x,
                event.y,
                width=self.pen_size.get(),
                fill=self.pen_color,
                capstyle=ROUND,
                smooth=TRUE,
                splinesteps=36,
                )

        self.old_x = event.x
        self.old_y = event.y

    def reset(self,*args):
        self.old_x = None
        self.old_y = None

    def select_color(self, col):
        global i
        i = 1
        self.pen_color = col

    def eraser(self):
        global color
        global i
        self.pen_color = color
        i = 0

    def canvas_color(self):
        global color
        color = colorchooser.askcolor()
        color = color[1]
        self.canvas.config(background=color)

    def rectangle(self):
        self.canvas.bind('<ButtonPress-3>', self.onStart) 
        self.canvas.bind('<B3-Motion>',     self.onGrow)
        self.canvas.bind('<Double-1>',      self.onClear)   
        self.drawn  = None
        self.kinds = [self.canvas.create_rectangle]

    def oval(self):
        self.canvas.bind('<ButtonPress-3>', self.onStart) 
        self.canvas.bind('<B3-Motion>',     self.onGrow)
        self.canvas.bind('<Double-1>',      self.onClear)   
        self.drawn  = None
        self.kinds = [self.canvas.create_oval]

    def line(self):
        self.canvas.bind('<ButtonPress-3>', self.onStart) 
        self.canvas.bind('<B3-Motion>',     self.onGrow)
        self.canvas.bind('<Double-1>',      self.onClear)   
        self.drawn  = None
        self.kinds = [self.canvas.create_line]

    def openlink(self):
        webbrowser.open_new(r"https://www.linkedin.com/in/jasleen-kaur-65818a205")



    def onStart(self, event):
        self.shape = self.kinds[0]
        self.kinds = self.kinds[1:]
        self.start = event
        self.drawn = None
    def onGrow(self, event):                         
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
        if trace: print(objectId)
        self.drawn = objectId
    def onClear(self):
        self.canvas.bind('<ButtonPress-1>', self.paint)
                   
    def onMove(self, event):
        if self.drawn:                               
            if trace: print(self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event

    def save_paint(self):
        try:
            self.canvas.update()
            filename = asksaveasfilename(defaultextension='.jpg')
            print(filename)
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            print(x) 
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            print(y)
            x1 = x + self.canvas.winfo_width()
            print(x1)
            y1 = y + self.canvas.winfo_height()
            print(y1)

            ImageGrab.grab().crop((x, y, x1, y1)).save(filename)
            messagebox.showinfo('paint says ', 'image is saved as '+ str(filename))
        except:

            pass


if __name__ == '__main__':
    root = Tk()
    Paint(root)
    root.mainloop()
