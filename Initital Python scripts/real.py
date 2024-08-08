import os 

folders = input("Enter the folder name: ").split()

for folder in folders:
  try:
    files = os.listdir(folder)
    print (f"Below are the output for {folder}:")
    for file in files:
     print (file)
  except FileNotFoundError:
    print("Folder not found", folder)
    continue
  except PermissionError:
    print("perissions denied to", folder)
    break
