from Tkinter import *
import tkFileDialog
import tkMessageBox
import net_parser
import elements
import matplotlib.pyplot as plt

class App:
    def __init__(self, master):
        self.file_input = open('C:\circuits\diode_tran.cir','r')
        texts = Frame(master)
        texts.pack(side=RIGHT)
        self.netlist = Text(texts, height=30, width=40)
        self.res_print = Text(texts, height=30, width=40)
        self.netlist.pack(side=LEFT)
        self.res_print.pack(side=LEFT)

        buttons = Frame(master)
        buttons.pack(side=TOP)
        self.choose_net = Button(buttons, text="Choose Netlist", command=self.get_file)
        self.choose_net.pack(side=TOP,fill=X,pady=20)
        self.start_simu = Button(buttons, text="Start Simulation", command=self.start_simu)
        self.start_simu.pack(side=TOP,fill=X,pady=20)
        self.quit = Button(buttons, text="Quit", command=self.file_input.close)
        self.quit.pack(side=TOP,fill=X,pady=20)

    def get_file(self):
        file_temp = tkFileDialog.askopenfilename(filetypes=[("text file", "*.cir")])
        if file_temp == '':
            pass
        else:
            self.file_input_name = file_temp
        self.file_input = open(self.file_input_name,'r')
        self.netlist.delete(0.0, END)
        self.net = self.file_input.readlines()
        for lines in self.net:
            self.netlist.insert(END, lines)
        print (self.file_input)

    def start_simu(self):
        plt.close()
        self.res_print.delete(0.0, END)
        self.res_print.insert(END, 'Simulation Start\n')
        self.res_print.insert(END, '>>>>>>\n')
        net = net_parser.myparser(self.file_input_name)
        element = elements.obj_element(net)
        self.res_print.delete(0.0, END)
        self.res_print.insert(END, 'Simulation Done\n')
        for lines in element.print_data:
            self.res_print.insert(END, lines)
