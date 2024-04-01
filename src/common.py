import os

class Similarity:
    def __init__(self, student_id_a, student_id_b, mse, ssim, psnr):
        self.student_id_a = student_id_a
        self.student_id_b = student_id_b
        self.mse = mse
        self.ssim = ssim
        self.psnr = psnr

class DB:
    def __init__(self):
        self.students = {}
        self.references = {}
        self.connections = {}   # Key: student_id, Value: reference_id and similarity
    
    def add_student(self, student):
        self.students[student.id] = student

    def add_reference(self, reference):
        self.references[reference.id] = reference

    def add_connection(self, student_id_a, student_id_b, mse, ssim, psnr):
        if student_id_a not in self.connections:
            self.connections[student_id_a] = []
        self.connections[student_id_a].append((student_id_b, mse, ssim, psnr))

        if student_id_b not in self.connections:
            self.connections[student_id_b] = []
        self.connections[student_id_b].append((student_id_a, mse, ssim, psnr))
    
    def get_student(self, student_id):
        return self.students[student_id]
    
    def get_reference(self, reference_id):
        return self.references[reference_id]
    
    def get_connection(self, student_id):
        return self.connections[student_id]
    
    def get_documents(self):
        sub_doc_names = []
        ref_doc_names = []
        for s in self.students:
            for name in self.students[s].doc_names:
                sub_doc_names.append(name)
        for r in self.references:
            for name in self.references[r].doc_names:
                ref_doc_names.append(name)
        return sub_doc_names, ref_doc_names


class Student:
    def __init__(self, student_id=None, code_names=None, doc_names=None, etc_names=None):
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
    def __init__(self, reference_id=None, code_names=None, doc_names=None, etc_names=None):
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

def init_database():
    global database
    database = DB()
    return database

def get_database():
    global database
    return database


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
