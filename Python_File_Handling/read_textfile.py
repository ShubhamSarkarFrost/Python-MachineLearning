#####<----------------  read data from a file --------------------->######
def read_text_file(filepath):
    try:
        with open(filepath, 'r') as file:
            content = file.read()
            print(f"File Read Successfully and it has content : \n {content}")
            file.close()
    except FileNotFoundError:
        print(f"No file has been found in the directory ${filepath}")


def write_text_file(filepath, data, mode):
     try:
         with open(filepath, mode) as file:
             file.write(data)
             print("Value successfully written to the file")
             file.close()
     except IOError as e:
         print(f"Error: Could not write to file '{filepath}'. Reason: {e}")
         return False
     except Exception as e:
         print(f"An unexpected error occurred while writing to '{filepath}': {e}")
         return False



#####<-------- code runner ------------->########
#read_text_file('read.txt')

user_data = input("Please enter your data")
write_text_file('read.txt', user_data, 'a')

