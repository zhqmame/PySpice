###class Resistor by zhq 20190323
import numpy as np 

class Resistor():
    def __init__(self,value,node1,node2):
        self.value=value
        self.node1=node1
        self.node2=node2
        ##index of matrix must be number not real node##
    def get_matrix_r(self,size):
        self.matrix_r=np.zeros((size,size))
        print (self.matrix_r)
        #we need conductance
        self.value= 1/float(self.value)
        self.matrix_r[self.node1,self.node1]=self.value
        self.matrix_r[self.node1,self.node2]=self.value
        self.matrix_r[self.node2,self.node1]=-self.value
        self.matrix_r[self.node2,self.node2]=-self.value
        
        return self.matrix_r