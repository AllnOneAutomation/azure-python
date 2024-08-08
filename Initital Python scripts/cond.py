import sys

type = sys.argv[1]

if type == "t2.micro":
    print ("This will charge $2 to you")

elif type == "t2.medium":
    print ("This will charge $4 to you")

elif type == "t2.large":
    print ("This will charge $8 to you")

else:
    print("Please give a valid instance type")