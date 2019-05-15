##class of Isrc
import numpy as np
class Isrc():
    def __init__(self,dcvalue,node1,node2,acvalue=0,other=''):
        self.node1=node1
        self.node2=node2
        self.dcvalue=dcvalue
        self.acvalue = acvalue
        self.other = other
    def get_matrix_Isrc(self,size):

        self.matrix_Isrc= np.zeros((size,1))
        self.matrix_Isrc[self.node1,0]=-self.dcvalue
        self.matrix_Isrc[self.node2,0]=self.dcvalue

        return self.matrix_Isrc