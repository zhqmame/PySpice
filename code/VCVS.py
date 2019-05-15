import numpy as np 
class VCVS():
    def __init__(self,node1,node2,node3,node4,value):
        self.node1=node1
        self.node2=node2
        self.node3=node3
        self.node4=node4
        self.value = value
    def get_matrix_VCVS(self,size,vbranch,ibranch):
        self.matrix_VCVS=np.zeros((size,size))
        self.matrix_VCVS[vbranch,self.node1]=1
        self.matrix_VCVS[vbranch,self.node2]=-1
        self.matrix_VCVS[vbranch,self.node3]=-self.value
        self.matrix_VCVS[vbranch,self.node4]=self.value
        self.matrix_VCVS[self.node1,ibranch]=1
        self.matrix_VCVS[self.node2,vbranch]=-1
        
        return self.matrix_VCVS
        
