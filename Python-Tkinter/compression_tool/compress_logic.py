import zlib
import os


def compress_file_data(source_filepath, output_filepath):
    try:
        if not os.path.exists(source_filepath):
            return False, "Source File Not Found"
        with open(source_filepath,'rb') as f_in:
            original_data = f_in.read()
            compressed_data = zlib.compress(original_data, level=9)
        with open(output_filepath, 'wb') as f_out:
            f_out.write(compressed_data)

        return True,""
    except Exception as e:
         return False, f"An error occured during compression, {e}"