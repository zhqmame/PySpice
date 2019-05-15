'''
from Parser import MyParser
example_netlist1 = """
*EE105 SPICE Tutorial Example 1 - Simple RC Circuit
vs vs gnd PWL(0s 0V 5ms 0V 5.001ms 5V 10ms 5V)
r1 vs vo  1k
c1 vo gnd 1uF
.tran 0.01ms 10ms
.option post=2 nomod
.end
"""
testParser = MyParser(example_netlist1)
print(testParser.parse())
a=1 and 0
print(a)
'''
a = [1,2,3,4,5]
b = [5,4,3,2,1]
c = [a[i] - b[i] for i in range(len(a))]
print(c)
#print((16*90+4*84)/20)