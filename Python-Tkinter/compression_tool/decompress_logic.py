import zlib
import os


def decompress_file_data(source_path, output_filepath):
    try:
        if not os.path.exists(source_path):
            return False, "Compressed File not Found"
        with open(source_path, 'rb') as f_in:
            compressed_data = f_in.read()
        decompressed_data = zlib.decompress(compressed_data)
        with open(output_filepath, 'wb') as f_out:
            f_out.write(decompressed_data)
        return True, ""
    except zlib.error as e:
        return False, f"Invalid zlib compressed file or corrupted data: {e}"
    except Exception as e:
        return False, f"An error occurred during decompression: {e}"
