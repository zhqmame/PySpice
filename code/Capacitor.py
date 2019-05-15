import numpy as np

class Capacitor:
    def __init__(self,value,node1,node2,ic):## h is the first step
        self.node1=node1
        self.node2=node2
        self.value=value
        self.ic = ic
        self.size= 0
        self.i_lasttime=0
        self.v_lasttime=ic
        self.i=0
        self.first_flag=True
        self.step=0
        self.last_step=0
        self.lte_lasttime=0


    def get_matrix_c(self,omega):

        m= np.zeros((self.size,self.size))
        self.matrix_c = np.matrix(m,complex)

        self.matrix_c[self.node1,self.node1]=self.value*(0+1j)*omega
        self.matrix_c[self.node2,self.node2]=self.value*(0+1j)*omega
        self.matrix_c[self.node1,self.node2]=-self.value*(0+1j)*omega
        self.matrix_c[self.node2,self.node1]=-self.value*(0+1j)*omega

        return self.matrix_c
    def get_dc_matrix_c(self,size):

        self.dc_matrix_c= np.zeros((size,size))

        self.dc_matrix_c[self.node1][self.node1]=0
        self.dc_matrix_c[self.node2][self.node2]=0
        self.dc_matrix_c[self.node1][self.node2]=0
        self.dc_matrix_c[self.node2][self.node1]=0

        self.size = size

        return self.dc_matrix_c
    ##MNA model
    def get_tran_matrixm_c(self,h,vt,branch):
        
        self.tran_matrix_c= np.zeros((branch+1,branch+1))
        
        z = np.zeros((branch+1,1))
        
        val = self.value/h
        self.tran_matrix_c[self.node1,branch]=1
        self.tran_matrix_c[self.node2,branch]=-1
        self.tran_matrix_c[branch,branch]=-1
        self.tran_matrix_c[branch,self.node1]=val
        self.tran_matrix_c[branch,self.node2]=-val
        #print'the state :', self.first_flag
        if(self.first_flag):
            self.last_step=h
            self.first_flag=False
        else:
            self.last_step=self.step
        self.step=h
        self.i_lasttime=self.i
        self.i = self.get_current(vt,self.v_lasttime,self.last_step)
        self.v_lasttime = vt
        #print h,self.value
        z[branch][0]=val*vt
        #print '*********vt:  ',vt
        self.tran_matrix_c = np.matrix(self.tran_matrix_c,float)
        z = np.matrix(z,float)
        '''
        print ('self.tran_matrix_c: ',self.tran_matrix_c)
        print ('z: ',z)
        '''
        return self.tran_matrix_c,z

    def get_current(self,vn,vn_1,hn_1):
        i = self.value*(vn-vn_1)/hn_1
        return i
    def compare_step(self):
        #print self.last_step,self.value,self.i,self.i_lasttime

        lte =  abs((self.i-self.i_lasttime)*self.last_step/self.value/2)
        #print 'the lte: ',lte
        if(lte<=0.5*self.lte_lasttime) :
            step=self.step*2
        elif(lte>2.2*self.lte_lasttime):
            step=self.step/2
        else:
            step=self.step
        self.lte_lasttime=lte
        return step

    def get_node_c(self):
        return self.node1,self.node2
    def get_ic_c(self):
        return self.ic