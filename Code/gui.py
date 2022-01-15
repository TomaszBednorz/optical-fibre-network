from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from data_structures import *
from SA import *
import matplotlib.pyplot as plt
import sys
from tkinter import filedialog as fd
import time
from tkinter.messagebox import showinfo

# root = Tk()
# root.title("Simulated Annealing")
# root.geometry('900x600')

# # label = Label(root, text='Hello World',font=("Arial Bold", 50))
# # label.pack()
# # label.grid(column=0, row=0)

# txt = Entry(root,width=10)

# txt.grid(column=1, row=0)

# selected = IntVar()
# rad1 = Radiobutton(root,text='First', value=1,variable=selected)
# rad2 = Radiobutton(root,text='Second', value=2,variable=selected)
# rad3 = Radiobutton(root,text='Third', value=3,variable=selected)

# def clicked():
#    print(selected.get())

# def clicked_1():
#     messagebox.showinfo('Message title', 'Message content')

# btn = Button(root, text="Click Me", command=clicked_1)
# btn.grid(column=50, row=50)

# rad1.grid(column=0, row=0)
# rad2.grid(column=1, row=0)
# rad3.grid(column=2, row=0)

# bar = Progressbar(root, length=200, style='black.Horizontal.TProgressbar')
# bar['value'] = 70
# bar.place(x=300,y = 450)

# root.mainloop()

from tkinter import *
class MyWindow:
    def __init__(self, win):
        self.lbl0=Label(win, text='Schemat wyżarzania:')
        self.lbl1=Label(win, text='Temperatura:')
        self.lbl2=Label(win, text='Liczba iteracji:')
        self.lbl3=Label(win, text='Liczba iteracji w jednej temperaturze:')
        self.lbl4=Label(win, text='Alfa:')
        self.t1=Entry(bd=3)
        self.t2=Entry(bd=3)
        self.t3=Entry(bd=3)
        self.t4=Entry(bd=3)
        self.btn1 = Button(win, text='Add')
        self.btn2=Button(win, text='Subtract')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        self.lbl3.place(x=100, y=150)
        self.t3.place(x=200, y=150)
        self.lbl4.place(x=100, y=200)
        self.t4.place(x=200, y=200)
        self.lbl0.place(x=100, y=0)
        self.cooling = StringVar()
        self.anneling_chose = Combobox(window, width = 27, textvariable = self.cooling)
        # Adding combobox drop down list
        self.anneling_chose['values'] = ('linear additive', 
                                'linear multiplicative',
                                'quadratic additive',
                                'exponential multiplicative',
                                'logarithmical multiplicative',
                                'None'
        )
        self.anneling_chose.place(x=200, y=0)
        self.anneling_chose.current()
        print(self.anneling_chose)
        self.b1=Button(win, text='START', command=self.run_alghorithm)
        # self.b2=Button(win, text='Subtract')
        # self.b2.bind('<Button-1>', self.sub)
        self.b1.place(x=100, y=250)
        # self.b2.place(x=200, y=150)
        # open button
        self.button_buildings = Button(win,width = 27, text='Wybierz plik z budynkami', command=self.select_file_buildings)
        self.button_buildings.pack(expand=True)
        self.button_buildings.place(x=400, y=50)
        self.button_poles = Button(win,width = 27, text='Wybierz plik ze słupami', command=self.select_file_poles)
        self.button_poles.pack(expand=True)
        self.button_poles.place(x=400, y=100)

        self.filename_buildings = 'Data/buildings.txt'
        self.filename_poles = 'Data/poles.txt'

    def select_file_buildings(self):
        filetypes = (('text files', '*.txt'),('All files', '*.*'))
        filename = fd.askopenfilename(title='Open a file',initialdir='Data/',filetypes=filetypes)
        self.filename_buildings = filename
        showinfo(title='Wybrany plik',message=filename)

    def select_file_poles(self):
        filetypes = (('text files', '*.txt'),('All files', '*.*'))
        filename = fd.askopenfilename(title='Open a file',initialdir='Data/',filetypes=filetypes)
        self.filename_poles = filename
        showinfo(title='Wybrany plik',message=filename)

    def run_alghorithm(self):
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        num3=int(self.t3.get())
        num4=float(self.t4.get())
        network = OpticalFibreNetwork()
        network.add_starting_point(50.16429619810853, 19.626773362067187)
        print(self.filename_buildings)
        network.add_buildings_from_txt(self.filename_buildings)
        network.add_poles_from_txt(self.filename_poles)

        sa_param = SA_parameters()
        sa_param.buildings = True
        sa_param.poles = True
        sa_param.devices = True
        sa_param.set_temperature(num1) # 100
        sa_param.set_iterations(num2,num3) #Change to 100, 10
        sa_param.set_alpha(num4) #0.98
        sa_param.set_cooling_schedule(self.cooling.get())   # Choose from: linear additive, linear multiplicative, quadratic additive, 
                                                        # exponential multiplicative, logarithmical multiplicative or None if you want constant temperature

        sa = SimulatedAnnealing(network,sa_param)
        sa.run_alghoritm()
        sa.best_solution.visualization(True,False) 
        print("Objective function cost: {} zł".format(sa.best_solution.cost))
        simple_sol = sa.best_solution.get_simple_solution()
        print("\nCost: {} zł".format(simple_sol[2]))
        print("\nOptical fibre network:")
        for key, value in simple_sol[0].items():
            print("{} : {}".format(key, value))
        print("\nDevices:")
        for key, value in simple_sol[1].items():
            print("{} : {}".format(key, value))
        history = sa.get_objective_function_history()
        print(" ")
        print("Buildings updates: {}".format(sa.realizations[0]))
        print("Poles updates: {}".format(sa.realizations[1]))
        print("Devices updates: {}".format(sa.realizations[2]))
        iterations = sa_param.max_iterations * sa_param.max_subiterations
        print(" ")
        print("Objective function cost: {} zł".format(sa.best_solution.cost))
        print("Worse cost (not accepted): {}  {:.3}%".format(sa.quality_changes[0], 100*sa.quality_changes[0]/ iterations))
        print("Worse cost (accepted): {}  {:.3}%".format(sa.quality_changes[1], 100*sa.quality_changes[1]/ iterations))
        print("Better cost: {}  {:.3}%".format(sa.quality_changes[2], 100*sa.quality_changes[2]/ iterations))
        print(" ")
        # print("Worse cost (not accepted): {}".format(sa.quality_changes_it['worse_not_acepted']))
        # print("Worse cost (accepted): {}".format(sa.quality_changes_it['worse_accepted']))
        # print("Better cost: {}".format(sa.quality_changes_it['better']))
        # network.save_buildings_to_txt('buildings.txt')
        # network.save_poles_to_txt('poles.txt')
        plt.figure(1)
        plt.plot(history)
        plt.grid()
        plt.xlabel("Iteration")
        plt.ylabel("Cost")
        plt.title("Objective function cost in time")
        temperature = sa.get_temperature_history()
        plt.figure(2)
        plt.plot(temperature)
        plt.grid()
        plt.xlabel("Iteration")
        plt.ylabel("Temperature")
        plt.title("Temperature in time")
        plt.show()
            # self.t3.insert(END, str(result))
    # def sub(self, event):
    #     self.t3.delete(0, 'end')
    #     num1=int(self.t1.get())
    #     num2=int(self.t2.get())
    #     result=num1-num2
    #     self.t3.insert(END, str(result))

window=Tk()
mywin=MyWindow(window)
window.title('Simulated annealing')
window.geometry("700x500+10+10")
window.mainloop()