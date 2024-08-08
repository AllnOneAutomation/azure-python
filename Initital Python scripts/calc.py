import sys


def add(a,b):
    add = a + b
    return add

def sub (a,b):
    sub = a - b
    return sub

def mul (a,b):
    mul = a * b
    return mul

a = float(sys.argv[1])
b = float (sys.argv [3])
operation = sys.argv[2]

if operation == "add":
    print (add(a,b))
elif operation == "sub":
    print (sub(a,b))
elif operation == "mul":
    print (mul(a,b))


