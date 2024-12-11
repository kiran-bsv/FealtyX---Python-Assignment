import re
from flask import Flask, request, jsonify
from student import Student, students
import threading
from ollama import generate_summary

app = Flask(__name__)
lock = threading.Lock()


def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_student_data(data):
    errors = {}
    if 'name' not in data or not data['name']:
        errors['name'] = "Name is required."
    if 'age' not in data or not isinstance(data['age'], int) or data['age'] <= 0:
        errors['age'] = "Age must be a positive integer."
    if 'email' not in data or not is_valid_email(data['email']):
        errors['email'] = "A valid email is required."
    
    return errors

# demo data
students[1] = Student(id=1, name="kiran bsv", age=21, email="boddepallisai@iitbhilai.ac.in")
students[2] = Student(id=1, name="bakki", age=21, email="bakki@gmail.com")


@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    errors = validate_student_data(data)
    if errors:
        return jsonify({"errors": errors}), 400 
    with lock:
        new_id = len(students)+1
        student=Student(new_id, data['name'], data['age'], data['email'])
        students[new_id] = student
    return jsonify({'_id': new_id}), 201


@app.route('/students', methods=['GET'])
def get_students():
    return jsonify([student.__dict__ for student in students.values()]), 200


@app.route('/students/<int:id>', methods = ['GET'])
def get_student(id):
    student = students.get(id)
    if not student:
        return jsonify({'error': "Student not found"}), 404
    return jsonify(student.__dict__),200


@app.route('/students/<int:id>', methods = ['PUT'])
def update_student(id):
    with lock:
        student = students.get(id)
        if not student:
            return jsonify({'error': 'student not found'}), 404
        errors = validate_student_data(data)
        data = request.get_json()
        if errors:
            return jsonify({"errors": errors}), 400
        if data.get('name'):
            student.name = data['name']
        if data.get('age'):
            student.age = data['age']
        if data.get('email'):
            student.email = data['email']
    return jsonify(student.__dict__), 200

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    with lock:
        if id in students:
            del students[id]
            return '', 204
        return jsonify({'error': 'student not found'}), 404

@app.route('/students/<int:id>/summary', methods=['GET'])
def student_summary(id):
    student = students[id]
    if not student:
        return jsonify({'error': 'student not found'}), 404
    summary = generate_summary(student)
    return jsonify({'summary': summary}), 200

if __name__ == '__main__':
    app.run(debug=True)