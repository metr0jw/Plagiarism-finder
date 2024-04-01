import os

class DB:
    def __init__(self):
        self.students = {}
        self.references = {}
        self.connections = {}
    
    def add_student(self, student):
        self.students[student.id] = student

    def add_reference(self, reference):
        self.references[reference.id] = reference

    def add_connection(self, student_id, reference_id):
        if student_id not in self.connections:
            self.connections[student_id] = []
        self.connections[student_id].append(reference_id)
    
    def get_student(self, student_id):
        return self.students[student_id]
    
    def get_reference(self, reference_id):
        return self.references[reference_id]
    
    def get_connection(self, student_id):
        return self.connections[student_id]
    

class Student:
    def __init__(self):
        self.id = None
        self.code_names = []
        self.doc_names = []
        self.etc_names = []

    def set_id(self, student_id):
        self.id = student_id

    def add_code_dir(self, code_name):
        self.code_names.append(code_name)

    def add_doc_dir(self, doc_name):
        self.doc_names.append(doc_name)

    def add_etc_dir(self, etc_name):
        self.etc_names.append(etc_name)


# inherit student (reference)
class Reference(Student):
    def __init__(self):
        super().__init__()
        self.id = None
        self.code_names = []
        self.doc_names = []
        self.etc_names = []

    def set_id(self, reference_id):
        self.id = reference_id

    def add_code_dir(self, code_name):
        self.code_names.append(code_name)

    def add_doc_dir(self, doc_name):
        self.doc_names.append(doc_name)

    def add_etc_dir(self, etc_name):
        self.etc_names.append(etc_name)


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

if __name__ == '__main__':
    print(project_root)
    print(buffer_dir)
    print(supported_types)
