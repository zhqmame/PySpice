from tkinter import*
import tkinter.filedialog
import tkinter.messagebox
from Parser import MyParser
from simulation import simulator
import matplotlib.pyplot as plt 

class myAPP():
    def __init__(self,root_master):
        # initial
        self.qFlag=False
        self.master=root_master
        ## text frame
        texts = Frame(root_master)
        texts.pack(side=LEFT)
        self.netlist = Text(texts, height=20, width=100)
        self.res_print = Text(texts, height=10, width=100)
        self.netlist.grid(row=0,column=0,sticky=W)
        self.res_print.grid(row=1,column=0,sticky=W)
        #self.netlist.pack(side=TOP)
        #self.res_print.pack(side=TOP)
        #buttons frame
        buttons = Frame(root_master)
        buttons.pack(side=LEFT)
        self.choose_net = Button(buttons, text="Choose Netlist", command=self.get_file)
        self.choose_net.pack(side=TOP,fill=X,pady=20)
        #self.start_parse = Button(buttons, text="Start Parse", command=self.start_parser)
        #self.start_parse.pack(side=TOP,fill=X,pady=20)
        self.start_simu = Button(buttons, text="Start Simulation", command=self.start_simulation)
        self.start_simu.pack(side=TOP,fill=X,pady=20)
        self.quit = Button(buttons, text="Quit",command=self.close)
        self.quit.pack(side=TOP,fill=X,pady=20)
    def get_file(self):
        file_name = tkinter.filedialog.askopenfilename(filetypes=[("text file", "*.sp")])
        if file_name == '':
            pass
        else:
            self.file_input_name = file_name
        self.file_input = open(self.file_input_name,'r')
        self.net = self.file_input.readlines()
        ## clear TEXT netlist
        self.netlist.delete(0.0,tkinter.END)
        # show TEXT netlist
        for lines in self.net:
            self.netlist.insert(END, lines)
        #self.master.update()
        #print (self.file_input)   
    def start_simulation(self):
        self.res_print.delete(0.0, END)
        #print(self.net)
        self.res_print.insert(END, '#--------------------Start Parse the Netlist---------------------#\n')
        sim_parse=MyParser(self.net)
        a,b=sim_parse.parse()
        #print (a,'hi')
        if (a==-1):
            parser_info=sim_parse.showParseResult()
        else:
            parser_info='have error at line '+str(b)
        for lines in parser_info:
            self.res_print.insert(END,lines)
        self.res_print.insert(END, ' ')
        self.res_print.insert(END,'#----------------------Start the Simulation----------------------#\n')
        sim_simulator=simulator(self.net)
        sim_simulator.solve_net()
        self.res_print.insert(END,'#----------------------Successful Simulation----------------------#\n')
    def close(self):
        #message box to give info in another window
        self.qFlag=tkinter.messagebox.askyesno('info','QUIT?')
        if(self.qFlag):
            self.master.quit()
            self.master.destroy()
        
'''
root = Tk()
a=myAPP(root)
root.title('PySimulator')
root.iconbitmap('C:\\Users\\朱汉卿\\Desktop\\EDA\\PySimulator\\ico\\circuit.ico')
root.mainloop()
'''