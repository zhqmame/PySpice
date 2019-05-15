import re
import string
def add_node(dictnode,node):
	if node in dictnode.keys():
	# if dictnode.has_key(node):
		return
	else:
		number = len(dictnode)
		dictnode[node]=number
		return dictnode
def add_element(dictelements,element,node1,node2):
	if(dictelements.has_key(node1)) :
		dictelements[node1]['v']=element
	else:
		dictelements[node1]={}
		dictelements[node1]['v']=element
	if(dictelements.has_key(node2)) :
		dictelements[node2]['v']=element
	else:
		dictelements[node2]={}
		dictelements[node2]['v']=element
	print(dictelements)

def get_v_5(dictv,elements,j):

		if((elements[3]!='dc') & (elements[3]!='ac')):

			return 11,j
		else:
			dcvalue= get_voltage(elements[4])

			if (dcvalue[1]==2):
				return 11,j
			elif(dcvalue[1]==0):
				if elements[3]=='dc':
					dictv[elements[0]]=(dcvalue[0],elements[1],elements[2])
					print (dictv[elements[0]])
				else:
					dictv[elements[0]]=(0,elements[1],elements[2],dcvalue[0])
					print (dictv[elements[0]])
			else:
				if (dictv.has_key(dcvalue[0])!=True):

					return 13,j #error 13
				if (elements[3]=='dc'):
					dictv[elements[0]]=(dictv[dcvalue[0]][0],elements[1],elements[2])
					print (dictv[elements[0]])
				else:
					dictv[elements[0]]=(0,elements[1],elements[2],dictv[dcvalue[0]][0])
					print (dictv[elements[0]])
			return -1,-1
def get_i_5(dicti,elements,j):

		if((elements[3]!='dc') & (elements[3]!='ac')):

			return 14,j
		else:
			dcvalue= get_current(elements[4])

			if (dcvalue[1]==2):
				return 14,j
			elif(dcvalue[1]==0):
				if elements[3]=='dc':
					dicti[elements[0]]=(dcvalue[0],elements[1],elements[2])
					print (dicti[elements[0]])
				else:
					dicti[elements[0]]=(0,elements[1],elements[2],dcvalue[0])
					print (dicti[elements[0]])
			else:
				if (dicti.has_key(dcvalue[0])!=True):

					return 16,j #error 16
				if (elements[3]=='dc'):
					dicti[elements[0]]=(dicti[dcvalue[0]][0],elements[1],elements[2])
					print (dicti[elements[0]])
				else:
					dicti[elements[0]]=(0,elements[1],elements[2],dicti[dcvalue[0]][0])
					print (dicti[elements[0]])
			return -1,-1
#def rprint(something):
#	result.insert(INSERT,something)
#	return

def get_frequency(fstr):   #0 is wrong 1 is correct
	length= len(fstr)
	if(fstr[length-2:length]=='hz'):
		fstr = fstr[0:length-2]
	freq=get_value(fstr)
	if freq=='f':
		return (-1,0)
	else:
		return (freq,1)

def get_time(tstr):
	length = len(tstr)
	if (tstr[length-1]=='s'):
		tstr = tstr[0:length-1]
	time = get_value(tstr)

	if time =='f':
		return (-1,0)
	else:
		return(time,1)
def get_voltage(vstr):#return voltage type
	if(vstr[0]=='v'):
		return (vstr,1)
	else:
		if vstr[len(vstr)-1]=='v':
			vstr=vstr[0:len(vstr)-1]
		value = get_value(vstr)
		if(get_value(vstr)!='f'):
			return (get_value(vstr),0)# 0 is a number
		return (3,2)



def get_current(istr):
	if(istr[0]=='i'):
		return (istr,1)
	else:
		if istr[len(istr)-1]=='a':
			istr=istr[0:len(istr)-1]
		value = get_value(istr)
		if(get_value(istr)!='f'):
			return (get_value(istr),0)# 0 is a number
		return (3,2)


## have problem
def get_value(vstr):
	#print (vstr)
	if (vstr.find('.')!=-1):
		valuestr = re.findall('[0-9]+\.[0-9]+',vstr)
		value = float(valuestr[0])
	else :
		valuestr = re.findall('[0-9]+',vstr)
		#print (valuestr)
		value = int(valuestr[0])

	#print value
#	print len(valuestr[0]),len(vstr)
	unit = vstr[len(valuestr[0]):len(vstr)]
	#print (unit)
	if unit=='k':
	#	print "line70 \n"
		value = value*1000
	elif unit=='m':
		value = value *0.001
	elif unit=='u':
		value = value *0.000001
	elif unit=='n':
		value = value *0.000000001
	elif unit=='p':
		value = value *0.000000000001
	elif unit=='f':
		value = value *0.000000000000001
	elif unit=='meg':
		value = value *1000000
	elif unit=='g':
		value = value *1000000000
	elif unit=='t':
		value = value *1000000000000
	elif unit=='':
		value = value
	#elif unit=='uf'
	#	value =value +'unit'

	else:
		return str(value)+unit
	return value


#parse_text1 = ["r2 3 4 5.035", "  "," Rce3 5 7 300k "," R342 3 6 45"," Re3 34 3 5"," Rce3 4 5 999"]
#Parser(parse_text1)
