def remove_space_from_file(filepath):
    try:
        # Step 1: Read the content of the file
        with open(filepath, 'r') as file:
            file_data = file.read() # Read the entire content

        # Step 2: Process the data (remove extra space)
        processed_data = file_data.strip() # .strip() removes leading/trailing whitespace

        # Step 3: Write the processed data back to the same file (this will overwrite it)
        with open(filepath, 'w') as file:
            file.write(processed_data)
            print(f"File '{filepath}' has been completely removed of extra leading/trailing space.")

    except FileNotFoundError:
        print(f"Error: No file has been found in the directory: {filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example Usage:
# First, create a dummy file with some leading/trailing spaces for testing
with open('read.txt', 'w') as f:
    f.write("   This is a test file.   \n")
    f.write("Another line with spaces. \n")
    f.write("  End of file.  ")

print("--- Before removing spaces ---")
with open('read.txt', 'r') as f:
    print(f.read())

remove_space_from_file('read.txt')

print("\n--- After removing spaces ---")
with open('read.txt', 'r') as f:
    print(f.read())
