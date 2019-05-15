import numpy as np 
class VCCS():
    def __init__(self,node1,node2,node3,node4,value):
        self.node1=node1
        self.node2=node2
        self.node3=node3
        self.node4=node4
        self.value = value
    def get_matrix_VCCS(self,size):
        self.matrix_VCCS=np.zeros((size,size))
        self.matrix_VCCS[self.node1,self.node3]=self.value
        self.matrix_VCCS[self.node2,self.node4]=self.value
        self.matrix_VCCS[self.node1,self.node4]=-self.value
        self.matrix_VCCS[self.node2,self.node3]=-self.value
        
        return self.matrix_VCCS