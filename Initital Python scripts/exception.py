a = input("enter a number: ")


try:
 for i in range(1, 11):
     print (f"{int(a)} X {i} = {int(a) * i}")
except ValueError:
   print (f"Enter a number insted of {a}")