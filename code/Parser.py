### parser - zhuhanqing - 2019 - version 0.5
### index  follow the HSPCIE Tutorial 
#use get_value from isTools.py (by myself)
import re
import string
import isTools

class MyParser():
    
    def __init__(self,netlist):
        ##turn string input into list
        '''
        self.netlist=netlist.strip()
        self.net=self.netlist.split('\n')
        '''
       
        self.net=netlist

        #print(self.net)
        self.dict_r={}
        self.dict_c={}
        self.dict_l={}
        self.dict_diode={}
        self.dict_v={}
        self.dict_i={}
        self.dict_mos={}
        self.dict_model={}
        self.dict_E={}
        self.dict_G={}
        self.dict_H={}
        self.dict_F={}
        #dict_elements={}
        #dict_acAnalysis={}
        #dict_dcAnalysis={}
        #dict_tranAnalysis={}

        self.dict_dot={}
        self.dict_op={} #only for option
        self.dict_node={}
        self.dict_command={}
        self.dict_out_cmd_print={}
        self.dict_out_cmd_plot={}
        self.dict_nodeset={}
        self.flag=[]
    def parse(self):
        i=len(self.net)
        #print(i)
        j=0
        '''
        ##create needed dict
        self.dict_r={}
        self.dict_c={}
        self.dict_l={}
        self.dict_diode={}
        self.dict_v={}
        self.dict_i={}
        self.dict_mos={}
        self.dict_model={}
        #dict_elements={}
        #dict_acAnalysis={}
        #dict_dcAnalysis={}
        #dict_tranAnalysis={}

        self.dict_dot={}
        self.dict_node={}
        '''
        #print("#---------Parse the Netlist---------#")
        while j<i:
            #print ('ok')
            ##modify the list string:change the case(lower),replace the ()
            # use return to get out of loop for declared error
            line = self.net[j].strip().lower() #A-a
            line = line.replace('(',' ')
            line = line.replace(')',' ')
            j = j+1
            #print (line)
            #print(j) 
            #print(line)
            #print(j)
            if(line[0]!='*'):
                pass
                #print("useful command")
            
            ##end parse at ".end" print parse information
            #problem
            #print(self.dict_node) 
            if line =='.end':
                '''
                if (len(self.dict_mos)!=0):
                    mosmodel = self.dict_mos.keys() #can print a list 
                    #print (mosmodel)
                    for t in mosmodel:
                        #print (mosmodel)
                        #???why use tmp
                        mos_tmp = self.dict_mos[i][5]
                        model_name = self.dict_mos[i][4]
                        print (mos_tmp)
                        if(model_name in self.dict_model.keys()):
                            model_tmp = self.dict_model[model_name]
                            mos_tmp.update(model_tmp)
                            self.dict_mos[i] = self.dict_mos[i][0:5]+(mos_tmp,)
                        else:
                            del self.dict_mos[i]
                            #return 33,j
                    print (self.dict_mos)
                '''
                '''
                if (len(self.dict_diode)!=0):
                    diodemodel = self.dict_diode.keys()
                    #print(diodemodel)
                    for i in diodemodel:
                        dio_temp =self.dict_diode[i]
                        if(dio_temp[2] in self.dict_model):
                        model_temp = self.dict_model[dio_temp[2]]
                            dio_temp=dio_temp+(model_temp['is'],)
                            self.dict_diode[i]=dio_temp
                        else:
                            del self.dict_diode[i]
                            #return 33,j
                    print (self.dict_diode)
                '''
                ## defualt : no gnd
                #print(self.dict_node)
                #print(j)
                if ('0' in self.dict_node) or ('gnd' in self.dict_node):
                    #print ('hi')
                    return -1,0
                else:
                    pass
                    #return 28,j
            
            ## turn line str into list for matching
            # two dimensions 
            line_element = line.split()
            line_element_len=len(line_element)

##-------------element matching-----------------##
            #resistor 
            if (line_element[0][0] =='r'): 
                #print('find a R')
                if line_element_len!=4:
                    #print('error',j)
                    return 0,j #error0: not in format
                if (line_element[0] in self.dict_r):
                    return 1,j #error 1: repeat define a R in line j
                    #print('wrong')
                else:
                    if (re.search('[0-9]+',line_element[3])):
                        p=0
                        #print(re.match('[0-9]+',line_element[3]))
                    else:
                        return 2,j #error2: no value
                    if(isTools.get_value(line_element[3])==0):
                        return 2,j
                    self.dict_r[line_element[0]]=[isTools.get_value(line_element[3]),line_element[1],line_element[2]]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    #print(line_element[0],":",self.dict_r[line_element[0]][0],'node1:',self.dict_r[line_element[0]][1],'node2:',self.dict_r[line_element[0]][2])
            #inductor 
            if (line_element[0][0] =='l'):
                if line_element_len!=4:
                    #print('error',j)
                    return 0,j #error0: not in format
                if (line_element[0] in self.dict_l):
                    return 1,j #error 1: repeat define a C in line j
                else:
                    if (re.search('[0-9]+',line_element[3])):
                        p=0
                        #print(re.match('[0-9]+',line_element[3]))
                    else:
                        return 2,j #error2: no value at line j
                    if(isTools.get_value(line_element[3])==0):
                        return 2,j
                    self.dict_l[line_element[0]]=[isTools.get_value(line_element[3]),line_element[1],line_element[2]]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    print(self.dict_node)
                    #print(line_element[0],":",self.dict_l[line_element[0]][0],'node1:',self.dict_l[line_element[0]][1],'node2:',self.dict_l[line_element[0]][2])
            #capacitor
            if (line_element[0][0] =='c'):
                if line_element_len!=4:
                    #print('error',j)
                    return 0,j #error0: not in format at line j
                if (line_element[0] in self.dict_c):
                    return 1,j #error 1: repeat define a C in line j
                else:
                    if (re.search('[0-9]+',line_element[3])):
                        p=0
                        #print(re.match('[0-9]+',line_element[3]))
                    else:
                        return 2,j #error2: no value at line j
                    if(isTools.get_value(line_element[3])==0):
                        return 2,j
                    self.dict_c[line_element[0]]=[isTools.get_value(line_element[3]),line_element[1],line_element[2]]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    #print(line_element[0],":",self.dict_c[line_element[0]][0],'node1:',self.dict_c[line_element[0]][1],'node2:',self.dict_c[line_element[0]][2])
            #diode
            if(line_element[0][0]=='d'):
                if line_element_len<4:
                    return 0,j #error0: not in format
                else:
                    self.dict_diode[line_element[0]]=(line_element[1],line_element[2],line_element[3])
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                #print (line_element[0],'node1:',self.dict_diode[line_element[0]][0],'node2:',self.dict_diode[line_element[0]][1],'model:',self.dict_diode[line_element[0]][2])
            #mosfet
            if (line_element[0][0]=='m'):
                if (line_element_len<8):
                    return 0,j #error0
                '''
                mos_param=line_element[6:]
                mos_param_tmp={'l':0.00018,'w':0.00018}
                for para in mos_param:
                    mos_param_name,mos_param_value= mos_param.split('=')
                    mos_param_tmp[mos_param_name]=isTools.get_value(mos_param_value)
                '''
                MOS_w=isTools.get_value(line_element[6])
                MOS_l=isTools.get_value(line_element[7])
                # drain gate source body model:P/N+ D+G+S+B+W+L
                self.dict_mos[line_element[0]]=[line_element[5],line_element[1],line_element[2],line_element[3],line_element[4],MOS_w,MOS_l]
                #print(self.dict_mos[line_element[0]])
                isTools.add_node(self.dict_node,line_element[1])
                isTools.add_node(self.dict_node,line_element[2])
                isTools.add_node(self.dict_node,line_element[3])
                isTools.add_node(self.dict_node,line_element[4])

##----------------source matching-------------------##
            #V source
            if(line_element[0][0]=='v'):
                #print('find a v')
                #print(line_element)
                if line_element[0] in self.dict_v.keys():
                    return 1,j #error 1 for repeate definition 
                if line_element_len<3:
                    return 0,j
                elif (line_element_len==3):
                    self.dict_v[line_element[0]]=[0,line_element[1],line_element[2]] #v node1 node2 0 use for measure current
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                elif line_element_len==4:
                    line_element.insert(3,'dc')
                    dc_value = isTools.get_value(line_element[4])
                    self.dict_v[line_element[0]]=[dc_value,line_element[1],line_element[2]] #v node1 node2 xV
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    #print(dc_value[0])
                elif line_element_len>5:
                    #print('hi')
                    if(line_element[3]!='dc'):
                        #print (line_element)
                        tmp_v=line_element[0:3] #store the v source definition
                        if (line_element[3]=='sin'):
                            #line_element.remove('sin')
                            #print (line_element)
                            self.dict_v[line_element[0]]=['sin',line_element[1],line_element[2],line_element[4],line_element[5],line_element[6]]
                            #self.dict_v[line_element[0]]=['sin',line_element[4],line_element[5],line_element[6],line_element[7],line_element[8],line_element[9]]
                            #self.dict_v[line_element[0]]=['sin',tmp_v,line_element[4:]]
                            isTools.add_node(self.dict_node,line_element[1])
                            isTools.add_node(self.dict_node,line_element[2])    
                        elif (line_element[3]=='pulse'):
                            #print('find a pulse')
                            #vmin+vmax+delay+rise+fall+pluse wid+period 
                            self.dict_v[line_element[0]]=[line_element[3],line_element[1],line_element[2],float(line_element[4]),float(line_element[5]),float(line_element[6]),float(line_element[7]),float(line_element[8]),float(line_element[9]),float(line_element[10])]
                            isTools.add_node(self.dict_node,line_element[1])
                            isTools.add_node(self.dict_node,line_element[2])
                        elif (line_element[3]=='pwl'):
                            #print('i')
                            #line_element.remove('pwl')
                            #print (line_element)
                            #self.dict_v[line_element[0]]=['PWL',tmp_v,line_element[4:]]
                            a=len(line_element)
                            b=[]
                            i=4
                            #self.dict_v[line_element[0]]=['pwl']
                            while i<a:
                                b.append([line_element[i],line_element[i+1]])
                                i=i+2
                            self.dict_v[line_element[0]]=['pwl',line_element[1],line_element[2],b]
                            isTools.add_node(self.dict_node,line_element[1])
                            isTools.add_node(self.dict_node,line_element[2])
                        #print(self.dict_v)
                            #print (self.dict_v[line_element[0]]) 
                        #print (tmp_v)
                else:
                    pass
            #I source
            if(line_element[0][0]=='i'):
                if line_element[0] in self.dict_i.keys():
                    return 1,j #error 1 for repeate definition 
                if line_element_len<4:
                    return 0,j
                elif line_element_len==4:
                    line_element.insert(3,'dc')
                    #print(j)
                    dc_value = isTools.get_value(line_element[4])
                    #print (j)
                    #print (dc_value)
                    self.dict_i[line_element[0]]=[dc_value,line_element[1],line_element[2]] #v node1 node2 xV
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    #print(dc_value[0])
                    '''    
                elif line_element_len>5:
                    if(line_element[3]!='dc'):
                        #print (line_element)
                        tmp_v=line_element[0:3] #store the v source definition
                        if (line_element[3]=='sin'):
                            line_element.remove('sin')
                            self.dict_v[line_element[0]]=['sin',tmp_v,line_element[4:]]
                            isTools.add_node(self.dict_node,line_element[1])
                            isTools.add_node(self.dict_node,line_element[2])    
                        elif (line_element[3]=='pulse'):
                            pass
                        elif (line_element[3]=='pwl'):
                            #print('i')
                            line_element.remove('pwl')
                            #print (line_element)
                            self.dict_v[line_element[0]]=['PWL',tmp_v,line_element[4:]]
                            isTools.add_node(self.dict_node,line_element[1])
                            isTools.add_node(self.dict_node,line_element[2])
                            print (self.dict_v)
                            #print (self.dict_v[line_element[0]]) 
                        #print (tmp_v)
                    '''    
                else:
                    pass 
            #E/G : voltage controll
            if (line_element[0][0]=='e') or (line_element[0][0]=='g'):
                if(line_element_len!=6):
                    return 0,j #error 0
                value_ctr = isTools.get_value(line_element[5])
                if (line_element[0][0]=='e'):
                    self.dict_E[line_element[0]]=[line_element[1],line_element[2],line_element[3],line_element[4],value_ctr]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    isTools.add_node(self.dict_node,line_element[3])
                    isTools.add_node(self.dict_node,line_element[4])
                else:
                    #print (value_ctr)
                    self.dict_G[line_element[0]]=[line_element[1],line_element[2],line_element[3],line_element[4],value_ctr]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    isTools.add_node(self.dict_node,line_element[3])
                    isTools.add_node(self.dict_node,line_element[4]) 
                
            #F/H : current controll 
            if (line_element[0][0]=='f') or (line_element[0][0]=='h'):
                if(line_element_len==5)&(line_element[3] in self.dict_v.keys()):
                    value_ctr = isTools.get_value(line_element[4])
                    if (line_element=='f'):
                        self.dict_F[line_element[0]]=[line_element[1],line_element[2],line_element[3],value_ctr]
                        isTools.add_node(self.dict_node,line_element[1])
                        isTools.add_node(self.dict_node,line_element[2])
                    else:
                        self.dict_H[line_element[0]]=[line_element[1],line_element[2],line_element[3],value_ctr]
                        isTools.add_node(self.dict_node,line_element[1])
                        isTools.add_node(self.dict_node,line_element[2])
                '''
                if (line_element[0][0]=='e'):
                    self.dict_E[line_element[0]]=[line_element[1],line_element[2],line_element[3],line_element[4],value_ctr]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    isTools.add_node(self.dict_node,line_element[3])
                    isTools.add_node(self.dict_node,line_element[4])
                else:
                    self.dict_G[line_element[0]]=[line_element[1],line_element[2],line_element[3],line_element[4],value_ctr]
                    isTools.add_node(self.dict_node,line_element[1])
                    isTools.add_node(self.dict_node,line_element[2])
                    isTools.add_node(self.dict_node,line_element[3])
                    isTools.add_node(self.dict_node,line_element[4])  
                #self.dict_v[line_element[0]]
                '''
##----------------command matching------------------##
            if (line_element[0][0]=='.'):
                #print('hi')
                line_element[0]=line_element[0].replace('.','')
                # nodeset .nodeset v(0) 0.3V
                '''
                if (line_element[0]=='nodeset'):
                    self.dict_nodeset[line_element[1]+line_element[2]]=[line_element[2],line_element[3]]
                '''
            #.model
                if(line_element[0]=='model'):
                    #diode
                    if (line_element[2][0]=='d'):
                       #print('diode model here at line',j)
                       #list all possible param to match
                       diode_param_tmp={'is':0,'rs':0,'tt':0,'cjo':0,'vj':0,'m':0,'eg':0,'xti':0,'bv':0,'ibv':0} 
                       for param in line_element[3:]:
                           param_name,param_value = param.split('=')
                           #print(param_name,param_value)
                           param_value = isTools.get_value(param_value)
                           if param_name in diode_param_tmp.keys():
                               diode_param_tmp[param_name]=param_value
                           else:
                               return 0,j
                       self.dict_model[line_element[1]]=['diode',diode_param_tmp]
                       #print (self.dict_model[line_element[1]])                                       
                    #mos
                    elif (line_element[1][0]=='m'):
                        if(line_element[2]!='nmos') and (line_element[2]!='pmos'):
                            print ('we just have \'nmos/pmos\' model for mos')
                        if(line_element[2]=='nmos'):
                            mospara_tmp={'vto':0,'k':4.0e-5,'lambda':0,'phi':0.6,'gamma':0,'type':'nmos'}
                        else:
                            mospara_tmp={'vto':0,'k':4.0e-5,'lambda':0,'phi':0.6,'gamma':0,'type':'pmos'}
                        for para in line_element[3:]:
                            paraname,paravalue = para.split('=')
                            paravalue =isTools.get_value(paravalue)
                            if(paravalue=='f'):
                                print ('the parameter value cannot take the unit')
                                return 31,j
                            if(paraname in mospara_tmp.keys()):
                                mospara_tmp[paraname]=paravalue
                            else:
                                print ('the mos model does not have this parameter')
                                return 34,j

                        #print mospara_tmp
                        self.dict_model[line_element[1]]=mospara_tmp
                #option
                elif line_element[0]=='option':
                    #print(line_element)
                    if (line_element[1][0:4]=='post'):
                        #print('h')
                        if (line_element[1][5]=='1'):
                            opValue='output data in binary format'
                        elif(line_element[1][5]=='2'):
                            opValue='output data in ASCII format'
                            #print(opValue)
                        self.dict_op['option']=[-1,opValue]
                    else:
                        pass
                #.dc
                elif(line_element[0]=='dc'):
                    if (line_element[1][0]!='v')&(line_element[1][0]!='i'):
                        return 0,j #error0: not in format
                    if (line_element_len!=5)&(line_element_len!=9):
                        return 0,j #error0: not in format
                    if (line_element_len==5):
                        if (line_element[1] in self.dict_v.keys()):
                            dc_element=self.dc_op(line_element[1:5])
                            source_start=isTools.get_value(line_element[2])
                            source_stop=isTools.get_value(line_element[3])
                            source_step=isTools.get_value(line_element[4])
                            #self.dict_command[line_element[0]]=[line_element[1],source_start,source_stop,source_step]
                            self.dict_command[line_element[0]]=[line_element[1],dc_element[1],dc_element[2],dc_element[3]]
                            #print (self.dict_dot[line_element[0]][0])
                            #print (dc_element)
                        if (line_element[1] in self.dict_i.keys()):
                            dc_element=self.dc_op(line_element[1:5])
                            source_start=isTools.get_value(line_element[2])
                            source_stop=isTools.get_value(line_element[3])
                            source_step=isTools.get_value(line_element[4])
                            #self.dict_command[line_element[0]]=[line_element[1],source_start,source_stop,source_step]
                            self.dict_command[line_element[0]]=[line_element[1],dc_element[1],dc_element[2],dc_element[3]]
                            #print (self.dict_dot[line_element[0]][0])
                            #print (dc_element)
                #.ac
                elif(line_element[0]=='ac'):
                    if (line_element_len!=5):
                        return 0,j #error0: not in format
                    if (line_element[1]!='lin')&(line_element[1]!='oct')&(line_element[1]!='dec'):
                        return 0,j #error0: not in format
                    sample_num = isTools.get_value(line_element[2])
                    if (sample_num=='f'):
                        return 0,j #error0
                    start_fre = self.get_frequency(line_element[3])
                    end_fre = self.get_frequency(line_element[4])
                    self.dict_command[line_element[0]]=[line_element[1],sample_num,start_fre[0],end_fre[0]]
                #.tran
                elif(line_element[0]=='tran'):
                    if(line_element_len<3)or(line_element_len>5):
                        return 0,j #error 0
                    if(line_element_len==3):
                        time_step=self.get_time(line_element[1])
                        time_stop=self.get_time(line_element[2])
                        self.dict_command[line_element[0]]=(time_step[0],time_stop[0])
                        #print (time_step)
                        #print (self.dict_dot[line_element[0]])  
                elif (line_element[0]=='plot'):
                    #print('ok')
                    if line_element[1]=='tran':
                        a=len(line_element)
                        i_plot=2
                        while i_plot<a:
                            self.dict_out_cmd_plot[line_element[i_plot]+line_element[i_plot+1]]=[line_element[0],line_element[1],line_element[i_plot+1]]
                            #v/i+node:plot+tran+node
                            i_plot+=2
                        #self.dict_out_cmd[line_element[3]]=[line_element[0],line_element[1],line_element[2]]
                    elif(line_element[1]=='dc'):
                        a=len(line_element)
                        i_plot=2
                        while i_plot<a:
                            self.dict_out_cmd_plot[line_element[i_plot]+line_element[i_plot+1]]=[line_element[0],line_element[1],line_element[i_plot+1]]
                            #v/i+node:plot+tran+node
                            i_plot+=2
                    elif (line_element[1]=='ac'):
                        a=len(line_element)
                        i_plot=2
                        while i_plot<a:
                            self.dict_out_cmd_plot[line_element[i_plot]+line_element[i_plot+1]]=[line_element[0],line_element[1],line_element[i_plot+1]]
                            #v/i+node:plot+tran+node
                            i_plot+=2
                    else:
                        pass
                elif (line_element[0]=='print'):
                    #print('hi')
                    if line_element[1]=='tran':
                        a=len(line_element)
                        #print (a)
                        i_plot=2
                        while i_plot<a:
                            self.dict_out_cmd_print[line_element[i_plot]+line_element[i_plot+1]]=[line_element[0],line_element[1],line_element[i_plot+1]]
                            i_plot+=2
                            #print(i,'hi')
                        #self.dict_out_cmd_print[line_element[2]+line_element[3]]=[line_element[0],line_element[1],line_element[2]]
                    elif(line_element[1]=='dc'):
                        a=len(line_element)
                        #print (a)
                        i_plot=2
                        while i_plot<a:
                            self.dict_out_cmd_print[line_element[i_plot]+line_element[i_plot+1]]=[line_element[0],line_element[1],line_element[i_plot+1]]
                            i_plot+=2
                    elif(line_element[1]=='ac'):
                        a=len(line_element)
                        #print (a)
                        i_plot=2
                        while i_plot<a:
                            self.dict_out_cmd_print[line_element[i_plot]+line_element[i_plot+1]]=[line_element[0],line_element[1],line_element[i_plot+1]]
                            i_plot+=2
                    else:
                        pass
        #print('ok')        
        #print (self.dict_out_cmd_plot,self.dict_out_cmd_print)

##---------------------function definition----------------##
    def showErrorInfor(self,errorNum):
        print('error',errorNum[0],'at line',errorNum[1])
    def showParseResult(self):
        #print(self.dict_node)
        #print(self.dict_mos)
        Parser_result_info=[]
        #Parser_result_temp=" "
        print('#---------Parse the Netlist Succesfully---------#')
        # 8 blank+ 5blank+9blank
        Parser_result_info.append('>>>>>>>>>>>>>>>>>>Parse the Netlist Succesfully<<<<<<<<<<<<<<<<<<<<\n')
        element_num ='element	number	element	 number	\n'+'R:        '+str(len(self.dict_r))+ \
        '     C:         '+str(len(self.dict_c))+'\n'+'L:        '+str(len(self.dict_l))+ \
            '     VS:         '+str(len(self.dict_v))+'\n''IS:       '+str(len(self.dict_i))+'\n'
        Parser_result_info.append(element_num)
        print (element_num)
    #print defined model param
        if self.dict_model:
            print('Defined model parameter:')
            Parser_result_info.append('Defined model parameter:\n')
        else:
            pass
        for key in self.dict_model.keys():
            print ('Defined model:',self.dict_model[key][0],'  Name:',key,'\nParam:',self.dict_model[key][1])
            Parser_result_info.append('Defined model:',self.dict_model[key][0],'  Name:',key,'\nParam:',self.dict_model[key][1],'\n')
    #print element
        print ('Element info:')
        Parser_result_info.append('Element info:\n')
        #print(self.dict_r)
        for key in self.dict_r.keys():
            print (key,":",'node1:',self.dict_r[key][1],'node2:',self.dict_r[key][2])
            Parser_result_temp=key+":"+'node1:'+self.dict_r[key][1]+'node2:'+self.dict_r[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_l.keys():
            print (key,":",'node1:',self.dict_l[key][1],'node2:',self.dict_l[key][2])
            Parser_result_temp= key+":"+'node1:'+self.dict_l[key][1]+'node2:'+self.dict_l[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_c.keys():
            print (key,":",'node1:',self.dict_c[key][1],'node2:',self.dict_c[key][2])
            Parser_result_temp=key+":"+'node1:'+self.dict_c[key][1]+'node2:'+self.dict_c[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_diode.keys():
            print (key,":",'node1:',self.dict_diode[key][1],'node2:',self.dict_diode[key][2])
            Parser_result_temp=key+":"+'node1:'+self.dict_diode[key][1]+'node2:'+self.dict_diode[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_mos.keys():
            #print(self.dict_mos[key])
            print(key,':',self.dict_mos[key][0],'drain:',self.dict_mos[key][1],'gate:',self.dict_mos[key][2],'source:',self.dict_mos[key][3],'body:',self.dict_mos[key][4],'W=',str(self.dict_mos[key][5]),'l=',str(self.dict_mos[key][6]))
            Parser_result_temp=key+':'+self.dict_mos[key][0]+'drain:'+self.dict_mos[key][1]+'gate:'+self.dict_mos[key][2]+'source:'+self.dict_mos[key][3]+'body:'+self.dict_mos[key][4]+'W='+str(self.dict_mos[key][5])+'l='+str(self.dict_mos[key][6])+'\n'
            Parser_result_info.append(Parser_result_temp)
    #print  source
        print ('Source info:')
        Parser_result_info.append('Source info:\n')
        # diff between v and v pulse 
        #print (self.dict_v)
        for key in self.dict_v.keys():
            if(self.dict_v[key][0]=='pulse'):
                print(key,": ",'pulse','vmin: ',self.dict_v[key][1],'vmax: ',self.dict_v[key][2],'delay: ',self.dict_v[key][3],'rise time: ',self.dict_v[key][4],'fall time: ',self.dict_v[key][5],'pulse width: ',self.dict_v[key][6],'period: ',self.dict_v[key][7])
                Parser_result_temp=key+":"+'pulse'+'vmin: '+str(self.dict_v[key][1])+'vmax: '+str(self.dict_v[key][2])+'delay: '+str(self.dict_v[key][3])+'rise time: '+str(self.dict_v[key][4])+'fall time: '+str(self.dict_v[key][5])+'pulse width: '+str(self.dict_v[key][6])+'period: '+str(self.dict_v[key][7])+'\n'
                Parser_result_info.append(Parser_result_temp)
            elif(self.dict_v[key][0]=='pwl'):
                print (key,":",'pwl')
                Parser_result_temp=key+":"+'pwl'+'\n'
                Parser_result_info.append(Parser_result_temp)
                '''
                print (self.dict_v[key][1][0],':','node1:',self.dict_v[key][1][1],'node2:',self.dict_v[key][1][2],'PWL',self.dict_v[key][2])
                Parser_result_temp=self.dict_v[key][1][0]+':'+'node1:'+self.dict_v[key][1][1]+'node2:'+self.dict_v[key][1][2]+'PWL'+self.dict_v[key][2]+'\n'
                Parser_result_info.append(Parser_result_temp)
                '''
            elif(self.dict_v[key][0]=='sin'):
                print (key,":",'value:',self.dict_v[key][0],'node1:',self.dict_v[key][1],'node2:',self.dict_v[key][2])
                Parser_result_temp=key+":"+'value:'+str(self.dict_v[key][0])+'node1:'+self.dict_v[key][1]+'node2:'+self.dict_v[key][2]+'\n'
                Parser_result_info.append(Parser_result_temp)
            else :
                print (key,":",'value:',self.dict_v[key][0],'node1:',self.dict_v[key][1],'node2:',self.dict_v[key][2])
                Parser_result_temp=key+":"+'value:'+str(self.dict_v[key][0])+'node1:'+str(self.dict_v[key][1])+'node2:'+str(self.dict_v[key][2])+'\n'
                Parser_result_info.append(Parser_result_temp)
        for key in self.dict_i.keys():
            print (key,':','node1:',self.dict_i[key][1],'node2:',self.dict_i[key][2])
            Parser_result_temp=key+':'+'node1:'+self.dict_i[key][1]+'node2:'+self.dict_i[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
        #vlotage control source
        for key in self.dict_E.keys():
            print (key,'+ terminal',self.dict_E[key][0],'- terminal',self.dict_E[key][1],'+ control',self.dict_E[key][2],'- control',self.dict_E[key][3])
            Parser_result_temp=key+'+ terminal'+self.dict_E[key][0]+'- terminal'+self.dict_E[key][1]+'+ control'+self.dict_E[key][2]+'- control'+self.dict_E[key][3]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_G.keys():
            print (key,'+ terminal',self.dict_G[key][0],'- terminal',self.dict_G[key][1],'+ control',self.dict_G[key][2],'- control',self.dict_G[key][3])
            Parser_result_temp=key+'+ terminal'+self.dict_G[key][0]+'- terminal'+self.dict_G[key][1]+'+ control'+self.dict_G[key][2]+'- control'+self.dict_G[key][3]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_F.keys():
            print (key,'+ terminal',self.dict_F[key][0],'- terminal',self.dict_F[key][1],'voltage control',self.dict_F[key][2])
            Parser_result_temp=key+'+ terminal'+self.dict_F[key][0]+'- terminal'+self.dict_F[key][1]+'voltage control'+self.dict_F[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
        for key in self.dict_H.keys():
            print (key,'+ terminal',self.dict_H[key][0],'- terminal',self.dict_H[key][1],'voltage control',self.dict_H[key][2])
            Parser_result_temp=key+'+ terminal'+self.dict_H[key][0]+'- terminal'+self.dict_H[key][1]+'voltage control'+self.dict_H[key][2]+'\n'
            Parser_result_info.append(Parser_result_temp)
    #print command
        print ('Command info:')
        #print (self.dict_dot)
        Parser_result_info.append('Command info:\n')
        for key in self.dict_command.keys():
            if (key=='dc'):
                print (key,'analysis:',self.dict_command[key][0],'start from',self.dict_command[key][1],'to',self.dict_command[key][2],'Step',self.dict_command[key][3])
                Parser_result_temp=key+'analysis:'+str(self.dict_command[key][0])+'start from'+str(self.dict_command[key][1])+'to'+str(self.dict_command[key][2])+'Step'+str(self.dict_command[key][3])+'\n'
                Parser_result_info.append(Parser_result_temp)
            elif (key=='ac'):
                print (key,'analysis:',self.dict_command[key][0],'number of samples:',self.dict_command[key][1],'freq start from',self.dict_command[key][2],'to',self.dict_command[key][3])
                Parser_result_temp=key+'analysis:'+str(self.dict_command[key][0])+'number of samples:'+str(self.dict_command[key][1])+'freq start from'+str(self.dict_command[key][2])+'to'+str(self.dict_command[key][3])+'\n'
                Parser_result_info.append(Parser_result_temp)
            elif (key=='tran'):
                print (key,'analysis:','step:',self.dict_command[key][0],'stop at',self.dict_command[key][1])
                Parser_result_temp=key+'analysis:'+'step:'+str(self.dict_command[key][0])+'stop at'+str(self.dict_command[key][1])+'\n'
                Parser_result_info.append(Parser_result_temp)
            else:
                pass
        for key in self.dict_op.keys():
            print (self.dict_op[key][1])
    #end parse output
        print('#---------Parse results END---------#')
        Parser_result_info.append('>>>>>>>>>>>>>>>>>>>Parse results END<<<<<<<<<<<<<<<<<<<\n')
        return Parser_result_info

    def get_time(self,tstr):
        length = len(tstr)
        if (tstr[length-1]=='s'):
            tstr = tstr[0:length-1]
        time =isTools.get_value(tstr)
        if time =='f':
	        return (-1,0)
        else:
            return(time,1)
    def get_frequency(self,fstr):
        length= len(fstr)
        if(fstr[length-2:length]=='hz'):
            fstr = fstr[0:length-2]
        freq=isTools.get_value(fstr)
        if freq=='f':
            return (-1,0)
        else:
            return (freq,1) #use flag to control fault
    def dc_op(self,elements):
        
        step = isTools.get_voltage(elements[3])
        start = isTools.get_voltage(elements[1])
        end = isTools.get_voltage(elements[2])
        if (step[1]==0)&(start[1]==0)&(end[1]==0):
            return (1,start[0],end[0],step[0])
        else :
            return (-1,-1)

#   def get_voltage()

        #print(i)

#test
'''
example_netlist1 = """
*EE105 
vs vs gnd PWL(0s 0V 5ms 0V 5.001ms 5V 10ms 5V)
r1 vs vo  1k
c1 vo gnd 1uF
.tran 0.01ms 10ms
.option post=2 nomod
.end
"""


example_netlist2="""
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
.end
"""

example_netlist3="""
*elmore delay
vin 1 0 pulse (0 1 1 0.2 0.2 6 12)
r1 1 2 1k
c1 2 0 100u
r2 2 3 1k
c2 3 0 100u
r3 2 4 1k
c3 4 0 100u
r4 4 5 1k
c4 5 0 100u
r5 4 6 1k
c5 6 0 100u
r6 6 7 1k
c6 7 0 100u
.tran 0.1 20
.end
"""

testParser = MyParser(example_netlist3)

a,b=testParser.parse()
#print(a)


if (a==-1):
    #print ('hi')
    testParser.showParseResult()
print (testParser.dict_node )
'''