import numpy as np
class Inductor:
    def __init__(self,value,node1,node2,ic):
        self.node1 = node1
        self.node2 = node2
        self.ic = ic
        self.value=value
        self.branch = 0
        self.size = 0
        self.i_lasttime=ic
        self.v_lasttime=0
        self.v=0
        self.first_flag=True
        self.step=0
        self.last_step=0
        self.lte_lasttime=0
    def get_matrix_l(self,omega):
        m = np.zeros((self.size,self.size))
        self.matrix_l = np.matrix(m,complex)  ## change the matrix into complex
        self.matrix_l[self.node1,self.branch]=1
        self.matrix_l[self.node2,self.branch]=-1
        self.matrix_l[self.branch,self.node2]=-1
        self.matrix_l[self.branch,self.node1]=1
        self.matrix_l[self.branch,self.branch]=-self.value*(0+1j)*omega

        return self.matrix_l
    def get_dc_matrix_l(self,size,vbranch,ibranch):

        self.dc_matrix_l = np.zeros((size,size))
        self.dc_matrix_l[self.node1,ibranch]=1
        self.dc_matrix_l[self.node2,ibranch]=-1
        self.dc_matrix_l[vbranch,self.node2]=-1
        self.dc_matrix_l[vbranch,self.node1]=1
        self.dc_matrix_l[vbranch,ibranch]=0
        self.branch = ibranch
        self.size = size

        return self.dc_matrix_l
    def get_branch_l(self):
        return self.branch
    def get_ic_l(self):
        return self.ic
    def get_tran_matrix_l(self,h,it,size):

        self.tran_matrix_l= np.zeros((size,size))
        z = np.zeros((size,1))
        val = self.value/h
        self.tran_matrix_l[self.node1][self.branch]=1
        self.tran_matrix_l[self.node2][self.branch]=-1
        self.tran_matrix_l[self.branch][self.node1]=1
        self.tran_matrix_l[self.branch][self.node2]=-1
        self.tran_matrix_l[self.branch][self.branch]=-val
        if(self.first_flag):
            self.last_step=h
            self.first_flag=False
        else:
            self.last_step=self.step
        self.step=h
        self.v_lasttime = self.v
        self.v = self.get_voltage(it,self.i_lasttime,self.last_step) ################
        self.i_lasttime = it
        z[self.branch][0]=-val*it
        self.tran_matrix_l = np.matrix(self.tran_matrix_l,float)
        z = np.matrix(z,float)

        return self.tran_matrix_l,z
    def get_voltage(self,i_n,i_n_1,hn_1):
        v = self.value*(i_n-i_n_1)/hn_1
        return v
    def compare_step(self):
        #print self.last_step,self.value,self.v,self.v_lasttime

        lte =  abs((self.v-self.v_lasttime)*self.last_step/self.value/2)
        #print 'the lte: ',lte
        if(lte<=0.5*self.lte_lasttime) :
            step=self.step*2
        elif(lte>2.2*self.lte_lasttime):
            step=self.step/2
        else:
            step=self.step
        self.lte_lasttime=lte
        return step
