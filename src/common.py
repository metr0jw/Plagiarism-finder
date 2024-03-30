import os

# project_root is a directory where the directory containing this file is located
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# buffer_dir is a directory where temporary files are stored
# it will be deleted after the program is finished
# If buffer_dir does not exist, create it
os.makedirs(os.path.join(project_root, 'buffer'), exist_ok=True)
buffer_dir = os.path.join(project_root, 'buffer')

# Supported file types
supported_doc_types = ['docx', 'pdf']
supported_code_types = ['c', 'cpp', 'h', 'hpp', 'py', 'java', 'mat', 'm', 'cs', 'asm', 'js', 'v', 'vhd', 'vhdl', 'r']
supported_etc_types = ['txt', 'csv', 'json', 'xml', 'html', 'css', 'yml', 'yaml']
supported_types = supported_doc_types + supported_code_types + supported_etc_types