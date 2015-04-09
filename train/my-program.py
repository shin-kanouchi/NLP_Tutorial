#!/usr/bin/python
#-*-coding:utf-8-*-
#2014/10/07 15:10:11 Shin Kanouchi


print "Hello World!"


print "***print, data type***"
my_int    = 4
my_float  = 2.5
my_string = "hello"
print "string: %s\tfloat: %s\tint: %d" % (my_string, my_float, my_int)
print my_string, my_float, my_int
print my_string+" "+str(my_float)+" "+str(my_int)


print "***if else, for***"
my_variable = 5
if my_variable == 4:
    print "my_variable is 4"
elif my_variable == 3:
    print "my_variable is 3"
else:    
    print "my_variable is not 3, 4"

for i in range(1, my_variable):
    print "i == %d" % (i)


print "***list***"
my_list = [1, 2, 4, 8, 16]
my_list.append(32)
print len(my_list)
print my_list[3]

for value in my_list:
	print value,


print "***dict***"
my_dict = {"a":5, "b":4, "c":3, "d":2, "e":1}
my_dict["aa"] = 0
print len(my_dict)
print my_dict["c"]

if "d" in my_dict:
    print "d exists in my_dict"

for k, v in sorted(my_dict.items()):
    print "%s --> %r" % (k, v)


print "***defaultdict***"
from collections import defaultdict
my_def_dict = defaultdict(lambda: 0)
my_def_dict["g"] = 33

print my_def_dict["g"]
print my_def_dict["h"]