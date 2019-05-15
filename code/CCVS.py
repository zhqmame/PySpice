import numpy as np

class CCVS():
    def __init__(self,node1,node2,node3,node4,value,voltage):
        self.node1=node1
        self.node2=node2
        self.node3=node3
        self.node4=node4
        self.value = value
        self.voltage = voltage
    def get_matrix_CCVS(self,size,vsvbranch,vsibranch,ccvbranch,ccibranch):
        self.martrix_CCVS = np.zeros((size,size))
    
        self.martrix_CCVS[vsvbranch,self.node1]=1
        self.martrix_CCVS[vsvbranch,self.node2]=-1
        self.martrix_CCVS[ccvbranch,self.node3]=1
        self.martrix_CCVS[ccvbranch,self.node4]=-1
        self.martrix_CCVS[self.node1,vsibranch]=1
        self.martrix_CCVS[self.node2,vsibranch]=-1
        self.martrix_CCVS[self.node3,ccibranch]=1
        self.martrix_CCVS[self.node4,ccibranch]=-1
        self.martrix_CCVS[vsvbranch,ccibranch]=-self.value

        return self.martrix_CCVS