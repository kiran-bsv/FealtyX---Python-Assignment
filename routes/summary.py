from flask import Blueprint, jsonify
from student import students
from ollama import generate_summary

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('', methods=['GET'])
def student_summary(id):
    student = students.get(id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    summary = generate_summary(student)
    return jsonify({'summary': summary}), 200
