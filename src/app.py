# app.py  –  Flask web server for Student Management System

import os
import sys

# Make sure imports from this package work when run from anywhere
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory
from manager import StudentManager

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

app = Flask(__name__)
manager = StudentManager()
manager.load_students_from_json()


# ── Serve frontend ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


# ── GET all students ──────────────────────────────────────────────────────────
@app.route('/api/students', methods=['GET'])
def get_all_students():
    result = []
    for s in manager.students:
        result.append({
            'enrollment_no': s.enrollment_no,
            'name':          s.name,
            'age':           s.age,
            'marks':         s.marks,
            'average':       round(s.get_average_marks(), 2)
        })
    return jsonify(result)


# ── POST add student ──────────────────────────────────────────────────────────
@app.route('/api/students', methods=['POST'])
def add_student():
    data          = request.get_json()
    enrollment_no = data.get('enrollment_no', '').strip()
    name          = data.get('name', '').strip()
    age           = data.get('age')
    marks         = data.get('marks', {})

    if not enrollment_no or not name or age is None:
        return jsonify({'success': False, 'message': 'enrollment_no, name and age are required.'}), 400

    if any(s.enrollment_no == enrollment_no for s in manager.students):
        return jsonify({'success': False,
                        'message': f"Enrollment No '{enrollment_no}' already exists."}), 400

    manager.add_student(name, int(age), marks, enrollment_no)
    manager.save_students_to_json()
    return jsonify({'success': True,
                    'message': f"Student '{name}' added with Enrollment No: {enrollment_no}."})


# ── GET search (must come before the <enrollment_no> route) ───────────────────
@app.route('/api/students/search', methods=['GET'])
def search_students():
    term    = request.args.get('q', '').strip()
    results = manager.search_student(term)
    return jsonify([{
        'enrollment_no': s.enrollment_no,
        'name':          s.name,
        'age':           s.age,
        'marks':         s.marks
    } for s in results])


# ── GET average marks ─────────────────────────────────────────────────────────
@app.route('/api/students/<enrollment_no>/average', methods=['GET'])
def get_average(enrollment_no):
    average = manager.get_average_marks(enrollment_no)
    if average is not None:
        return jsonify({'success': True,
                        'enrollment_no': enrollment_no,
                        'average':       round(average, 2)})
    return jsonify({'success': False,
                    'message': f"No student found with Enrollment No '{enrollment_no}'."}), 404


# ── DELETE student ────────────────────────────────────────────────────────────
@app.route('/api/students/<enrollment_no>', methods=['DELETE'])
def delete_student(enrollment_no):
    before = len(manager.students)
    manager.delete_student(enrollment_no)
    if len(manager.students) < before:
        manager.save_students_to_json()
        return jsonify({'success': True,
                        'message': f"Student with Enrollment No '{enrollment_no}' deleted."})
    return jsonify({'success': False,
                    'message': f"No student found with Enrollment No '{enrollment_no}'."}), 404


if __name__ == '__main__':
    print("Starting Student Management System server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)
