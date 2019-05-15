#coding=utf-8

##      created by zhq    ##
##------------test part-----------------##
##python version test
#print ('hi')
#print 'hi'

##test import class succesful 
#R1=Resistor(3,2,1)
import scipy.sparse 
import scipy.sparse.linalg
import numpy as np
import math
from Parser import MyParser
## NOTE:try to import devices class from a self-difinited package but #error#
import turn_unit
from nonlinear import nonlinear_solver
from Resistor import Resistor
from Capacitor import Capacitor
from CCCS import CCCS
from CCVS import CCVS
from VCVS import VCVS
from VCCS import VCCS
from Isrc import Isrc
from Vsrc import Vsrc
from Inductor import Inductor
import matplotlib.pyplot as plt
#from devices.Resistor import *

class simulator():
    def __init__(self,netlist):
        self.net=netlist
        self.sim_Parser=MyParser(self.net)
        self.sim_Parser.parse()
        #print(self.sim_Parser.dict_node)
        self.modify_rows=0
        self.rows=len(self.sim_Parser.dict_node)
        self.MNA_dc_solve={}
        self.RHS_dc_solve={}
        self.results_DC_print={}
        ##param for ac simul
        self.MNA_ac_solve={}
        self.RHS_ac_solve={}
        ## param for tran simul
        self.MNA_tran_solve={}
        self.RHS_tran_solve={}
        self.tran_step=0
        self.tran_end=0
        self.tran_simulator_option={'BE': 0,'FE':1,'TR':2}
        self.tran_option_select=0
        self.step_value=0
        self.v_value={}
        self.node_D={}
        self.node_M={}
        #test type ?int
        #a=self.tran_simulator_option['BE']
        #print (type(a))
        #print (self.rows)
        '''
        if (a==-1):
            #print ('hi')
            self.sim_Parser.showParseResult()
        '''
        self.MNA_dc={}
        self.RHS_dc={}
        self.modify_node_branch={} #store row num and index v?i
        self.modify_node_branch_num_change={}
        #for print
        '''
        if net.print_plot_cmd != {}:
            self.out_plot()
        '''
    ##---------------------------some tool function-----------------------------------##
    def delete_x(self,MNA,RHS,x):
        MNA=np.delete(MNA,x,0)
        MNA=np.delete(MNA,x,1)
        RHS=np.delete(RHS,x,0)
        return MNA,RHS
    def node_num_change(self,dict_node_change):
        i=0
        minus_flag=0
        #print(self.modify_node_branch)
        #self.results_DC_print.update({0:0})
        for node_key in dict_node_change.keys():
            #print(node_key)
            #print (self.rows)
            if i< self.modify_rows:
                i+=1
                if (node_key=='gnd') or (node_key=='0'):
                    #print('hi')
                    minus_flag = 1
                else:
                    if (minus_flag==0):
                        pass
                        #print(minus_flag)
                        #print (node_key)
                        #node_num=dict_node[node_key]
                        #print (node_num)
                        #node_v_value=self.results_DC[node_num]
                        #self.results_DC_print.update({node_key:node_v_value})
                    else:
                        node_num=dict_node_change[node_key]
                        node_num-=1
                        dict_node_change[node_key]=node_num
                        #node_v_value=self.results_DC[node_num]
                        #self.results_DC_print.update({node_key:node_v_value})
            else:
                break
        return dict_node_change    
    def add_branch_ac(self):
        i=self.rows-1
        #for index need
        self.modify_node_branch.update(self.sim_Parser.dict_node)
        if (len(self.sim_Parser.dict_v)!=0):
            for v_key in self.sim_Parser.dict_v.keys():
                i+=1
                self.modify_node_branch.update({v_key:i})
        if (len(self.sim_Parser.dict_l)!=0):
            for l_key in self.sim_Parser.dict_l.keys():
                i+=1
                self.modify_node_branch.update({l_key:i})
        if (len(self.sim_Parser.dict_E)!=0):
            for E_key in self.sim_Parser.dict_E.keys():
                i+=1
                self.modify_node_branch.update({E_key:i})
        if (len(self.sim_Parser.dict_H)!=0):
            for H_key in self.sim_Parser.dict_H.keys():
                i+=1
                self.modify_node_branch.update({H_key:i})
        if (len(self.sim_Parser.dict_F)!=0):
            for F_key in self.sim_Parser.dict_F.keys():
                i+=1
                self.modify_node_branch.update({F_key:i})
                
        #print (self.modify_node_branch)
        self.modify_rows=i+1
        #print (self.modify_rows)

        #print (self.modify_node_branch)
    def add_branch(self):
        i=self.rows-1
        #for index need
        self.modify_node_branch.update(self.sim_Parser.dict_node)
        if (len(self.sim_Parser.dict_v)!=0):
            for v_key in self.sim_Parser.dict_v.keys():
                i+=1
                self.modify_node_branch.update({v_key:i})
        if (len(self.sim_Parser.dict_l)!=0):
            for l_key in self.sim_Parser.dict_l.keys():
                i+=1
                self.modify_node_branch.update({l_key:i})
        if (len(self.sim_Parser.dict_c)!=0):
            for c_key in self.sim_Parser.dict_c.keys():
                i+=1
                self.modify_node_branch.update({c_key:i})
        if (len(self.sim_Parser.dict_E)!=0):
            for E_key in self.sim_Parser.dict_E.keys():
                i+=1
                self.modify_node_branch.update({E_key:i})
        if (len(self.sim_Parser.dict_H)!=0):
            for H_key in self.sim_Parser.dict_H.keys():
                i+=1
                self.modify_node_branch.update({H_key:i})
        if (len(self.sim_Parser.dict_F)!=0):
            for F_key in self.sim_Parser.dict_F.keys():
                i+=1
                self.modify_node_branch.update({F_key:i})
                
        #print (self.modify_node_branch)
        self.modify_rows=i+1
        #print (self.modify_rows)

        #print (self.modify_node_branch)
    def dc_mna_matrix(self):
        self.add_branch()
        self.MNA_dc=np.zeros ((self.modify_rows,self.modify_rows))
        self.RHS_dc=np.zeros(self.modify_rows)
        #R
        if (len(self.sim_Parser.dict_r)!=0):
            #r_length=len(self.sim_Parser.dict_r)
            #i=0
            for r_key in self.sim_Parser.dict_r.keys():
                r_value=self.sim_Parser.dict_r[r_key][0]
                #print(r_value)
                ##node for N+ N-
                node1=self.sim_Parser.dict_r[r_key][1]
                node2=self.sim_Parser.dict_r[r_key][2]
                ##get node num to be np's index
                node1_num=self.sim_Parser.dict_node[node1]
                node2_num=self.sim_Parser.dict_node[node2]
                #print(node1_num,node2_num)
                self.R_mna_constr(node1_num,node2_num,r_value,self.MNA_dc)
                #print (self.MNA_dc)
                #print(node1,node2)
        #V
        if (len(self.sim_Parser.dict_v)!=0):
            for v_key in self.sim_Parser.dict_v.keys():
                #print (self.sim_Parser.dict_v[v_key])
                v_value=self.sim_Parser.dict_v[v_key][0]
                node1=self.sim_Parser.dict_v[v_key][1]
                node2=self.sim_Parser.dict_v[v_key][2]
                #print (node1)
                node1_num=self.modify_node_branch[node1]
                node2_num=self.modify_node_branch[node2]
                #np.c_(self.MNA_dc,'0')
                #np.r_(self.MNA_dc,0)
                #print(self.sim_Parser.dict_v[v_key])
                self.V_mna_constr(node1_num,node2_num,v_key,v_value,self.MNA_dc,self.RHS_dc)
                #print (self.MNA_dc)
        #I
        if (len(self.sim_Parser.dict_i)!=0):
            for i_key in self.sim_Parser.dict_i.keys():
                i_value=self.sim_Parser.dict_i[i_key][0]
                node1=self.sim_Parser.dict_i[i_key][1]
                node2=self.sim_Parser.dict_i[i_key][2]
                node1_num=self.modify_node_branch[node1]
                node2_num=self.modify_node_branch[node2]
                self.I_mna_constr(node1_num,node2_num,i_value,self.RHS_dc)
                #print (self.MNA_dc)
        #G
        if (len(self.sim_Parser.dict_G)!=0):
            for g_key in self.sim_Parser.dict_G.keys():
                node1=self.sim_Parser.dict_G[g_key][0]
                node2=self.sim_Parser.dict_G[g_key][1]
                nc1=self.sim_Parser.dict_G[g_key][2]
                nc2=self.sim_Parser.dict_G[g_key][3]
                node1_num=self.modify_node_branch[node1]
                node2_num=self.modify_node_branch[node2]
                nc1_num=self.modify_node_branch[nc1]
                nc2_num=self.modify_node_branch[nc2]
                g_value=self.sim_Parser.dict_G[g_key][4]
                self.G_mna_constr(node1_num,node2_num,nc1_num,nc2_num,g_value,self.MNA_dc)
                #print (self.MNA_dc)
        #E
        if (len(self.sim_Parser.dict_E)!=0):
            for e_key in self.sim_Parser.dict_E.keys():
                node1=self.sim_Parser.dict_E[e_key][0]
                node2=self.sim_Parser.dict_E[e_key][1]
                nc1=self.sim_Parser.dict_E[e_key][2]
                nc2=self.sim_Parser.dict_E[e_key][3]
                node1_num=self.modify_node_branch[node1]
                node2_num=self.modify_node_branch[node2]
                nc1_num=self.modify_node_branch[nc1]
                nc2_num=self.modify_node_branch[nc2]
                e_value=self.sim_Parser.dict_E[e_key][4]
                self.E_mna_constr(node1_num,node2_num,nc1_num,nc2_num,e_key,e_value,self.MNA_dc)
                #print (self.MNA_dc)
        #F
        if (len(self.sim_Parser.dict_F)!=0):
            for f_key in self.sim_Parser.dict_F.keys():
                node1=self.sim_Parser.dict_F[f_key][0]
                node2=self.sim_Parser.dict_F[f_key][1]
                node1_num=self.modify_node_branch[node1]
                node2_num=self.modify_node_branch[node2]
                v_name=self.sim_Parser.dict_v[f_key][2]
                nc1=self.sim_Parser.dict_v[v_name][1]
                nc2=self.sim_Parser.dict_v[v_name][2]
                nc1_num=self.modify_node_branch[nc1]
                nc2_num=self.modify_node_branch[nc2]
                f_value=self.sim_Parser.dict_F[f_key][3]
                self.F_mna_constr(node1_num,node2_num,nc1_num,nc2_num,f_key,f_value,0,self.MNA_dc)
                #print (self.MNA_dc)
        #H
        if(len(self.sim_Parser.dict_H)!=0):
            for h_key in self.sim_Parser.dict_H.keys():
                node1=self.sim_Parser.dict_H[h_key][0]
                node2=self.sim_Parser.dict_H[h_key][1]
                node1_num=self.modify_node_branch[node1]
                node2_num=self.modify_node_branch[node2]
                v_name=self.sim_Parser.dict_v[h_key][2]
                nc1=self.sim_Parser.dict_v[v_name][1]
                nc2=self.sim_Parser.dict_v[v_name][2]
                nc1_num=self.modify_node_branch[nc1]
                nc2_num=self.modify_node_branch[nc2]
                h_value=self.sim_Parser.dict_H[h_key][3]
                self.H_mna_constr(node1_num,node2_num,nc1_num,nc2_num,h_key,v_name,h_value,0,self.MNA_dc)
                #print (self.MNA_dc)




            '''
            r_name = self.sim_Parser.dict_r.keys()
            print (r_name[2])
            while i<r_length:
                node1=self.sim_Parser.dict_r[r_name[i]]
                print(node1)
            '''
    ##------------------------------------solve part-----------------------------------##
    def solve_net(self):
        #print(self.sim_Parser.dict_command)
        for command_key in self.sim_Parser.dict_command.keys():
            #print(self.sim_Parser.dict_command[command_key])
            if (command_key=='dc'):
                self.source=self.sim_Parser.dict_command['dc'][0]
                self.source_start=self.sim_Parser.dict_command['dc'][1]
                self.source_stop=self.sim_Parser.dict_command['dc'][2]
                self.source_step=self.sim_Parser.dict_command['dc'][3]
                self.dc_solve_net()
            elif(command_key == 'ac'):
                self.ac_swep_type = self.sim_Parser.dict_command['ac'][0]
                self.ac_samp_num = self.sim_Parser.dict_command['ac'][1]
                self.ac_swep_start = self.sim_Parser.dict_command['ac'][2]
                self.ac_swep_end = self.sim_Parser.dict_command['ac'][3]
                self.ac_solve_net()
            elif (command_key =='tran'):
                #print('hi')
                self.tran_step = self.sim_Parser.dict_command['tran'][0] #tran plot step
                self.tran_end =self.sim_Parser.dict_command['tran'][1]
                self.tran_solve_net()
    def dc_solve_net(self):
        self.DC_swep_result={}
        u0={}
        u1={}
        ud0={}
        ud1={}
        vs0={}
        vs1={}
        vg0={}
        vg1={}
        is_op=0
        self.dc_converge_threshold=0.0005
        self.dc_mos_converge_threshold=0.01
        flag_iter_end=1
        iter_flag=0
        iter_cnt=0
        flag_dc_append=0
        self.DC_swep_list=np.arange(self.source_start,self.source_stop+self.source_step,self.source_step)
        #print(self.DC_swep_list)
        for v_swep in self.DC_swep_list:
            flag_iter=0
            #print('1')
            while ((flag_iter<=1))or(flag_iter_end==0):
                #print('2')
                #end iter
                for u_key,u_val in u0.items():
                    flag_iter_end=1
                    if (abs(u_val-u1[u_key])>=self.dc_converge_threshold):
                        end=0
                    else:
                        end=1
                    flag_iter_end=flag_iter_end and end
                for ud_key,ud_val in ud0.items():
                    flag_iter_end=1
                    if (abs(ud_val-ud1[ud_key])>=self.dc_mos_converge_threshold) or (abs(vs0[ud_key]-vs1[ud_key])>=self.dc_mos_converge_threshold) or(abs(vg0[ud_key]-vg1[ud_key])>=self.dc_mos_converge_threshold) :
                        end=0
                    else:
                        end=1
                    flag_iter_end=flag_iter_end and end
                #need flag iter to excute one loop
                flag_iter+=1
                #print(flag_iter)
                if flag_iter>200:
                    break
                self.add_branch()
                self.MNA_dc=np.zeros ((self.modify_rows,self.modify_rows))
                self.RHS_dc=np.zeros(self.modify_rows)
                #print('original',self.modify_node_branch)
                #self.dc_mna_matrix()
                #dc_mna don not need a extra func
                ##dc no C
                #C
                if (len(self.sim_Parser.dict_c)!=0):
                    for c_key in self.sim_Parser.dict_c.keys():
                        '''
                        node1=self.sim_Parser.dict_c[c_key][1]
                        node2=self.sim_Parser.dict_c[c_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        '''
                        c_branch_num=self.modify_node_branch[c_key]
                        self.MNA_dc=np.delete(self.MNA_dc,c_branch_num,0)
                        self.MNA_dc=np.delete(self.MNA_dc,c_branch_num,1)
                        self.RHS_dc=np.delete(self.RHS_dc,c_branch_num,0)
                        ## get c_key out of modify_branch for dc don't have C
                        i=0
                        minus_flag=0
                        self.modify_node_branch_dc=self.modify_node_branch.copy()
                        for node_key in self.modify_node_branch_dc.keys():
                            #print(node_key)
                            if i< self.modify_rows:
                                i+=1
                                if (node_key==c_key):
                                    minus_flag=1
                                    #del self.modify_node_branch_dc[c_key]                                
                                else:
                                    if(minus_flag==0):
                                        pass
                                    else:
                                        node_num=self.modify_node_branch_dc[node_key]
                                        self.modify_node_branch_dc[node_key]=node_num-1
                                        node_num=self.modify_node_branch[node_key]
                                        self.modify_node_branch[node_key]=node_num-1
                                                                        
                            else:
                                break
        #test
                    #print(self.modify_node_branch,self.modify_node_branch_dc)
                #R
                if (len(self.sim_Parser.dict_r)!=0):
                    #r_length=len(self.sim_Parser.dict_r)
                    #i=0
                    for r_key in self.sim_Parser.dict_r.keys():
                        r_value=self.sim_Parser.dict_r[r_key][0]
                        #print(r_value)
                        ##node for N+ N-
                        node1=self.sim_Parser.dict_r[r_key][1]
                        node2=self.sim_Parser.dict_r[r_key][2]
                        ##get node num to be np's index
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        #print(node1_num,node2_num)
                        self.R_mna_constr(node1_num,node2_num,r_value,self.MNA_dc)
                        #print (self.MNA_dc)
                        #print(node1,node2)
                #V
                if (len(self.sim_Parser.dict_v)!=0):
                    for v_key in self.sim_Parser.dict_v.keys():
                        #print (self.sim_Parser.dict_v[v_key])
                        if (v_key==self.source):
                            v_value=v_swep
                            node1=self.sim_Parser.dict_v[v_key][1]
                            node2=self.sim_Parser.dict_v[v_key][2]
                            node1_num=self.modify_node_branch[node1]
                            node2_num=self.modify_node_branch[node2]
                            self.V_mna_constr(node1_num,node2_num,v_key,v_value,self.MNA_dc,self.RHS_dc)
                        else:
                            v_value=self.sim_Parser.dict_v[v_key][0]
                            node1=self.sim_Parser.dict_v[v_key][1]
                            node2=self.sim_Parser.dict_v[v_key][2]
                            #print (node1)
                            node1_num=self.modify_node_branch[node1]
                            node2_num=self.modify_node_branch[node2]
                            #np.c_(self.MNA_dc,'0')
                            #np.r_(self.MNA_dc,0)
                            #print(self.sim_Parser.dict_v[v_key])
                            self.V_mna_constr(node1_num,node2_num,v_key,v_value,self.MNA_dc,self.RHS_dc)
                            #print (self.MNA_dc)
                        
                #I
                if (len(self.sim_Parser.dict_i)!=0):
                    for i_key in self.sim_Parser.dict_i.keys():
                        i_value=self.sim_Parser.dict_i[i_key][0]
                        node1=self.sim_Parser.dict_i[i_key][1]
                        node2=self.sim_Parser.dict_i[i_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        self.I_mna_constr(node1_num,node2_num,i_value,self.RHS_dc)
                        #print (self.MNA_dc)
                #G
                if (len(self.sim_Parser.dict_G)!=0):
                    for g_key in self.sim_Parser.dict_G.keys():
                        node1=self.sim_Parser.dict_G[g_key][0]
                        node2=self.sim_Parser.dict_G[g_key][1]
                        nc1=self.sim_Parser.dict_G[g_key][2]
                        nc2=self.sim_Parser.dict_G[g_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        g_value=self.sim_Parser.dict_G[g_key][4]
                        self.G_mna_constr(node1_num,node2_num,nc1_num,nc2_num,g_value,self.MNA_dc)
                        #print (self.MNA_dc)
                #E
                if (len(self.sim_Parser.dict_E)!=0):
                    for e_key in self.sim_Parser.dict_E.keys():
                        node1=self.sim_Parser.dict_E[e_key][0]
                        node2=self.sim_Parser.dict_E[e_key][1]
                        nc1=self.sim_Parser.dict_E[e_key][2]
                        nc2=self.sim_Parser.dict_E[e_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        e_value=self.sim_Parser.dict_E[e_key][4]
                        self.E_mna_constr(node1_num,node2_num,nc1_num,nc2_num,e_key,e_value,self.MNA_dc)
                        #print (self.MNA_dc)
                #F
                if (len(self.sim_Parser.dict_F)!=0):
                    for f_key in self.sim_Parser.dict_F.keys():
                        node1=self.sim_Parser.dict_F[f_key][0]
                        node2=self.sim_Parser.dict_F[f_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        v_name=self.sim_Parser.dict_v[f_key][2]
                        nc1=self.sim_Parser.dict_v[v_name][1]
                        nc2=self.sim_Parser.dict_v[v_name][2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        f_value=self.sim_Parser.dict_F[f_key][3]
                        self.F_mna_constr(node1_num,node2_num,nc1_num,nc2_num,f_key,f_value,0,self.MNA_dc)
                        #print (self.MNA_dc)
                #H
                if(len(self.sim_Parser.dict_H)!=0):
                    for h_key in self.sim_Parser.dict_H.keys():
                        node1=self.sim_Parser.dict_H[h_key][0]
                        node2=self.sim_Parser.dict_H[h_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        v_name=self.sim_Parser.dict_v[h_key][2]
                        nc1=self.sim_Parser.dict_v[v_name][1]
                        nc2=self.sim_Parser.dict_v[v_name][2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        h_value=self.sim_Parser.dict_H[h_key][3]
                        self.H_mna_constr(node1_num,node2_num,nc1_num,nc2_num,h_key,v_name,h_value,0,self.MNA_dc)
                #diode
                if (len(self.sim_Parser.dict_diode)!=0):
                    for diode_key in self.sim_Parser.dict_diode.keys():
                        if (u0=={})or(u1=={}):
                            for diode_key2 in self.sim_Parser.dict_diode.keys():
                                u0.update({diode_key2:0})
                                u1.update({diode_key2:0})
                        iter_flag+=1
                        node1=self.sim_Parser.dict_diode[diode_key][0]
                        node2=self.sim_Parser.dict_diode[diode_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        self.node_D.update({diode_key:{'node1':node1,'node2':node2}})
                        self.MNA_tran,self.RHS_tran=self.D_mna_constr(node1_num,node2_num,u1[diode_key],self.MNA_dc,self.RHS_dc)
                #MOS
                if (len(self.sim_Parser.dict_mos)!=0):
                    for mos_key in self.sim_Parser.dict_mos.keys():
                        #initial
                        if vg0=={}:
                            for mos_key2 in self.sim_Parser.dict_mos.keys():
                                if self.sim_Parser.dict_mos[mos_key2][0]=='nmos':
                                    ud0.update({mos_key2:0})
                                    vg0.update({mos_key2:0})
                                    vs0.update({mos_key2:0})
                                    ud1.update({mos_key2:1.15})
                                    vg1.update({mos_key2:1})
                                    vs1.update({mos_key2:0})
                                else:
                                    ud0.update({mos_key2:0})
                                    vg0.update({mos_key2:0})
                                    vs0.update({mos_key2:0})
                                    ud1.update({mos_key2:1.15})
                                    vg1.update({mos_key2:1})
                                    vs1.update({mos_key2:1.8})  
                        node1=self.sim_Parser.dict_mos[mos_key][1]
                        node2=self.sim_Parser.dict_mos[mos_key][2]
                        node3=self.sim_Parser.dict_mos[mos_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        node3_num=self.modify_node_branch[node3]
                        self.node_M.update({mos_key:{'noded':node1,'nodeg':node2,'nodes':node3}})
                        w_l=float(self.sim_Parser.dict_mos[mos_key][5])/self.sim_Parser.dict_mos[mos_key][6]
                        #print(w_l)
                        iter_flag+=1
                        if (self.sim_Parser.dict_mos[mos_key][0]=='nmos'):
                            self.NMOS_mna_constr(node1_num,node2_num,node3_num,ud1[mos_key],vs1[mos_key],vg1[mos_key],w_l,self.MNA_dc,self.RHS_dc)
                        else:
                            #print('hi')
                            self.PMOS_mna_constr(node1_num,node2_num,node3_num,ud1[mos_key],vs1[mos_key],vg1[mos_key],w_l,self.MNA_dc,self.RHS_dc)
                if iter_flag==0:
                    while is_op>0:
                        pass
                    if 'gnd' in self.modify_node_branch.keys():
                        num=self.modify_node_branch['gnd']
                    else:
                        num=self.modify_node_branch['0']
                    #print(num)
                    ##??? doesn't matter delect which row
                    #print(self.RHS_dc,self.MNA_dc)
                    self.MNA_dc_solve,self.RHS_dc_solve=self.delete_x(self.MNA_dc,self.RHS_dc,num)
                    #print (self.MNA_dc_solve,self.RHS_dc_solve)
                    self.results_DC = np.linalg.solve(self.MNA_dc_solve,self.RHS_dc_solve)
                    #print (self.results_DC)
                    #print (self.modify_node_branch)
                    #lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(self.MNA_dc_solve))
                    #x=lu.solve(self.RHS_dc_solve)
                    #print(x)
                    ##get a right num -->result
                    self.modify_node_branch_num_change=self.node_num_change(self.modify_node_branch)
                    #print (self.modify_node_branch_num_change)
                    self.modify_node_branch_no_gnd=self.modify_node_branch_num_change.copy()
                    self.modify_node_branch_copy=self.modify_node_branch.copy()
                    if 'gnd' in self.modify_node_branch_no_gnd.keys():
                        del self.modify_node_branch_no_gnd['gnd']
                    else:
                        del self.modify_node_branch_no_gnd['0']
                else:
                    #print('iter here')
                    iter_cnt+=1
                    if 'gnd' in self.modify_node_branch.keys():
                        num=self.modify_node_branch['gnd']
                    else:
                        num=self.modify_node_branch['0']
                    ## --------------slove part---------------------##
                    self.MNA_dc_solve,self.RHS_dc_solve=self.delete_x(self.MNA_dc,self.RHS_dc,num)
                    self.results_DC=np.linalg.solve(self.MNA_dc_solve,self.RHS_dc_solve)
                    #print(self.results_DC)
                    ##-------end---------------#
                    ##get a right num -->result
                    self.modify_node_branch_num_change=self.node_num_change(self.modify_node_branch)
                    #print ('num',self.modify_node_branch_num_change)
                    self.modify_node_branch_no_gnd=self.modify_node_branch_num_change.copy()
                    self.modify_node_branch_copy=self.modify_node_branch.copy()
                    
                    if 'gnd' in self.modify_node_branch_no_gnd.keys():
                        del self.modify_node_branch_no_gnd['gnd']
                    else:
                        del self.modify_node_branch_no_gnd['0']
                    #print('no gnd',self.modify_node_branch_no_gnd)
                    ## value for u0 u1
                    for diode_key in self.sim_Parser.dict_diode.keys():
                        u0[diode_key]=u1[diode_key]
                        if (self.node_D[diode_key]['node1']=='0') or (self.node_D[diode_key]['node1']=='gnd'):
                            u1[diode_key] =-self.results_DC[self.modify_node_branch_no_gnd['node2']]
                        elif (self.node_D[diode_key]['node2']=='0') or (self.node_D[diode_key]['node2']=='gnd'):
                            u1[diode_key] = self.results_DC[self.modify_node_branch_no_gnd['node1']]
                        else:
                            u1[diode_key] = self.results_DC[self.modify_node_branch_no_gnd['node1']]-self.results_DC[self.modify_node_branch_no_gnd['node2']]
                    ## value for mos
                    for mos_key in self.sim_Parser.dict_mos.keys():
                        ud0[mos_key] = ud1[mos_key]
                        vs0[mos_key] = vs1[mos_key]
                        vg0[mos_key] = vg1[mos_key]
                        if (self.node_M[mos_key]['noded']=='0') or (self.node_M[mos_key]['noded']=='gnd'):
                            ud1[mos_key] =0
                            vs1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodes']]]
                            vg1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodeg']]]
                        elif (self.node_M[mos_key]['nodes']=='0') or (self.node_M[mos_key]['nodes']=='gnd'):
                            ud1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['noded']]]
                            vs1[mos_key] =0
                            vg1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodeg']]]
                        elif (self.node_M[mos_key]['nodeg']=='0') or (self.node_M[mos_key]['nodeg']=='gnd'):
                            ud1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['noded']]]
                            vs1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodes']]]
                            vg1[mos_key] =0
                        else:
                            ud1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['noded']]]
                            vs1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodes']]]
                            vg1[mos_key] =self.results_DC[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodeg']]]
                    #print(ud0,ud1)
                    self.modify_node_branch.clear()
                    #print(self.modify_node_branch_no_gnd)
            #print(self.modify_node_branch,self.modify_node_branch_no_gnd)
            #print(self.modify_node_branch_no_gnd)
            for node_key in self.modify_node_branch_no_gnd.keys():
                    if len(self.DC_swep_result)!=0:
                        if flag_dc_append:
                            self.DC_swep_result[node_key].append(self.results_DC[self.modify_node_branch_no_gnd[node_key]])
                        else:
                            #print (flag_tran_y_append)
                            #print (self.modify_node_branch_no_gnd)
                            #print(node_key)
                            #print (self.TRAN_y_axis)
                            #print (self.results_tran[self.modify_node_branch_no_gnd[node_key]])
                            self.DC_swep_result.update({node_key:[self.results_DC[self.modify_node_branch_no_gnd[node_key]]]})
                    else:
                        self.DC_swep_result={'0':[0],node_key:[self.results_DC[self.modify_node_branch_no_gnd[node_key]]]}
            flag_dc_append=1
            self.DC_swep_result['0'].append(0)
        #print('hi')
        self.output_print()
        #print(self.node_M)
            #print (self.DC_swep_result)
        '''
                self.modify_node_branch_no_gnd=self.modify_node_branch.copy()
                if 'gnd' in self.modify_node_branch_no_gnd.keys():
                    del self.modify_node_branch_no_gnd['gnd']
                else:
                    del self.modify_node_branch_no_gnd['0']
                #print(self.modify_node_branch_no_gnd)
                i=0
                minus_flag=0
                #print(self.modify_node_branch)
                self.results_DC_print.update({0:0})
                for node_key in self.modify_node_branch.keys():
                    #print(node_key)
                    if i< self.rows:
                        i+=1
                        if (node_key=='gnd') or (node_key=='0'):
                            #print('hi')
                            minus_flag = 1
                        else:
                            if (minus_flag==0):
                                #print(minus_flag)
                                #print (node_key)
                                node_num=self.modify_node_branch[node_key]
                                #print (node_num)
                                node_v_value=self.results_DC[node_num]
                                self.results_DC_print.update({node_key:node_v_value})
                            else:
                                node_num=self.modify_node_branch[node_key]
                                node_num-=1
                                node_v_value=self.results_DC[node_num]
                                self.results_DC_print.update({node_key:node_v_value})
                    else:
                        break
                        
        
        while i<self.rows:
            i+=1
            self.results_DC_print.update({})
        
        #a=self.rows
        #print(a)
        self.results_DC_print_v=self.results_DC_print.copy()
        j=0
        self.results_DC_print_other={}
        for node_key in self.modify_node_branch.keys():
            if j<self.rows:
                j+=1
            else:
                j+=1
                node_num=self.modify_node_branch[node_key]
                node_num-=1
                value=self.results_DC[node_num]
                self.results_DC_print_other.update({node_key:value})
        '''
    def ac_solve_net(self):
        #ac simulation
        is_op=0
        u0={}
        u1={}
        vd0={}
        vd1={}
        vs0={}
        vs1={}
        vg0={}
        vg1={}
        iter_flag=0
        iter_cnt=0
        flag_ac_append=0
        self.AC_swep_result={}
        self.AC_swep_result_phase={}
        self.ac_converge_threshold=0.0005
        #print(self.ac_samp_num)
        self.ac_swep_list=np.arange(self.ac_swep_start,self.ac_swep_end+self.ac_samp_num,1,dtype=float)
        #self.ac_swep_list = np.linspace(self.ac_swep_start,self.ac_swep_end,self.ac_samp_num,dtype=float)
        #print(self.ac_swep_list)
        for omega in self.ac_swep_list:
            flag_iter=0
            while ((flag_iter<=1))or(flag_iter_end==0):
                flag_iter_end=1
                #end iter
                for u_key,u_val in u0.items():
                    if (abs(u_val-u1[u_key])<=self.ac_converge_threshold) :
                        end=1
                    else:
                        end=0
                    flag_iter_end=flag_iter_end and end
                for vd_key in vd0.keys():
                    if (abs(vd0[vd_key]-vd1[vd_key])>=self.ac_converge_threshold) or (abs(vs0[vd_key]-vs1[vd_key])>=self.ac_converge_threshold) or(abs(vg0[vd_key]-vg1[vd_key])>=self.ac_converge_threshold):
                        end =0
                    else:
                        end =1
                    flag_iter_end=flag_iter_end and end
                flag_iter+=1
                self.add_branch_ac()
                self.MNA_ac=np.zeros ((self.modify_rows,self.modify_rows))
                self.MNA_ac = np.array(self.MNA_ac,dtype=complex)
                self.RHS_ac=np.zeros(self.modify_rows)
                self.RHS_ac = np.array(self.RHS_ac,dtype=complex)
                #C element ac no equal to dc
                '''
                if (len(self.sim_Parser.dict_c)!=0):
                    for c_key in self.sim_Parser.dict_c.keys():
                        node1=self.sim_Parser.dict_c[c_key][1]
                        node2=self.sim_Parser.dict_c[c_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        c_branch_num=self.modify_node_branch[c_key]
                        self.MNA_ac=np.delete(self.MNA_ac,c_branch_num,0)
                        self.MNA_ac=np.delete(self.MNA_ac,c_branch_num,1)
                        self.RHS_ac=np.delete(self.RHS_ac,c_branch_num,0)
                        ## get c_key out of modify_branch for ac don't have C
                        i=0
                        minus_flag=0
                        self.modify_node_branch_ac=self.modify_node_branch.copy()
                        for node_key in self.modify_node_branch_ac.keys():
                            #print(node_key)
                            if i< self.modify_rows:
                                i+=1
                                if (node_key==c_key):
                                    minus_flag=1
                                    #del self.modify_node_branch_dc[c_key]                                
                                else:
                                    if(minus_flag==0):
                                        pass
                                    else:
                                        node_num=self.modify_node_branch_ac[node_key]
                                        self.modify_node_branch_ac[node_key]=node_num-1
                                        node_num=self.modify_node_branch[node_key]
                                        self.modify_node_branch[node_key]=node_num-1                                           
                            else:
                                break
                '''
                #C and L ac stamp
                #c
                if (len(self.sim_Parser.dict_c)!=0):
                    for c_key in self.sim_Parser.dict_c.keys():
                        node1=self.sim_Parser.dict_c[c_key][1]
                        node2=self.sim_Parser.dict_c[c_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        c_value=self.sim_Parser.dict_c[c_key][0]
                        self.C_AC_mna_constr(node1_num,node2_num,c_key,c_value,omega,self.MNA_ac)
                #l
                if (len(self.sim_Parser.dict_l)!=0):
                    for l_key in self.sim_Parser.dict_l.keys():
                        node1=self.sim_Parser.dict_l[l_key][1]
                        node2=self.sim_Parser.dict_l[l_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        l_value=self.sim_Parser.dict_l[l_key][0]
                        self.L_AC_mna_constr(node1_num,node2_num,l_key,l_value,omega,self.MNA_ac)
                #R
                if (len(self.sim_Parser.dict_r)!=0):
                    #r_length=len(self.sim_Parser.dict_r)
                    #i=0
                    for r_key in self.sim_Parser.dict_r.keys():
                        r_value=self.sim_Parser.dict_r[r_key][0]
                        #print(r_value)
                        ##node for N+ N-
                        node1=self.sim_Parser.dict_r[r_key][1]
                        node2=self.sim_Parser.dict_r[r_key][2]
                        ##get node num to be np's index
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        #print(node1_num,node2_num)
                        self.R_mna_constr(node1_num,node2_num,r_value,self.MNA_ac)
                        #print (self.MNA_dc)
                        #print(node1,node2)
                #V
                if (len(self.sim_Parser.dict_v)!=0):
                    for v_key in self.sim_Parser.dict_v.keys():
                        #print (self.sim_Parser.dict_v[v_key])
                        v_value=self.sim_Parser.dict_v[v_key][0]
                        node1=self.sim_Parser.dict_v[v_key][1]
                        node2=self.sim_Parser.dict_v[v_key][2]
                        #print (node1)
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        #np.c_(self.MNA_dc,'0')
                        #np.r_(self.MNA_dc,0)
                        #print(self.sim_Parser.dict_v[v_key])
                        self.V_mna_constr(node1_num,node2_num,v_key,v_value,self.MNA_ac,self.RHS_ac)
                        #print (self.MNA_dc)
                #I
                if (len(self.sim_Parser.dict_i)!=0):
                    for i_key in self.sim_Parser.dict_i.keys():
                        i_value=self.sim_Parser.dict_i[i_key][0]
                        node1=self.sim_Parser.dict_i[i_key][1]
                        node2=self.sim_Parser.dict_i[i_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        self.I_mna_constr(node1_num,node2_num,i_value,self.RHS_ac)
                        #print (self.MNA_dc)
                #G
                if (len(self.sim_Parser.dict_G)!=0):
                    for g_key in self.sim_Parser.dict_G.keys():
                        node1=self.sim_Parser.dict_G[g_key][0]
                        node2=self.sim_Parser.dict_G[g_key][1]
                        nc1=self.sim_Parser.dict_G[g_key][2]
                        nc2=self.sim_Parser.dict_G[g_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        g_value=self.sim_Parser.dict_G[g_key][4]
                        self.G_mna_constr(node1_num,node2_num,nc1_num,nc2_num,g_value,self.MNA_ac)
                        #print (self.MNA_dc)
                #E
                if (len(self.sim_Parser.dict_E)!=0):
                    for e_key in self.sim_Parser.dict_E.keys():
                        node1=self.sim_Parser.dict_E[e_key][0]
                        node2=self.sim_Parser.dict_E[e_key][1]
                        nc1=self.sim_Parser.dict_E[e_key][2]
                        nc2=self.sim_Parser.dict_E[e_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        e_value=self.sim_Parser.dict_E[e_key][4]
                        self.E_mna_constr(node1_num,node2_num,nc1_num,nc2_num,e_key,e_value,self.MNA_ac)
                        #print (self.MNA_dc)
                #F
                if (len(self.sim_Parser.dict_F)!=0):
                    for f_key in self.sim_Parser.dict_F.keys():
                        node1=self.sim_Parser.dict_F[f_key][0]
                        node2=self.sim_Parser.dict_F[f_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        v_name=self.sim_Parser.dict_v[f_key][2]
                        nc1=self.sim_Parser.dict_v[v_name][1]
                        nc2=self.sim_Parser.dict_v[v_name][2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        f_value=self.sim_Parser.dict_F[f_key][3]
                        self.F_mna_constr(node1_num,node2_num,nc1_num,nc2_num,f_key,f_value,0,self.MNA_ac)
                        #print (self.MNA_dc)
                #H
                if(len(self.sim_Parser.dict_H)!=0):
                    for h_key in self.sim_Parser.dict_H.keys():
                        node1=self.sim_Parser.dict_H[h_key][0]
                        node2=self.sim_Parser.dict_H[h_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        v_name=self.sim_Parser.dict_v[h_key][2]
                        nc1=self.sim_Parser.dict_v[v_name][1]
                        nc2=self.sim_Parser.dict_v[v_name][2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        h_value=self.sim_Parser.dict_H[h_key][3]
                        self.H_mna_constr(node1_num,node2_num,nc1_num,nc2_num,h_key,v_name,h_value,0,self.MNA_ac)
                #diode
                if (len(self.sim_Parser.dict_diode)!=0):
                    for diode_key in self.sim_Parser.dict_diode.keys():
                        if (u0=={})or(u1=={}):
                            for diode_key in self.sim_Parser.dict_diode.keys():
                                u0.update({diode_key:0})
                                u1.update({diode_key:0})
                        iter_flag+=1
                        node1=self.sim_Parser.dict_diode[diode_key][0]
                        node2=self.sim_Parser.dict_diode[diode_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        self.node_D.update({diode_key:{'node1':node1,'node2':node2}})
                        self.MNA_ac,self.RHS_ac=self.D_mna_constr(node1_num,node2_num,u1[diode_key],self.MNA_ac,self.RHS_ac)
                # simulation part
                if iter_flag==0:
                    while is_op>0:
                        pass
                    if 'gnd' in self.modify_node_branch.keys():
                            num=self.modify_node_branch['gnd']
                    else:
                        num=self.modify_node_branch['0']   
                    ## --------------slove part---------------------##
                    self.MNA_ac_solve,self.RHS_ac_solve=self.delete_x(self.MNA_ac,self.RHS_ac,num)
                    self.results_ac=np.linalg.solve(self.MNA_ac_solve,self.RHS_ac_solve)
                    ##-------end---------------#
                    self.modify_node_branch_num_change=self.node_num_change(self.modify_node_branch)
                    #print (self.modify_node_branch_num_change)
                    self.modify_node_branch_no_gnd=self.modify_node_branch_num_change.copy()
                    self.modify_node_branch_copy=self.modify_node_branch.copy()
                    if 'gnd' in self.modify_node_branch_no_gnd.keys():
                        del self.modify_node_branch_no_gnd['gnd']
                    else:
                        del self.modify_node_branch_no_gnd['0']
                    #get a node dict without 0 & num correct
                    #???why need this
                    self.modify_node_branch.clear()
                else:
                    iter_cnt+=1
                    if 'gnd' in self.modify_node_branch.keys():
                        num=self.modify_node_branch['gnd']
                    else:
                        num=self.modify_node_branch['0']
                    ## --------------slove part---------------------##
                    self.MNA_ac_solve,self.RHS_ac_solve=self.delete_x(self.MNA_ac,self.RHS_ac,num)
                    self.results_ac=np.linalg.solve(self.MNA_ac_solve,self.RHS_ac_solve)
                    ##-------end---------------#
                    self.modify_node_branch_num_change=self.node_num_change(self.modify_node_branch)
                    #print (self.modify_node_branch_num_change)
                    self.modify_node_branch_no_gnd=self.modify_node_branch_num_change.copy()
                    self.modify_node_branch_copy=self.modify_node_branch.copy()
                    if 'gnd' in self.modify_node_branch_no_gnd.keys():
                        del self.modify_node_branch_no_gnd['gnd']
                    else:
                        del self.modify_node_branch_no_gnd['0']
                    ## value for u0 u1
                    for diode_key in self.sim_Parser.dict_diode.keys():
                        u0[diode_key]=u1[diode_key]
                        #print(diode_key)
                        #print(self.node_D)
                        #print (self.node_D[diode_key])
                        if (self.node_D[diode_key]['node1']=='0') or (self.node_D[diode_key]['node1']=='gnd'):
                            u1[diode_key] =-self.results_ac[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node2']]]
                        elif (self.node_D[diode_key]['node2']=='0') or (self.node_D[diode_key]['node2']=='gnd'):
                            u1[diode_key] = self.results_ac[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node1']]]
                        else:
                            u1[diode_key] = self.results_ac[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node1']]]-self.results_ac[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node2']]]
                    self.modify_node_branch.clear()
            for node_key in self.modify_node_branch_no_gnd.keys():
                if len(self.AC_swep_result)!=0:
                    if flag_ac_append:
                        self.AC_swep_result[node_key].append(self.results_ac[self.modify_node_branch_no_gnd[node_key]])
                        self.AC_swep_result_phase[node_key].append(math.atan(np.imag(self.results_ac[self.modify_node_branch_no_gnd[node_key]])/np.real(self.results_ac[self.modify_node_branch_no_gnd[node_key]])))
                    else:
                        self.AC_swep_result.update({node_key:[self.results_ac[self.modify_node_branch_no_gnd[node_key]]]})
                        self.AC_swep_result_phase.update({node_key:[math.atan(np.imag(self.results_ac[self.modify_node_branch_no_gnd[node_key]])/np.real(self.results_ac[self.modify_node_branch_no_gnd[node_key]]))]})
                else:
                    self.AC_swep_result={'0':[0],node_key:[self.results_ac[self.modify_node_branch_no_gnd[node_key]]]}
                    self.AC_swep_result_phase={'0':[0],node_key:[math.atan(np.imag(self.results_ac[self.modify_node_branch_no_gnd[node_key]])/np.real(self.results_ac[self.modify_node_branch_no_gnd[node_key]]))]}
            flag_ac_append=1
            self.AC_swep_result['0'].append(0)
            self.AC_swep_result_phase['0'].append(0)
        #print(self.AC_swep_result)
        self.output_print()
    #def solve__net_tran(self,method,h):
    #    self.tran_mna_matrix()
    def tran_solve_net(self):
        #tran simulation
        ##tran model set for h_step and method
        method='BE'
        h_step='1m'
        self.step_value = turn_unit.solve_unit(h_step) #h
        self.step_value = self.sim_Parser.dict_command['tran'][0]
        #param get
        flag_tran_y_append=0
        pw_cnt=0
        pw_r_cnt=0
        pw_f_cnt=0
        per_cnt=1
        per_r_cnt=1
        per_f_cnt=1
        u0={}
        u1={}
        ud0={}
        ud1={}
        vs0={}
        vs1={}
        vg0={}
        vg1={}
        self.tran_converge_threshold=0.0005
        self.tran_mos_converge_threshold=0.005
        self.tran_method=method
        self.tran_option_select=self.tran_simulator_option[method]
        self.tran_option_select=self.tran_simulator_option[method]
        #print (self.step_value)
        #self.tran_mna_matrix()
        self.tran_plot_list=np.arange(0,self.sim_Parser.dict_command['tran'][1],self.sim_Parser.dict_command['tran'][0],dtype=float)
        self.tran_swep_list=np.arange(0,self.sim_Parser.dict_command['tran'][1],self.step_value,dtype=float)
        #print(self.step_value)
        #print(len(self.tran_swep_list))
        #get v source
        for v_key in self.sim_Parser.dict_v.keys():
            if self.sim_Parser.dict_v[v_key][0]=='pulse':
                #print(self.sim_Parser.dict_v[v_key])
                for t_cnt in self.tran_swep_list:
                    if v_key in self.v_value.keys():
                        if t_cnt >= self.sim_Parser.dict_v[v_key][5]+self.sim_Parser.dict_v[v_key][6]*per_cnt+(self.sim_Parser.dict_v[v_key][9]-self.sim_Parser.dict_v[v_key][6])*(per_cnt-1):
                            v_val_estp = self.sim_Parser.dict_v[v_key][4]#high value
                            pw_cnt +=  self.step_value
                            #print(t_cnt,per_cnt,(self.sim_Parser.dict_v[v_key][5]+(self.sim_Parser.dict_v[v_key][9])*(per_r_cnt-1)),v_val_estp,'high')
                            if pw_cnt >= self.sim_Parser.dict_v[v_key][8]:
                                pw_cnt = 0
                                per_cnt += 1
                        elif t_cnt >= (self.sim_Parser.dict_v[v_key][5]+(self.sim_Parser.dict_v[v_key][9])*(per_r_cnt-1)):
                            v_val_estp = ((self.sim_Parser.dict_v[v_key][4] - self.sim_Parser.dict_v[v_key][3])/self.sim_Parser.dict_v[v_key][6])*(t_cnt-self.sim_Parser.dict_v[v_key][5]-(self.sim_Parser.dict_v[v_key][9])*(per_r_cnt-1))
                            pw_r_cnt +=  self.step_value
                            #print(t_cnt,pw_r_cnt,(self.sim_Parser.dict_v[v_key][5]+(self.sim_Parser.dict_v[v_key][9])*(per_r_cnt-1)),v_val_estp,'rise')
                            if pw_r_cnt >= self.sim_Parser.dict_v[v_key][6]:
                                pw_r_cnt = 0
                                per_r_cnt += 1
                        elif t_cnt >= (self.sim_Parser.dict_v[v_key][5]+(self.sim_Parser.dict_v[v_key][6]+self.sim_Parser.dict_v[v_key][7])*per_f_cnt+(self.sim_Parser.dict_v[v_key][9])*(per_f_cnt-1)):
                            v_val_estp = self.sim_Parser.dict_v[v_key][4]+((self.sim_Parser.dict_v[v_key][3] - self.sim_Parser.dict_v[v_key][4])/self.sim_Parser.dict_v[v_key][6])*(t_cnt-(self.sim_Parser.dict_v[v_key][5]+(self.sim_Parser.dict_v[v_key][6]+self.sim_Parser.dict_v[v_key][8])*per_f_cnt+(self.sim_Parser.dict_v[v_key][9]-self.sim_Parser.dict_v[v_key][6]-self.sim_Parser.dict_v[v_key][8])*(per_f_cnt-1)))
                            pw_f_cnt +=  self.step_value
                            #print(t_cnt,per_f_cnt,(self.sim_Parser.dict_v[v_key][5]+(self.sim_Parser.dict_v[v_key][6]+self.sim_Parser.dict_v[v_key][7])*per_f_cnt+(self.sim_Parser.dict_v[v_key][9])*(per_f_cnt-1)),v_val_estp,'fall')
                            #print(pw_f_cnt)
                            if pw_f_cnt >= self.sim_Parser.dict_v[v_key][7]:
                                pw_f_cnt = 0
                                per_f_cnt += 1
                        else:
                            v_val_estp = self.sim_Parser.dict_v[v_key][3]
                            #print(t_cnt,v_val_estp,'zero')
                        self.v_value[v_key].append(v_val_estp)
                    else:
                        v_val_estp = self.sim_Parser.dict_v[v_key][3]
                        self.v_value.update({v_key:[v_val_estp]})
            elif self.sim_Parser.dict_v[v_key][0]=='sin':
                #print(self.sim_Parser.dict_v[v_key])
                self.v_value.update({v_key:float(self.sim_Parser.dict_v[v_key][4])*np.sin(2*np.pi*float(self.sim_Parser.dict_v[v_key][5])*self.tran_swep_list)+float(self.sim_Parser.dict_v[v_key][3])})    
            else:
                for t_cnt in self.tran_swep_list:
                    if v_key in self.v_value.keys():
                        self.v_value[v_key].append(self.sim_Parser.dict_v[v_key][0])
                    else:
                        self.v_value.update({v_key:[self.sim_Parser.dict_v[v_key][0]]}) 
        #print(len(self.tran_swep_list))
        #print(self.v_value)
        #sim
        v0={}
        i0={}
        flag_vi_iter=0
        iter_flag=0 #for nonlinear model
        is_op =0 #for E
        #flag_iter=0
        flag_iter_end=1
        
        self.TRAN_y_axis={}
        # give the source value not constant
        t_step_cnt=0
        iter_cnt=0
        #print('hi')
        #print(self.v_value)
        #print(self.tran_swep_list)
        for t_step in self.tran_swep_list:
            #flag=0
            #print('hi')
            #print(flag_tran_y_append)
            #flag_vi_iter for update u0,i0 for MNA stamp solve C/L
            if flag_vi_iter==0:
                for c_key in self.sim_Parser.dict_c.keys():
                    v0.update({c_key:0})
                    i0.update({c_key:0})
                for l_key in self.sim_Parser.dict_l.keys():
                    v0.update({l_key:0})
                    i0.update({l_key:0})
            else:
                for c_key in self.sim_Parser.dict_c.keys():
                    #print (self.sim_Parser.dict_c[c_key])
                    #print (flag_vi_iter)
                    #print (self.TRAN_y_axis)
                    #a=self.TRAN_y_axis['2']
                    #print(a)
                    #print (self.TRAN_y_axis[self.sim_Parser.dict_c[c_key][1]])
                    tran_node1 = self.TRAN_y_axis[self.sim_Parser.dict_c[c_key][1]]
                    #print (tran_node1[-1])
                    #print (self.TRAN_y_axis[0])
                    tran_node2 = self.TRAN_y_axis[self.sim_Parser.dict_c[c_key][2]]
                    #print(tran_node1)                    
                    v0[c_key] = tran_node1[-1]-tran_node2[-1]
                    tran_i = self.TRAN_y_axis[c_key]
                    i0[c_key] = tran_i[-1]
                for l_key in self.sim_Parser.dict_l.keys():
                    tran_node1 = self.TRAN_y_axis[self.sim_Parser.dict_l[l_key][1]]
                    tran_node2 = self.TRAN_y_axis[self.sim_Parser.dict_l[l_key][2]]
                    v0[l_key] = tran_node1[-1]-tran_node2[-1]
                    tran_i = self.TRAN_y_axis[l_key]
                    i0[l_key] = tran_i[-1]
            flag_vi_iter=1
            flag_iter=0            
            #while ((flag<=1) or (if_iter_end==0)):
            ## inner loop
            # flag_iter&flag_iter_end
            #??? flag_iter ???<1 or <=1
            while ((flag_iter<=1))or(flag_iter_end==0):
                #print(t_step_cnt)
                flag_iter_end=1
                #end iter
                for u_key,u_val in u0.items():
                    if (abs(u_val-u1[u_key])<=self.tran_converge_threshold):
                        end=1
                        #print('1')
                        #print(u_val,u1[u_key])
                        #print(u_val-u1[u_key])
                        #print('hello')
                    else:
                        end=0
                        #print('0')
                        #print('hi')
                        #print(u_val-u1[u_key])
                    flag_iter_end=flag_iter_end and end
                #mos 
                for ud_key,ud_val in ud0.items():
                    flag_iter_end=1
                    if (abs(ud0[ud_key]-ud1[ud_key])>=self.tran_mos_converge_threshold) or (abs(vs0[ud_key]-vs1[ud_key])>=self.tran_mos_converge_threshold) or(abs(vg0[ud_key]-vg1[ud_key])>=self.tran_mos_converge_threshold) :
                        end=0
                    else:
                        end=1
                    flag_iter_end=flag_iter_end and end
                #print (flag_iter_end)
                #print(flag_iter)
                #print(ud1,ud0,self.v_value['vin'][t_step_cnt])
                #need flag iter to excute one loop
                flag_iter+=1
                #print(flag_iter)
                if flag_iter>1000:
                    break
                #tran mna 
                self.add_branch()
                #print(self.modify_node_branch)
                self.MNA_tran=np.zeros ((self.modify_rows,self.modify_rows))
                self.RHS_tran=np.zeros(self.modify_rows)
                #r
                if (len(self.sim_Parser.dict_r)!=0):
                #r_length=len(self.sim_Parser.dict_r)
                #i=0
                    for r_key in self.sim_Parser.dict_r.keys():
                        r_value=self.sim_Parser.dict_r[r_key][0]
                        #print(r_value)
                        ##node for N+ N-
                        node1=self.sim_Parser.dict_r[r_key][1]
                        node2=self.sim_Parser.dict_r[r_key][2]
                        ##get node num to be np's index
                        node1_num=self.sim_Parser.dict_node[node1]
                        node2_num=self.sim_Parser.dict_node[node2]
                        #print(node1_num,node2_num)
                        self.R_mna_constr(node1_num,node2_num,r_value,self.MNA_tran)
                        #print (self.MNA_dc)
                        #print(node1,node2)
                #V
                if (len(self.sim_Parser.dict_v)!=0):
                    for v_key in self.sim_Parser.dict_v.keys():
                        #print (self.sim_Parser.dict_v[v_key])
                        #v_value=self.sim_Parser.dict_v[v_key][0]
                        node1=self.sim_Parser.dict_v[v_key][1]
                        node2=self.sim_Parser.dict_v[v_key][2]
                        #print (self.sim_Parser.dict_v[v_key],v_key)
                        #print(self.modify_node_branch)
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        #np.c_(self.MNA_dc,'0')
                        #np.r_(self.MNA_dc,0)
                        #print(self.sim_Parser.dict_v[v_key])
                        #print(self.v_value[v_key][t_step_cnt])
                        #print(t_step_cnt)
                        self.V_mna_constr(node1_num,node2_num,v_key,self.v_value[v_key][t_step_cnt],self.MNA_tran,self.RHS_tran)
                        #print (self.MNA_dc)
                #I
                if (len(self.sim_Parser.dict_i)!=0):
                    for i_key in self.sim_Parser.dict_i.keys():
                        i_value=self.sim_Parser.dict_i[i_key][0]
                        node1=self.sim_Parser.dict_i[i_key][1]
                        node2=self.sim_Parser.dict_i[i_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        self.I_mna_constr(node1_num,node2_num,i_value,self.RHS_tran)
                        #print (self.MNA_dc)
                #G
                if (len(self.sim_Parser.dict_G)!=0):
                    for g_key in self.sim_Parser.dict_G.keys():
                        node1=self.sim_Parser.dict_G[g_key][0]
                        node2=self.sim_Parser.dict_G[g_key][1]
                        nc1=self.sim_Parser.dict_G[g_key][2]
                        nc2=self.sim_Parser.dict_G[g_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        g_value=self.sim_Parser.dict_G[g_key][4]
                        self.G_mna_constr(node1_num,node2_num,nc1_num,nc2_num,g_value,self.MNA_tran)
                        #print (self.MNA_dc)
                #E
                if (len(self.sim_Parser.dict_E)!=0):
                    for e_key in self.sim_Parser.dict_E.keys():
                        node1=self.sim_Parser.dict_E[e_key][0]
                        node2=self.sim_Parser.dict_E[e_key][1]
                        nc1=self.sim_Parser.dict_E[e_key][2]
                        nc2=self.sim_Parser.dict_E[e_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        e_value=self.sim_Parser.dict_E[e_key][4]
                        self.E_mna_constr(node1_num,node2_num,nc1_num,nc2_num,e_key,e_value,self.MNA_tran)
                        #print (self.MNA_dc)
                #F
                if (len(self.sim_Parser.dict_F)!=0):
                    for f_key in self.sim_Parser.dict_F.keys():
                        node1=self.sim_Parser.dict_F[f_key][0]
                        node2=self.sim_Parser.dict_F[f_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        v_name=self.sim_Parser.dict_v[f_key][2]
                        nc1=self.sim_Parser.dict_v[v_name][1]
                        nc2=self.sim_Parser.dict_v[v_name][2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        f_value=self.sim_Parser.dict_F[f_key][3]
                        self.F_mna_constr(node1_num,node2_num,nc1_num,nc2_num,f_key,f_value,0,self.MNA_tran)
                        #print (self.MNA_dc)
                #H
                if(len(self.sim_Parser.dict_H)!=0):
                    for h_key in self.sim_Parser.dict_H.keys():
                        node1=self.sim_Parser.dict_H[h_key][0]
                        node2=self.sim_Parser.dict_H[h_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        v_name=self.sim_Parser.dict_v[h_key][2]
                        nc1=self.sim_Parser.dict_v[v_name][1]
                        nc2=self.sim_Parser.dict_v[v_name][2]
                        nc1_num=self.modify_node_branch[nc1]
                        nc2_num=self.modify_node_branch[nc2]
                        h_value=self.sim_Parser.dict_H[h_key][3]
                        self.H_mna_constr(node1_num,node2_num,nc1_num,nc2_num,h_key,v_name,h_value,0,self.MNA_tran)
                #c
                if (len(self.sim_Parser.dict_c)!=0):
                    for c_key in self.sim_Parser.dict_c.keys():
                        node1=self.sim_Parser.dict_c[c_key][1]
                        node2=self.sim_Parser.dict_c[c_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        c_value=self.sim_Parser.dict_c[c_key][0]
                        self.C_TRAN_mna_constr(node1_num,node2_num,c_key,c_value,v0[c_key],i0[c_key],self.tran_option_select,self.MNA_tran,self.RHS_tran)
                #l
                if (len(self.sim_Parser.dict_l)!=0):
                    for l_key in self.sim_Parser.dict_l.keys():
                        node1=self.sim_Parser.dict_l[l_key][1]
                        node2=self.sim_Parser.dict_l[l_key][2]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        l_value=self.sim_Parser.dict_l[l_key][0]
                        self.L_TRAN_mna_constr(node1_num,node2_num,l_key,l_value,v0[l_key],i0[l_key],self.tran_option_select,self.MNA_tran,self.RHS_tran)
                #diode
                if (len(self.sim_Parser.dict_diode)!=0):
                    for diode_key in self.sim_Parser.dict_diode.keys():
                        #print(diode_key)
                        if (u0=={})or(u1=={}):
                            for diode_key_2 in self.sim_Parser.dict_diode.keys():
                                u0.update({diode_key_2:0})
                                u1.update({diode_key_2:0})
                        iter_flag+=1
                        
                        node1=self.sim_Parser.dict_diode[diode_key][0]
                        node2=self.sim_Parser.dict_diode[diode_key][1]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        #print(node1)
                        self.node_D.update({diode_key:{'node1':node1,'node2':node2}})
                        #print(self.node_D)
                        self.MNA_tran,self.RHS_tran=self.D_mna_constr(node1_num,node2_num,u1[diode_key],self.MNA_tran,self.RHS_tran)
                #MOS
                if (len(self.sim_Parser.dict_mos)!=0):
                    for mos_key in self.sim_Parser.dict_mos.keys():
                        #initial
                        if vg0=={}:
                            for mos_key2 in self.sim_Parser.dict_mos.keys():
                                if self.sim_Parser.dict_mos[mos_key2][0]=='nmos':
                                    ud0.update({mos_key2:0})
                                    vg0.update({mos_key2:0})
                                    vs0.update({mos_key2:0})
                                    ud1.update({mos_key2:1.3})
                                    vg1.update({mos_key2:1})
                                    vs1.update({mos_key2:0})
                                else:
                                    ud0.update({mos_key2:0})
                                    vg0.update({mos_key2:0})
                                    vs0.update({mos_key2:0})
                                    ud1.update({mos_key2:1.3})
                                    vg1.update({mos_key2:1})
                                    vs1.update({mos_key2:1.8})  
                        node1=self.sim_Parser.dict_mos[mos_key][1]
                        node2=self.sim_Parser.dict_mos[mos_key][2]
                        node3=self.sim_Parser.dict_mos[mos_key][3]
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        node3_num=self.modify_node_branch[node3]
                        self.node_M.update({mos_key:{'noded':node1,'nodeg':node2,'nodes':node3}})
                        w_l=float(self.sim_Parser.dict_mos[mos_key][5])/self.sim_Parser.dict_mos[mos_key][6]
                        iter_flag+=1
                        if (self.sim_Parser.dict_mos[mos_key][0]=='nmos'):
                            self.NMOS_mna_constr(node1_num,node2_num,node3_num,ud1[mos_key],vs1[mos_key],vg1[mos_key],w_l,self.MNA_tran,self.RHS_tran)
                        else:
                            self.PMOS_mna_constr(node1_num,node2_num,node3_num,ud1[mos_key],vs1[mos_key],vg1[mos_key],w_l,self.MNA_tran,self.RHS_tran)
                ##end mna 
                #print (self.MNA_tran,'\n',self.RHS_tran,'\n',self.modify_node_branch)
                if iter_flag==0:
                    #print('hi')
                    while is_op >0:
                        pass
                    if 'gnd' in self.modify_node_branch.keys():
                        num=self.modify_node_branch['gnd']
                    else:
                        num=self.modify_node_branch['0']
                    ## --------------slove part---------------------##
                    self.MNA_tran_solve,self.RHS_tran_solve=self.delete_x(self.MNA_tran,self.RHS_tran,num)
                    self.results_tran=np.linalg.solve(self.MNA_tran_solve,self.RHS_tran_solve)
                    ##-------end---------------#
                    self.modify_node_branch_num_change=self.node_num_change(self.modify_node_branch)
                    #print (self.modify_node_branch_num_change)
                    self.modify_node_branch_no_gnd=self.modify_node_branch_num_change.copy()
                    self.modify_node_branch_copy=self.modify_node_branch.copy()
                    if 'gnd' in self.modify_node_branch_no_gnd.keys():
                        del self.modify_node_branch_no_gnd['gnd']
                    else:
                        del self.modify_node_branch_no_gnd['0']
                    #get a node dict without 0 & num correct
                    #???why need this
                    self.modify_node_branch.clear()
                else:
                    iter_cnt+=1
                    if 'gnd' in self.modify_node_branch.keys():
                        num=self.modify_node_branch['gnd']
                    else:
                        num=self.modify_node_branch['0']
                    ## --------------slove part---------------------##
                    self.MNA_tran_solve,self.RHS_tran_solve=self.delete_x(self.MNA_tran,self.RHS_tran,num)
                    self.results_tran=np.linalg.solve(self.MNA_tran_solve,self.RHS_tran_solve)
                    ##-------end---------------#
                    self.modify_node_branch_num_change=self.node_num_change(self.modify_node_branch)
                    #print (self.modify_node_branch_num_change)
                    self.modify_node_branch_no_gnd=self.modify_node_branch_num_change.copy()
                    self.modify_node_branch_copy=self.modify_node_branch.copy()
                    if 'gnd' in self.modify_node_branch_no_gnd.keys():
                        del self.modify_node_branch_no_gnd['gnd']
                    else:
                        del self.modify_node_branch_no_gnd['0']
                    ## value for u0 u1
                    for diode_key in self.sim_Parser.dict_diode.keys():
                        u0[diode_key]=u1[diode_key]
                        #print(diode_key)
                        #print(self.node_D)
                        #print (self.node_D[diode_key])
                        if (self.node_D[diode_key]['node1']=='0') or (self.node_D[diode_key]['node1']=='gnd'):
                            u1[diode_key] =-self.results_tran[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node2']]]
                        elif (self.node_D[diode_key]['node2']=='0') or (self.node_D[diode_key]['node2']=='gnd'):
                            u1[diode_key] = self.results_tran[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node1']]]
                        else:
                            u1[diode_key] = self.results_tran[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node1']]]-self.results_tran[self.modify_node_branch_no_gnd[self.node_D[diode_key]['node2']]]
                    ## mos update
                    for mos_key in self.sim_Parser.dict_mos.keys():
                        ud0[mos_key] = ud1[mos_key]
                        vs0[mos_key] = vs1[mos_key]
                        vg0[mos_key] = vg1[mos_key]
                        if (self.node_M[mos_key]['noded']=='0') or (self.node_M[mos_key]['noded']=='gnd'):
                            ud1[mos_key] =0
                            vs1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodes']]]
                            vg1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodeg']]]
                        elif (self.node_M[mos_key]['nodes']=='0') or (self.node_M[mos_key]['nodes']=='gnd'):
                            ud1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['noded']]]
                            vs1[mos_key] =0
                            vg1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodeg']]]
                        elif (self.node_M[mos_key]['nodeg']=='0') or (self.node_M[mos_key]['nodeg']=='gnd'):
                            ud1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['noded']]]
                            vs1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodes']]]
                            vg1[mos_key] =0
                        else:
                            ud1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['noded']]]
                            vs1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodes']]]
                            vg1[mos_key] =self.results_tran[self.modify_node_branch_no_gnd[self.node_M[mos_key]['nodeg']]]
                    for mos_key in self.sim_Parser.dict_mos.keys():
                        if ud1[mos_key]<0:
                            end=0
                            flag_iter_end=flag_iter_end and 0
                    self.modify_node_branch.clear()
                ## result ---->node  need transfer the node's index for node 0 not in the first line
                ##put the result into the tran_y_axis list 
            for node_key in self.modify_node_branch_no_gnd.keys():
                if len(self.TRAN_y_axis)!=0:
                    if flag_tran_y_append:
                        self.TRAN_y_axis[node_key].append(self.results_tran[self.modify_node_branch_no_gnd[node_key]])
                        self.TRAN_y_axis['0'].append(0)
                    else:
                        #print (flag_tran_y_append)
                        #print (self.modify_node_branch_no_gnd)
                        #print(node_key)
                        #print (self.TRAN_y_axis)
                        #print (self.results_tran[self.modify_node_branch_no_gnd[node_key]])
                        self.TRAN_y_axis.update({node_key:[self.results_tran[self.modify_node_branch_no_gnd[node_key]]]})
                else:
                    self.TRAN_y_axis={'0':[0],node_key:[self.results_tran[self.modify_node_branch_no_gnd[node_key]]]}
            flag_tran_y_append=1
            t_step_cnt+=1
            #print(self.TRAN_y_axis['0'])
            #print(t_step_cnt)     
        #print(self.TRAN_y_axis)
        self.output_print()

        '''
        if 'dc' in self.sim_Parser.dict_command.keys():
            self.dc_mna_matrix()
            if 'gnd' in self.modify_node_branch.keys():
                num=self.modify_node_branch['gnd']
            else:
                num=self.modify_node_branch['0']
            #print(num)
            ##??? doesn't matter delect which row
            #print(self.RHS_dc,self.MNA_dc)
            self.MNA_dc_solve,self.RHS_dc_solve=self.delete_x(self.MNA_dc,self.RHS_dc,num)
            #print (self.MNA_dc_solve,self.RHS_dc_solve)
            self.results_DC = np.linalg.solve(self.MNA_dc_solve,self.RHS_dc_solve)
            #print (self.results_DC)
            #print (self.modify_node_branch)
            #lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(self.MNA_dc_solve))
            #x=lu.solve(self.RHS_dc_solve)
            #print(x)
            self.modify_node_branch_no_gnd=self.modify_node_branch.copy()
            if 'gnd' in self.modify_node_branch_no_gnd.keys():
                del self.modify_node_branch_no_gnd['gnd']
            else:
                del self.modify_node_branch_no_gnd['0']
            #print(self.modify_node_branch_no_gnd)
            i=0
            minus_flag=0
            #print(self.modify_node_branch)
            self.results_DC_print.update({0:0})
            for node_key in self.modify_node_branch.keys():
                #print(node_key)
                if i< self.rows:
                    i+=1
                    if (node_key=='gnd') or (node_key=='0'):
                        #print('hi')
                        minus_flag = 1
                    else:
                        if (minus_flag==0):
                            #print(minus_flag)
                            #print (node_key)
                            node_num=self.modify_node_branch[node_key]
                            #print (node_num)
                            node_v_value=self.results_DC[node_num]
                            self.results_DC_print.update({node_key:node_v_value})
                        else:
                            node_num=self.modify_node_branch[node_key]
                            node_num-=1
                            node_v_value=self.results_DC[node_num]
                            self.results_DC_print.update({node_key:node_v_value})
                else:
                    break
            
            while i<self.rows
                i+=1
                self.results_DC_print.update({})
            
            #a=self.rows
            #print(a)
            self.results_DC_print_v=self.results_DC_print.copy()
            j=0
            self.results_DC_print_other={}
            for node_key in self.modify_node_branch.keys():
                if j<self.rows:
                    j+=1
                else:
                    j+=1
                    node_num=self.modify_node_branch[node_key]
                    node_num-=1
                    value=self.results_DC[node_num]
                    self.results_DC_print_other.update({node_key:value})
            print('#-----------------print value-------------------#')
            print('node voltage:','\n',self.results_DC_print_v,'\n','other:','\n',self.results_DC_print_other)
        elif 'tran' in self.sim_Parser.dict_command.keys():
            pass
        elif 'ac' in self.sim_Parser.dict_command.keys():
            pass
        else:
            print ('no simulation command')  
        '''      
    def print_matrix(self): 
        self.dc_mna_matrix()
        print('#-----------------print MNA-------------------#')       
        print ('MNA:\n',self.MNA_dc,'\n','RHS:\n',self.RHS_dc,'\n','node index:\n',self.modify_node_branch)    
    ##------------------------------------out plot part------------------------------##
    def output_print(self):
        print('out_put')
        i=0
        ##one figure
        #plt_list={0:'plt_a',1:'plt_a',2:'plt_a',3:'plt_a',4:'plt_a',5:'plt_a',6:'plt_a',7:'plt_a',8:'plt_a'}
        plt_list={0:'plt_a',1:'plt_b',2:'plt_c',3:'plt_d',4:'plt_e',5:'plt_f',6:'plt_g',7:'plt_h',8:'plt_i'}
        self.print_data='out_put'
        for out_key in self.sim_Parser.dict_out_cmd_plot.keys():
            #print(out_key)
            if self.sim_Parser.dict_out_cmd_plot[out_key][0]=='plot':
                #plt.ion()
                plt.ion()
                #p=plt.subplot(1,1,1)
                #print('hi')
                #print(self.sim_Parser.dict_out_cmd_plot[out_key][2][0])
                if self.sim_Parser.dict_out_cmd_plot[out_key][1]=='tran':
                    #print(self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot['v4'][2]])
                    if ',' in self.sim_Parser.dict_out_cmd_plot[out_key][2]:
                        if out_key[0]=='v':
                            i=0
                        elif out_key[0]=='i':
                            i=1
                        plt.figure(plt_list[i])
                        p=plt.subplot(1,1,1)
                        num_sub_a=self.sim_Parser.dict_out_cmd_plot[out_key][2][0]
                        num_sub_b=self.sim_Parser.dict_out_cmd_plot[out_key][2][2]
                        num_len=len(self.TRAN_y_axis[num_sub_a])
                        sub_res_out=[self.TRAN_y_axis[num_sub_a][i]-self.TRAN_y_axis[num_sub_b][i] for i in range(num_len)]
                        #print((self.tran_swep_list,self.TRAN_y_axis[num_sub_a]-self.tran_swep_list,self.TRAN_y_axis[num_sub_a]))
                        print('#----------------TRAN:print output  method:',self.tran_method,'-----------------#')
                        #print (self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                        plt.plot(self.tran_swep_list,sub_res_out,label=out_key)
                        #print(self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                        plt.title('TRAN SIMULATION PLOT')
                        if out_key[0]=='v':
                            plt.xlabel('t/s')
                            plt.ylabel('U/V')
                        elif out_key[0]=='i':
                            plt.xlabel('t/s')
                            plt.ylabel('i/A')
                        handles,lables = p.get_legend_handles_labels()
                        p.legend(handles[::-1],lables[::-1])
                        
                    else:
                        if out_key[0]=='v':
                            i=0
                        elif out_key[0]=='i':
                            i=1
                        plt.figure(plt_list[i])
                        p=plt.subplot(1,1,1)
                        print('#----------------TRAN:print output  method:',self.tran_method,'-----------------#')
                        #print (self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                        plt.plot(self.tran_swep_list,self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]],label=out_key)
                        #print(self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                        plt.title('TRAN SIMULATION PLOT')
                        if out_key[0]=='v':
                            plt.xlabel('t/s')
                            plt.ylabel('U/V')
                        elif out_key[0]=='i':
                            plt.xlabel('t/s')
                            plt.ylabel('i/A')
                        handles,lables = p.get_legend_handles_labels()
                        p.legend(handles[::-1],lables[::-1])
                        
                        print(i)
                elif self.sim_Parser.dict_out_cmd_plot[out_key][1]=='dc':
                    plt.figure(plt_list[i])
                    p=plt.subplot(1,1,1)
                    print('#----------------DC output-----------------#')
                    plt.plot(self.DC_swep_list,self.DC_swep_result[self.sim_Parser.dict_out_cmd_plot[out_key][2]],label=out_key)
                    #print(self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                    plt.title('DC SIMULATION PLOT')
                    if out_key[0]=='v':
                            plt.xlabel('t/s')
                            plt.ylabel('U/V')
                    elif out_key[0]=='i':
                        plt.xlabel('t/s')
                        plt.ylabel('i/A')
                    handles,lables = p.get_legend_handles_labels()
                    p.legend(handles[::-1],lables[::-1])
                    i+=1
                elif self.sim_Parser.dict_out_cmd_plot[out_key][1]=='ac':
                    plt.figure(plt_list[i])
                    #print(i)
                    #plt_list[i] = plt.subplot(1,1,1)
                    print('#----------------AC output-----------------#')
                    self.ac_swep_list = np.log10(self.ac_swep_list)
                    self.AC_swep_result[self.sim_Parser.dict_out_cmd_plot[out_key][2]] = 20*np.log10(self.AC_swep_result[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                    p1=plt.subplot(211)
                    p1.plot(self.ac_swep_list,self.AC_swep_result[self.sim_Parser.dict_out_cmd_plot[out_key][2]],label=out_key)
                    #print(self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                    plt.title('AC simulation magnitude and phase plot')
                    plt.ylabel('Mag/dB20')
                    handles,lables = p1.get_legend_handles_labels()
                    p1.legend(handles[::-1],lables[::-1])
                    p2=plt.subplot(212)
                    p2.plot(self.ac_swep_list,self.AC_swep_result_phase[self.sim_Parser.dict_out_cmd_plot[out_key][2]],label=out_key)
                    #print(self.TRAN_y_axis[self.sim_Parser.dict_out_cmd_plot[out_key][2]])
                    plt.xlabel('Freq/dB')
                    plt.ylabel('Phase/rad')
                    handles,lables = p2.get_legend_handles_labels()
                    p2.legend(handles[::-1],lables[::-1])
                    i+=1
                    #plt.show()
                else:
                    pass
                plt.show()
        for out_key in self.sim_Parser.dict_out_cmd_print.keys():
            if self.sim_Parser.dict_out_cmd_print[out_key][0]=='print':
                #print('hi')
                if self.sim_Parser.dict_out_cmd_print[out_key][1]=='dc':
                    print(out_key,'\n',self.DC_swep_result[self.sim_Parser.dict_out_cmd_print[out_key][2]])
                else:
                    pass
        
        '''
        if  self.sim_Parser.dict_out_cmd_plot !={}:
            self.output_print()
        '''
    ##------------------------------- element stamp---------------------------------##
    # class obj_R(obj_element):
    def R_mna_constr(self,node1,node2,para,MNA):
        MNA[node1,node1] = MNA[node1,node1] + 1/float(para)
        MNA[node1,node2] = MNA[node1,node2] - 1/float(para)
        MNA[node2,node1] = MNA[node2,node1] - 1/float(para)
        MNA[node2,node2] = MNA[node2,node2] + 1/float(para)
        return MNA
    # class obj_C(obj_element):
    def C_AC_mna_constr(self,node1,node2,name,para,omega,MNA):
        MNA[node1,node1] = MNA[node1,node1] + 1j*2*np.pi*omega*para
        MNA[node1,node2] = MNA[node1,node2] - 1j*2*np.pi*omega*para
        MNA[node2,node1] = MNA[node2,node1] - 1j*2*np.pi*omega*para
        MNA[node2,node2] = MNA[node2,node2] + 1j*2*np.pi*omega*para
        return MNA
    def C_TRAN_mna_constr(self,node1,node2,name,para,v0,i0,method,MNA,RHS):
        if method==0:
            ##BE:
            MNA[node1,self.modify_node_branch[name]] = 1
            MNA[self.modify_node_branch[name],node1] = para/self.step_value
            MNA[node2,self.modify_node_branch[name]] = -1
            MNA[self.modify_node_branch[name],node2] = -para/self.step_value
            MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = -1
            RHS[self.modify_node_branch[name]] = para/self.step_value*v0
        elif method==1:
            ##FE
            MNA[node1,self.modify_node_branch[name]] = 1
            MNA[self.modify_node_branch[name],node1] = para/self.step_value
            MNA[node2,self.modify_node_branch[name]] = -1
            MNA[self.modify_node_branch[name],node2] = -para/self.step_value
            #MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = -1
            RHS[self.modify_node_branch[name]] = para/self.step_value*v0+i0
        elif method ==2:
            MNA[node1,self.modify_node_branch[name]] = 1
            MNA[self.modify_node_branch[name],node1] = para/self.step_value
            MNA[node2,self.modify_node_branch[name]] = -1
            MNA[self.modify_node_branch[name],node2] = -para/self.step_value
            MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = -0.5
            RHS[self.modify_node_branch[name]] = para/self.step_value*v0+0.5*i0
        return MNA,RHS    
    # class obj_L(obj_element):
    def L_AC_mna_constr(self,node1,node2,name,para,omega,MNA):
        MNA[node1,self.modify_node_branch[name]] = MNA[node1,self.modify_node_branch[name]] + 1
        MNA[self.modify_node_branch[name],node1] = MNA[self.modify_node_branch[name],node1] + 1
        MNA[node2,self.modify_node_branch[name]] = MNA[node2,self.modify_node_branch[name]] - 1
        MNA[self.modify_node_branch[name],node2] = MNA[self.modify_node_branch[name],node2] - 1
        MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = MNA[self.modify_node_branch[name],self.modify_node_branch[name]] - 1j*2*np.pi*omega*para
        return MNA   
    def L_DC_mna_constr(self,node1,node2,name,para,MNA):
        MNA[node1,self.modify_node_branch[name]] = MNA[node1,self.modify_node_branch[name]] + 1
        MNA[self.modify_node_branch[name],node1] = MNA[self.modify_node_branch[name],node1] + 1
        MNA[node2,self.modify_node_branch[name]] = MNA[node2,self.modify_node_branch[name]] - 1
        MNA[self.modify_node_branch[name],node2] = MNA[self.modify_node_branch[name],node2] - 1
        return MNA   
    def L_TRAN_mna_constr(self,node1,node2,name,para,v0,i0,method,MNA,RHS):
        if method==0:
            ##BE:
            MNA[node1,self.modify_node_branch[name]] = 1
            MNA[self.modify_node_branch[name],node1] = 1
            MNA[node2,self.modify_node_branch[name]] = -1
            MNA[self.modify_node_branch[name],node2] = -1
            MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = -para/self.step_value
            RHS[self.modify_node_branch[name]] = -para/self.step_value*i0
        elif method==1:
            ##FE
            MNA[node1,self.modify_node_branch[name]] = 1
            #MNA[self.modify_node_branch[name],node1] = para/self.step_value
            MNA[node2,self.modify_node_branch[name]] = -1
            #MNA[self.modify_node_branch[name],node2] = -para/self.step_value
            MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = para/self.step_value
            RHS[self.modify_node_branch[name]] = para/self.step_value*i0+v0
        elif method ==2:
            MNA[node1,self.modify_node_branch[name]] = 1
            MNA[self.modify_node_branch[name],node1] = 0.5
            MNA[node2,self.modify_node_branch[name]] = -1
            MNA[self.modify_node_branch[name],node2] = -0.5
            MNA[self.modify_node_branch[name],self.modify_node_branch[name]] = -para/self.step_value
            RHS[self.modify_node_branch[name]] = -para/self.step_value*i0-0.5*v0        
        return MNA,RHS
    # class obj_D(obj_element):
    def D_mna_constr(self,node1,node2,u_last_time,MNA,RHS):
        MNA[node1,node1] = MNA[node1,node1] + 40*math.exp(40*u_last_time)
        MNA[node1,node2] = MNA[node1,node2] - 40*math.exp(40*u_last_time)
        MNA[node2,node1] = MNA[node2,node1] - 40*math.exp(40*u_last_time)
        MNA[node2,node2] = MNA[node2,node2] + 40*math.exp(40*u_last_time)
        RHS[node1] = RHS[node1] + 40*u_last_time*math.exp(40*u_last_time) - (math.exp(40*u_last_time)-1)
        RHS[node2] = RHS[node2] - 40*u_last_time*math.exp(40*u_last_time) + (math.exp(40*u_last_time)-1)
        return MNA,RHS
        # class obj_MOS(obj_element)
    def NMOS_mna_constr(self,nd,ng,ns,vd,vs,vg,w_d_l,MNA,RHS):
        vt = 0.4
        kn = w_d_l*250*(1e-6)/2
        if vd-vs>0:
            lamda = 0.1
            if ((vg-vs-vt)>0 and (vd-vs)<(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[nd,ns] = MNA[nd,ns] - kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[ns,nd] = MNA[ns,nd] - kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[ns,ns] = MNA[ns,ns] + kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[nd,ng] = MNA[nd,ng] + kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                MNA[nd,ns] = MNA[nd,ns] - kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                MNA[ns,ng] = MNA[ns,ng] - kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                MNA[ns,ns] = MNA[ns,ns] + kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                RHS[nd] = RHS[nd] + kn*(2*((vg-vs-vt)*(vd-vs))-np.square(vd-vs))*(1+lamda*(vd-vs))
                RHS[ns] = RHS[ns] - kn*(2*((vg-vs-vt)*(vd-vs))-np.square(vd-vs))*(1+lamda*(vd-vs))
            elif ((vg-vs-vt)>0 and (vd-vs)>=(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*(np.square(vg-vs-vt)*lamda)
                MNA[nd,ns] = MNA[nd,ns] - kn*(np.square(vg-vs-vt)*lamda)
                MNA[ns,nd] = MNA[ns,nd] - kn*(np.square(vg-vs-vt)*lamda)
                MNA[ns,ns] = MNA[ns,ns] + kn*(np.square(vg-vs-vt)*lamda)
                MNA[nd,ng] = MNA[nd,ng] + kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                MNA[nd,ns] = MNA[nd,ns] - kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                MNA[ns,ng] = MNA[ns,ng] - kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                MNA[ns,ns] = MNA[ns,ns] + kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                RHS[nd] = RHS[nd] + kn*(np.square(vg-vs-vt))*(1+lamda*(vd-vs))
                RHS[ns] = RHS[ns] - kn*(np.square(vg-vs-vt))*(1+lamda*(vd-vs))
        elif vs-vd>0:
            lamda=0
            if ((vg-vd-vt)>0 and (vs-vd)<(vg-vd-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[nd,ns] = MNA[nd,ns] - kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ns] = MNA[ns,ns] + kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ng] = MNA[ns,ng] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,nd] = MNA[nd,nd] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                RHS[ns] = RHS[ns] + kn*(2*((vg-vd-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
                RHS[nd] = RHS[nd] - kn*(2*((vg-vd-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
            elif ((vg-vs-vt)>0 and (vd-vs)>=(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*(np.square(vg-vd-vt)*lamda)
                MNA[nd,ns] = MNA[nd,ns] - kn*(np.square(vg-vd-vt)*lamda)
                MNA[ns,nd] = MNA[ns,nd] - kn*(np.square(vg-vd-vt)*lamda)
                MNA[ns,ns] = MNA[ns,ns] + kn*(np.square(vg-vd-vt)*lamda)
                MNA[ns,ng] = MNA[ns,ng] + kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] - kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                MNA[nd,nd] = MNA[nd,nd] + kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                RHS[ns] = RHS[ns] + kn*(np.square(vg-vs-vt))*(1+lamda*(vs-vd))
                RHS[nd] = RHS[nd] - kn*(np.square(vg-vs-vt))*(1+lamda*(vs-vd))
        return MNA,RHS
    def PMOS_mna_constr(self,nd,ng,ns,vd,vs,vg,w_d_l,MNA,RHS):
        vt = 0.45
        kn = w_d_l*125*(1e-6)/2
        
        #print(MNA)
        if vd-vs<0:
            lamda = 0.15
            if ((vs-vg-vt)>0 and (vs-vd)<(vs-vg-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*((vs-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[nd,ns] = MNA[nd,ns] - kn*((vs-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*((vs-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ns] = MNA[ns,ns] + kn*((vs-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,ns] = MNA[nd,ns] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[ns,ng] = MNA[ns,ng] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[ns,ns] = MNA[ns,ns] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                RHS[nd] = RHS[nd] - kn*(2*((vs-vg-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
                RHS[ns] = RHS[ns] + kn*(2*((vs-vg-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
            elif ((vs-vg-vt)>0 and (vs-vd)>=(vs-vg-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*(np.square(vs-vg-vt)*lamda)
                MNA[nd,ns] = MNA[nd,ns] - kn*(np.square(vs-vg-vt)*lamda)
                MNA[ns,nd] = MNA[ns,nd] - kn*(np.square(vs-vg-vt)*lamda)
                MNA[ns,ns] = MNA[ns,ns] + kn*(np.square(vs-vg-vt)*lamda)
                MNA[nd,ng] = MNA[nd,ng] + kn*(2*(vs-vg-vt)*(1+lamda*(vs-vd)))
                MNA[nd,ns] = MNA[nd,ns] - kn*(2*(vs-vg-vt)*(1+lamda*(vs-vd)))
                MNA[ns,ng] = MNA[ns,ng] - kn*(2*(vs-vg-vt)*(1+lamda*(vs-vd)))
                MNA[ns,ns] = MNA[ns,ns] + kn*(2*(vs-vg-vt)*(1+lamda*(vs-vd)))
                RHS[nd] = RHS[nd] - kn*(np.square(vs-vg-vt))*(1+lamda*(vs-vd))
                RHS[ns] = RHS[ns] + kn*(np.square(vs-vg-vt))*(1+lamda*(vs-vd))
        elif vs-vd<0:
            lamda = 0
            if ((vd-vg-vt)>0 and (vd-vs)<(vd-vg-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*((vd-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[nd,ns] = MNA[nd,ns] - kn*((vd-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*((vd-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ns] = MNA[ns,ns] + kn*((vd-vg-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ng] = MNA[ns,ng] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,nd] = MNA[nd,nd] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                RHS[ns] = RHS[ns] - kn*(2*((vd-vg-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
                RHS[nd] = RHS[nd] + kn*(2*((vd-vg-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
            elif ((vd-vg-vt)<0 and (vd-vs)>=(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*(np.square(vd-vg-vt)*lamda)
                MNA[nd,ns] = MNA[nd,ns] - kn*(np.square(vd-vg-vt)*lamda)
                MNA[ns,nd] = MNA[ns,nd] - kn*(np.square(vd-vg-vt)*lamda)
                MNA[ns,ns] = MNA[ns,ns] + kn*(np.square(vd-vg-vt)*lamda)
                MNA[ns,ng] = MNA[ns,ng] + kn*(2*(vd-vg-vt)*(1+lamda*(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*(2*(vd-vg-vt)*(1+lamda*(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] - kn*(2*(vd-vg-vt)*(1+lamda*(vs-vd)))
                MNA[nd,nd] = MNA[nd,nd] + kn*(2*(vd-vg-vt)*(1+lamda*(vs-vd)))
                RHS[ns] = RHS[ns] - kn*(np.square(vs-vg-vt))*(1+lamda*(vs-vd))
                RHS[nd] = RHS[nd] + kn*(np.square(vs-vg-vt))*(1+lamda*(vs-vd))
        return MNA,RHS
    
    '''
    def PMOS_mna_constr(self,nd,ng,ns,vd,vs,vg,w_d_l,MNA,RHS):
        vt = 0.6
        kn = w_d_l*125*(1e-6)/2
        lamda = 0.15
        #print(MNA)
        if vd-vs<0:
            if ((vg-vs-vt)<0 and (vd-vs)>(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[nd,ns] = MNA[nd,ns] - kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[ns,nd] = MNA[ns,nd] - kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[ns,ns] = MNA[ns,ns] + kn*((vg-vs-vt)*(2+4*lamda*(vd-vs))-(2*(vd-vs)+3*lamda*np.square(vd-vs)))
                MNA[nd,ng] = MNA[nd,ng] + kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                MNA[nd,ns] = MNA[nd,ns] - kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                MNA[ns,ng] = MNA[ns,ng] - kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                MNA[ns,ns] = MNA[ns,ns] + kn*(2*(vd-vs)*(1+lamda*(vd-vs)))
                RHS[nd] = RHS[nd] + kn*(2*((vg-vs-vt)*(vd-vs))-np.square(vd-vs))*(1+lamda*(vd-vs))
                RHS[ns] = RHS[ns] - kn*(2*((vg-vs-vt)*(vd-vs))-np.square(vd-vs))*(1+lamda*(vd-vs))
            elif ((vg-vs-vt)<0 and (vd-vs)<=(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*(np.square(vg-vs-vt)*lamda)
                MNA[nd,ns] = MNA[nd,ns] - kn*(np.square(vg-vs-vt)*lamda)
                MNA[ns,nd] = MNA[ns,nd] - kn*(np.square(vg-vs-vt)*lamda)
                MNA[ns,ns] = MNA[ns,ns] + kn*(np.square(vg-vs-vt)*lamda)
                MNA[nd,ng] = MNA[nd,ng] + kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                MNA[nd,ns] = MNA[nd,ns] - kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                MNA[ns,ng] = MNA[ns,ng] - kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                MNA[ns,ns] = MNA[ns,ns] + kn*(2*(vg-vs-vt)*(1+lamda*(vd-vs)))
                RHS[nd] = RHS[nd] + kn*(np.square(vg-vs-vt))*(1+lamda*(vd-vs))
                RHS[ns] = RHS[ns] - kn*(np.square(vg-vs-vt))*(1+lamda*(vd-vs))
        elif vs-vd<0:
            if ((vg-vd-vt)<0 and (vs-vd)>(vg-vd-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[nd,ns] = MNA[nd,ns] - kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ns] = MNA[ns,ns] + kn*((vg-vd-vt)*(2+4*lamda*(vs-vd))-(2*(vs-vd)+3*lamda*np.square(vs-vd)))
                MNA[ns,ng] = MNA[ns,ng] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] - kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                MNA[nd,nd] = MNA[nd,nd] + kn*(2*(vs-vd)*(1+lamda*(vs-vd)))
                RHS[ns] = RHS[ns] + kn*(2*((vg-vd-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
                RHS[nd] = RHS[nd] - kn*(2*((vg-vd-vt)*(vs-vd))-np.square(vs-vd))*(1+lamda*(vs-vd))
            elif ((vg-vs-vt)<0 and (vd-vs)<=(vg-vs-vt)):
                MNA[nd,nd] = MNA[nd,nd] + kn*(np.square(vg-vd-vt)*lamda)
                MNA[nd,ns] = MNA[nd,ns] - kn*(np.square(vg-vd-vt)*lamda)
                MNA[ns,nd] = MNA[ns,nd] - kn*(np.square(vg-vd-vt)*lamda)
                MNA[ns,ns] = MNA[ns,ns] + kn*(np.square(vg-vd-vt)*lamda)
                MNA[ns,ng] = MNA[ns,ng] + kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                MNA[ns,nd] = MNA[ns,nd] - kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                MNA[nd,ng] = MNA[nd,ng] - kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                MNA[nd,nd] = MNA[nd,nd] + kn*(2*(vg-vd-vt)*(1+lamda*(vs-vd)))
                RHS[ns] = RHS[ns] + kn*(np.square(vg-vs-vt))*(1+lamda*(vs-vd))
                RHS[nd] = RHS[nd] - kn*(np.square(vg-vs-vt))*(1+lamda*(vs-vd))
        return MNA,RHS
    '''
    # class obj_V(obj_element):
    def V_mna_constr(self,node1,node2,name,para,MNA,RHS):
        MNA[node1,self.modify_node_branch[name]] = MNA[node1,self.modify_node_branch[name]] + 1
        MNA[self.modify_node_branch[name],node1] = MNA[self.modify_node_branch[name],node1] + 1
        MNA[node2,self.modify_node_branch[name]] = MNA[node2,self.modify_node_branch[name]] - 1
        MNA[self.modify_node_branch[name],node2] = MNA[self.modify_node_branch[name],node2] - 1
        RHS[self.modify_node_branch[name]] = RHS[self.modify_node_branch[name]] + para
        return MNA,RHS
    # class obj_I(obj_element):
    def I_mna_constr(self,node1,node2,para,RHS):
        RHS[node1] = RHS[node1] - para
        RHS[node2] = RHS[node2] + para
        return RHS
    # class obj_G(obj_element):
    def G_mna_constr(self,node1,node2,nc1,nc2,para,MNA):
        MNA[node1,nc1] = MNA[node1,nc1] + para
        MNA[node2,nc1] = MNA[node2,nc1] - para
        MNA[node1,nc2] = MNA[node1,nc2] - para
        MNA[node2,nc2] = MNA[node2,nc2] + para
        return MNA
    # class obj_E(obj_element):
    def E_mna_constr(self,node1,node2,nc1,nc2,name,para,MNA):
        MNA[node1,self.modify_node_branch[name]] = MNA[node1,self.modify_node_branch[name]] + 1
        MNA[node2,self.modify_node_branch[name]] = MNA[node2,self.modify_node_branch[name]] - 1
        MNA[self.modify_node_branch[name],node1] = MNA[self.modify_node_branch[name],node1] + 1
        MNA[self.modify_node_branch[name],node2] = MNA[self.modify_node_branch[name],node2] - 1
        MNA[self.modify_node_branch[name],nc1] = MNA[self.modify_node_branch[name],nc1] - para
        MNA[self.modify_node_branch[name],nc2] = MNA[self.modify_node_branch[name],nc2] + para
        return MNA
    # class obj_F(obj_element):
    def F_mna_constr(self,node1,node2,nc1,nc2,name,para,is_v,MNA):
        MNA[node1,self.modify_node_branch[name]] = MNA[node1,self.modify_node_branch[name]] + para
        MNA[node2,self.modify_node_branch[name]] = MNA[node2,self.modify_node_branch[name]] - para
        if is_v == 0:
            MNA[nc1,self.modify_node_branch[name]] = MNA[nc1,self.modify_node_branch[name]] + 1
            MNA[nc2,self.modify_node_branch[name]] = MNA[nc2,self.modify_node_branch[name]] - 1
            MNA[self.modify_node_branch[name],nc1] = MNA[self.modify_node_branch[name],nc1] + 1
            MNA[self.modify_node_branch[name],nc2] = MNA[self.modify_node_branch[name],nc2] - 1
        return MNA
    # class obj_H(obj_element):
    def H_mna_constr(self,node1,node2,nc1,nc2,vk_name,vc_name,para,is_v,MNA):
        MNA[self.modify_node_branch[vk_name],self.modify_node_branch[vk_name]] = MNA[self.modify_node_branch[vk_name],self.modify_node_branch[vk_name]] - para
        MNA[self.modify_node_branch[vk_name],node1] = MNA[self.modify_node_branch[vk_name],node1] + 1
        MNA[self.modify_node_branch[vk_name],node2] = MNA[self.modify_node_branch[vk_name],node2] - 1
        MNA[node1,self.modify_node_branch[vk_name]] = MNA[node1,self.modify_node_branch[vk_name]] + 1
        MNA[node2,self.modify_node_branch[vk_name]] = MNA[node2,self.modify_node_branch[vk_name]] - 1
        if is_v == 0:
            MNA[nc1,self.modify_node_branch[vc_name]] = MNA[nc1,self.modify_node_branch[vc_name]] + 1
            MNA[nc2,self.modify_node_branch[vc_name]] = MNA[nc2,self.modify_node_branch[vc_name]] - 1
            MNA[self.modify_node_branch[vc_name],nc1] = MNA[self.modify_node_branch[vc_name],nc1] + 1
            MNA[self.modify_node_branch[vc_name],nc2] = MNA[self.modify_node_branch[vc_name],nc2] - 1
        return MNA
    
    


#---------------------test part-------------------------#
# net list
'''
example_netlist1 = """
*netlist example 1
R1 1 2 1k
C1 2 0 1u
Vs 1 0 2
.tran 1ms 10ms
.plot tran V(2)
.end
"""
'''
'''
example_netlist1="""
*EE105 SPICE Tutorial Example 7 - homework3 Circuit1
Vin 1 0 SIN(0 1 10)
R 1 2 3k
L 1 2 4
C 2 0 2
.tran 1ms 1s
.dc VS6 0v 3v 0.1v
.plot tran V(1) V(2)
.end
"""
'''
'''
example_netlist1 = """
*EE105 SPICE Tutorial Example 1 - Simple RC Circuit
vs vs gnd PWL(0s 0V 5ms 0V 5.001ms 5V 10ms 5V)
r1 vs vo  1k
c1 vo gnd 1uF
.tran 0.01ms 10ms
.option post=2 nomod
.end
"""
'''
'''
example_netlist1 = """
*netlist example

Vs 1 0 PULSE 0 5 2n 0.5n 0.5n 5n 10n
r1 1 2 2
c1 2 0 50p
r2 2 3 2
c2 3 0 50p
r3 3 4 2
c3 4 0 50p
r4 4 5 2
c4 5 0 50p
r5 5 6 2
c5 6 0 50p
r6 6 7 2
c6 7 0 50p

.TRAN 0.01n 50n
.PRINT TRAN V(3)
.PLOT TRAN V(3) V(1)
.END

"""
'''
'''
example_netlist1 = """
*EE105 SPICE Tutorial Example 9 - homework4 Circuit1
Isrc 0 1 1
R1 1 0 1
R2 1 2 0.5
D 2 0 diode
.tran 1u 1m
.plot tran v(2) v(1)
.end
"""
'''
'''
example_netlist1 = """
*EE105 SPICE Tutorial Example 10 - homework4 Circuit2
Isrc 0 1 1
R1 1 0 1
R2 1 2 0.5
D1 1 0 diode
D2 2 0 diode
C 2 0 3
.tran 1m 1
.plot tran v(2) v(1)
.end
"""
'''
'''
example_netlist1 = """
*two order RC filter
vin 1 0 1
r1 1 2 1k
c1 2 0 1u
r2 2 3 1k
c2 3 0 10n
.ac LIN 1 0 10000
.plot ac v(2) v(3)
.end
"""
'''
'''
example_netlist1 = """
*coms inverter-transient simulation
Vin 1 0 pulse (0 1 0.1 0.1 0.1 1.0 1.5)
Vdd 3 0 1.8
M1 2 1 0 0 NMOS 2u 2u
M2 2 1 3 3 PMOS 4u 2u
R1 2 0 5k
.tran 0.1 2 
.plot tran v(1) v(2)
.end
"""

# excute test

print (example_netlist1)
sim=simulator(example_netlist1)
sim.solve_net()

#sim.printMNAwithDiode()
#sim.showNewtonRapson()
#sim.showIteration()
#sim.tran_solve_net('BE','1m')

#sim.dc_mna_matrix()
#sim.print_matrix()
#sim.solve_net('BE','1m')
#sim.output_print()
#print ('hi')


#sim =simulator('a')
#sim.solve_net('BE','5n')
'''