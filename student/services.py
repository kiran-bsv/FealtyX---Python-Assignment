from student.models import Student
from utils.threading_utils import global_lock as lock

students = {
    1: Student(id=1, name="kiran bsv", age=21, email="boddepallisai@iitbhilai.ac.in"),
    2: Student(id=2, name="bakki", age=21, email="bakki@gmail.com")
}

def add_student(data):
    with lock:
        new_id = len(students) + 1
        student = Student(new_id, data['name'], data['age'], data['email'])
        students[new_id] = student
    return student

def update_student(student, data):
    with lock:
        if 'name' in data:
            student.name = data['name']
        if 'age' in data:
            student.age = data['age']
        if 'email' in data:
            student.email = data['email']
    return student

def delete_student(id):
    with lock:
        if id in students:
            del students[id]
            return True
        return False
