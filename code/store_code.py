#print(self.MNA_dc,self.RHS_dc)
    def printMNAwithDiode(self):
        #tran simulation
        #param get
        mna_out_flag=0
        flag_tran_y_append=0
        per_cnt=1
        pw_cnt=0
        pw_r_cnt=0
        pw_f_cnt=0
        u0={}
        u1={}
        self.tran_converge_threshold=0.0005
        self.tran_method='BE'
        self.tran_option_select=self.tran_simulator_option['BE']
        self.step_value = turn_unit.solve_unit('1m') #h
        self.tran_step = self.sim_Parser.dict_command['tran'][0] #tran plot step
        self.tran_option_select=self.tran_simulator_option['BE']
        #print (self.step_value)
        #self.tran_mna_matrix()
        self.tran_plot_list=np.arange(0,self.sim_Parser.dict_command['tran'][1],self.sim_Parser.dict_command['tran'][0],dtype=float)
        self.tran_swep_list=np.arange(0,self.sim_Parser.dict_command['tran'][1],self.step_value,dtype=float)
        #get v source
        for v_key in self.sim_Parser.dict_v.keys():
            if self.sim_Parser.dict_v[v_key][0]=='pulse':
                for t_cnt in self.tran_swep_list:
                    if v_key in self.v_value.keys():
                        if t_cnt >= self.sim_Parser.dict_v[v_key][3]+self.sim_Parser.dict_v[v_key][4]*per_cnt+(self.sim_Parser.dict_v[v_key][7]-self.sim_Parser.dict_v[v_key][4])*(per_cnt-1):
                            v_val_estp = self.sim_Parser.dict_v[v_key][2]
                            pw_cnt +=  self.step_value
                            if pw_cnt >= self.sim_Parser.dict_v[v_key][6]:
                                pw_cnt = 0
                                per_cnt += 1
                            elif t_cnt >= self.sim_Parser.dict_v[v_key][3]+(self.sim_Parser.dict_v[v_key][7])*(per_r_cnt-1):
                                v_val_estp = ((self.sim_Parser.dict_v[v_key][2] - self.sim_Parser.dict_v[v_key][1])/self.sim_Parser.dict_v[v_key][4])*(t_cnt-self.sim_Parser.dict_v[v_key][3]-(self.sim_Parser.dict_v[v_key][7])*(per_r_cnt-1))
                                pw_r_cnt +=  self.step_value
                                if pw_r_cnt >= self.sim_Parser.dict_v[v_key][4]:
                                    pw_r_cnt = 0
                                    per_r_cnt += 1
                            elif t_cnt >= self.sim_Parser.dict_v[v_key][3]+(self.sim_Parser.dict_v[v_key][4]+self.sim_Parser.dict_v[v_key][6])*per_f_cnt+(self.sim_Parser.dict_v[v_key][7]-self.sim_Parser.dict_v[v_key][4]-self.sim_Parser.dict_v[v_key][6])*(per_f_cnt-1):
                                v_val_estp = self.sim_Parser.dict_v[v_key][2]+((self.sim_Parser.dict_v[v_key][1] - self.sim_Parser.dict_v[v_key][2])/self.sim_Parser.dict_v[v_key][4])*(t_cnt-(self.sim_Parser.dict_v[v_key][3]+(self.sim_Parser.dict_v[v_key][4]+self.sim_Parser.dict_v[v_key][6])*per_f_cnt+(self.sim_Parser.dict_v[v_key][7]-self.sim_Parser.dict_v[v_key][4]-self.sim_Parser.dict_v[v_key][6])*(per_f_cnt-1)))
                                pw_f_cnt +=  self.step_value
                                if pw_f_cnt >= self.sim_Parser.dict_v[v_key][4]:
                                    pw_f_cnt = 0
                                    per_f_cnt += 1
                            else:
                                v_val_estp = self.sim_Parser.dict_v[v_key][1]
                                self.v_value[v_key].append(v_val_estp)
                    else:
                        v_val_estp = self.sim_Parser.dict_v[v_key][1]
                        self.v_value.update({v_key:[v_val_estp]})
            elif self.sim_Parser.dict_v[v_key][0]=='sin':
                #print(self.sim_Parser.dict_v[v_key])
                self.v_value.update({v_key:float(self.sim_Parser.dict_v[v_key][2])*np.sin(2*np.pi*float(self.sim_Parser.dict_v[v_key][3])*self.tran_swep_list)+float(self.sim_Parser.dict_v[v_key][1])})    
            else:
                for t_cnt in self.tran_swep_list:
                    if v_key in self.v_value.keys():
                        self.v_value[v_key].append(self.sim_Parser.dict_v[v_key][0])
                    else:
                        self.v_value.update({v_key:[self.sim_Parser.dict_v[v_key][0]]}) 
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
                        #print(u_val-u1[u_key])
                        #print('hello')
                    else:
                        end=0
                        #print('hi')
                        #print(u_val-u1[u_key])
                    flag_iter_end=flag_iter_end and end
                #need flag iter to excute one loop
                flag_iter+=1
                #print(flag_iter)

                #tran mna 
                self.add_branch()
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
                        #print (node1)
                        node1_num=self.modify_node_branch[node1]
                        node2_num=self.modify_node_branch[node2]
                        #np.c_(self.MNA_dc,'0')
                        #np.r_(self.MNA_dc,0)
                        #print(self.sim_Parser.dict_v[v_key])
                        self.V_mna_constr(node1_num,node2_num,v_key,self.v_value[v_key][t_step_cnt],self.MNA_tran,self.RHS_tran)
                        #print(self.v_value[v_key][t_step_cnt])
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
                ##end mna
                if (mna_out_flag==0):
                    print('#--------------------print mna matrix----------------------#')
                    print (self.MNA_tran,'\n',self.RHS_tran,'\n',self.modify_node_branch)
                    mna_out_flag=1
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
            #print('hi')
            #print(self.TRAN_y_axis['0'])
            #print(t_step_cnt) 
    def showNewtonRapson(self):
        print('#---------------show  NewtonRapson---------------------#') 
        shabi=nonlinear_solver(0.0005,0)
        #a=shabi.solver(0.1,0)
    def showIteration(self):
        print('#-----------------show  Iteration-------------------#') 
        shabi=nonlinear_solver(0.0005,1)
        #a=shabi.solver(0.1,1)