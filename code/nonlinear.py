import numpy as np
import matplotlib.pyplot as plt  
from math import*
class nonlinear_solver():
    def __init__(self,esp,flag_out):
        self.esp=esp
        self.flag_out=flag_out
        if(self.flag_out==0):
            self.solver(0.1)
        else:
            self.iter_out(0.1)
    def solve_function(self,x):
        f0=2/3*x+exp(40*x)-5/3
        f1=40*exp(40*x)+2/3
        f1=1/f1
        return f0,f1
    def x_list(self,x,initial_value):
        dict_x={}
        dict_x_previous={}
        dict_x.update({x:initial_value})
        dict_x_previous.update({x:0})
        return dict_x,dict_x_previous
    def iter_out(self,initial_value):
        x=np.arange(0,0.1,0.00001)
        #e=math.e
        #y=2*x
        plt.xlim((0,0.15))
        plt.ylim((0,60))
        y=2/3*x+e**(40*x)-5/3
        #plt.plot(x,y)
        
        iter_num=0
        iter_flag=0
        dict_x,dict_x_previous=self.x_list('x',initial_value)
        #f={}
        #f_previous={}
        print('threshold','                  ',self.esp)
        print('iteration','                  ','iter_num')
        while (iter_flag==0):
            iter_num+=1
            for key,val in dict_x.items():
                #print(key,val)
                dict_x_previous[key]=dict_x[key]
                node_value,slope=self.solve_function(val)
                #print(node_value,slope)
                dict_x[key]=val-slope*node_value
                temp=dict_x[key]
                iter_val=-temp+dict_x_previous[key]
                '''
                #plot part
                x_plot=np.arange(0,0.1,0.00001)
                y_plot=1/slope*(x-val)+node_value
                plt.plot(x_plot,y_plot)
                plt.scatter(val,node_value,s=50)
                plt.scatter(temp,0,s=50)
                '''
                print (iter_val,'     ',iter_num)
                #print(type(val))
                #print(type(dict_x_previous[key]))
                if(abs(val-temp)<=self.esp):
                    iter_flag=1
                    #print(abs(val-temp))
                    
        #plt.show()
    def solver(self,initial_value):
        x=np.arange(0,0.1,0.00001)
        #e=math.e
        #y=2*x
        plt.xlim((0,0.15))
        plt.ylim((0,60))
        y=2/3*x+e**(40*x)-5/3
        plt.plot(x,y)
        
        iter_num=0
        iter_flag=0
        dict_x,dict_x_previous=self.x_list('x',initial_value)
        #f={}
        #f_previous={}
        print('V2','                  ','iter_num')
        while (iter_flag==0):
            iter_num+=1
            for key,val in dict_x.items():
                #print(key,val)
                dict_x_previous[key]=dict_x[key]
                node_value,slope=self.solve_function(val)
                #print(node_value,slope)
                dict_x[key]=val-slope*node_value
                temp=dict_x[key]
                
                #plot part
                x_plot=np.arange(0,0.1,0.00001)
                y_plot=1/slope*(x-val)+node_value
                plt.plot(x_plot,y_plot)
                plt.scatter(val,node_value,s=50)
                plt.scatter(temp,0,s=50)
                print (dict_x[key],'     ',iter_num)
                #print(type(val))
                #print(type(dict_x_previous[key]))
                if(abs(val-temp)<=self.esp):
                    iter_flag=1
                    #print(abs(val-temp))
                    
        plt.show()

            
            

'''
shabi=nonlinear_solver(0.0005)
a=shabi.solver(0.1)
'''
'''
for key, val in a.items():
    print (key,val)
print(5/3)

'''