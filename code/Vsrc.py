###class of Vsrc
import numpy as np 
class Vsrc():
    def __init__(self,dcValue,node1,node2,acvalue):
        self.dcValue=dcValue
        self.node1=node1
        self.node2=node2
        self.acvalue=acvalue
    def get_matrix_Vs(self,size,branchv,branchi):
        
        self.matrix_Vs=np.zeros((size,size))
        self.matrix_Vs[self.node1,branchi]=1
        self.matrix_Vs[self.node2,branchi]=-1
        self.matrix_Vs[self.node1,branchv]=1
        self.matrix_Vs[self.node2,branchv]=-1

        return self.matrix_Vs


