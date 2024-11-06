from flask import Blueprint, request, jsonify
from student import students, add_student, update_student, delete_student, validate_student_data

student_bp = Blueprint('students', __name__)

@student_bp.route('', methods=['POST'])
def create_student():
    data = request.get_json()
    errors = validate_student_data(data)
    if errors:
        return jsonify({"errors": errors}), 400
    student = add_student(data)
    return jsonify({'_id': student.id}), 201

@student_bp.route('', methods=['GET'])
def get_students():
    return jsonify([student.to_dict for student in students.values()]), 200

@student_bp.route('/<int:id>', methods=['GET'])
def get_student(id):
    student = students.get(id)
    if not student:
        return jsonify({'error': "Student not found"}), 404
    return jsonify(student.to_dict), 200

@student_bp.route('/<int:id>', methods=['PUT'])
def update_student_route(id):
    student = students.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    data = request.get_json()
    errors = validate_student_data(data)
    if errors:
        return jsonify({"errors": errors}), 400
    updated_student = update_student(student, data)
    return jsonify(updated_student.to_dict), 200

@student_bp.route('/<int:id>', methods=['DELETE'])
def delete_student_route(id):
    if delete_student(id):
        return '', 204
    return jsonify({'error': 'Student not found'}), 404
