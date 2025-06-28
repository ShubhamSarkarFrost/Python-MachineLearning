## Tkinter File Compression/Decompression Tool
This is a simple desktop application built using Python's Tkinter library that allows you to compress and decompress files. The core compression and decompression logic is separated into dedicated modules for better organization and reusability.

## Features

## 1 -File Compression: Select any file to compress it using zlib (a standard compression library).

## 2 - File Decompression: Select a .zlib compressed file to decompress it back to its original form.

## 3 -Intuitive GUI: User-friendly interface for selecting files and initiating operations.

## 4 -Real-time Status: A status bar provides feedback on the selected files and ongoing operations.



## Prerequisites
This application uses Python's built-in tkinter, os, and zlib modules. No external pip packages are required.

Python 3.x: Ensure you have a compatible version of Python installed.

Project Structure
To run this application, organize your files in the following structure:

my_compression_tool/
├── compression_tool_app.py   # The main Tkinter GUI application
├── compression_logic.py      # Contains the 'compress_file_data' function
├── decompression_logic.py    # Contains the 'decompress_file_data' function
└── README.md                 # This file

How to Run
Save the Code:

Save the code for the main GUI (from the tkinter-compression-tool immersive) as compression_tool_app.py.

Save the compression logic code as compression_logic.py.

Save the decompression logic code as decompression_logic.py.

Place all three Python files in the same directory (e.g., my_compression_tool/).

Execute the Application:
Open a terminal or command prompt, navigate to your my_compression_tool/ directory, and run the main application script:

python compression_tool_app.py

Usage
Launch the App: Run the compression_tool_app.py script.

Compress a File:

In the "Compress File" section, click the "Browse" button next to "Source File:".

Select the file you wish to compress.

Click the "Compress" button. A "Save As" dialog will appear.

Choose a location and filename (default will be original_filename.zlib) and click "Save".

A success message will appear, and the status bar will update.

Decompress a File:

In the "Decompress File" section, click the "Browse" button next to "Compressed File:".

Select a .zlib file that was previously compressed by this tool or any valid zlib compressed file.

Click the "Decompress" button. A "Save As" dialog will appear.

Choose a location and filename (default will attempt to remove .zlib from the original name) and click "Save".

A success message will appear, and the status bar will update.

Troubleshooting
ModuleNotFoundError: If you get an error like ModuleNotFoundError: No module named 'compression_logic', ensure that compression_logic.py and decompression_logic.py are in the same directory as compression_tool_app.py.

zlib.error during decompression: This typically means the file you are trying to decompress is either not a valid zlib compressed file or it has been corrupted.

Permissions Errors: Ensure the application has the necessary read/write permissions for the files and directories you are trying to access.