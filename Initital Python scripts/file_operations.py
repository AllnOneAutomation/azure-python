def server_config_update():
    file_path = input("Enter the file path: ")
    key = input("Enter the key: ")
    value = input("Enter the value: ")

    # Check if any of the inputs are empty
    if file_path == "" or key == "" or value == "":
        print("Error: File path, key, and value must not be empty.")
        return


    try:
        with open(file_path, "r") as file:  # read operation
            lines = file.readlines()  # here it took all the lines from the file and stored in lines variable

        with open(file_path, "w") as file:  # write operation
            for line in lines:  # iterating through the lines
                if key in line:  # if key is present in the line
                    file.write(f"{key} = {value}\n")  # then write the key and value in the file
                    print("key updated successfully")
                else:
                    file.write(line)  # if key is not present then write the line as it is

    except Exception as e:
        print(f"Error: {e}")

server_config_update()
