import numpy as np
class CCCS:
    def __init__(self,node1,node2,node3,node4,value,voltage):
        self.node1=node1
        self.node2=node2
        self.node3=node3
        self.node4=node4
        self.value = value
        self.voltage = voltage
    def get_matrix_CCCS(self,size,vbranch,ibranch):
        self.martrix_CCCS = np.zeros((size,size))
        '''
        print vbranch,self.node3
        print type(vbranch),type(self.node3)
        print self.node4
        '''
        self.martrix_CCCS[vbranch,self.node3]=1
        self.martrix_CCCS[vbranch,self.node4]=-1
        self.martrix_CCCS[self.node3,ibranch]=self.value
        self.martrix_CCCS[self.node4,ibranch]=-self.value
        self.martrix_CCCS[self.node1,ibranch]=1
        self.martrix_CCCS[self.node2,ibranch]=-1
        
        return self.martrix_CCCS