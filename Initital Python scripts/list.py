import sys
from env import student_list

student_name = input("Enter student name: ")

if student_name in student_list:
    print (f"{student_name} is present")

else:
    print(f"{student_name} is not present")