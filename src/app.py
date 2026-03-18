# app.py  –  Flask web server for Student Management System

import os
import sys
import io

import matplotlib
matplotlib.use('Agg')  # headless backend for server-side rendering
import matplotlib.pyplot as plt

# Make sure imports from this package work when run from anywhere
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from manager import StudentManager

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

app = Flask(__name__)
CORS(app)
manager = StudentManager()
manager.load_students_from_json()


def _avg_dataframe():
    df = manager.to_dataframe()
    if df.empty:
        return None
    df['average'] = df['average'].astype(float)
    return df


def _figure_to_png(fig):
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf


def _bar_chart(df):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(df['name'], df['average'], color="#4e79a7")
    ax.set_xlabel('Student')
    ax.set_ylabel('Average Marks')
    ax.set_title('Average Marks per Student (Bar)')
    ax.set_ylim(bottom=0)
    ax.tick_params(axis='x', rotation=35)
    return _figure_to_png(fig)


def _pie_chart(df):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df['average'], labels=df['name'], autopct='%1.1f%%', startangle=120)
    ax.set_title('Average Marks Share (Pie)')
    return _figure_to_png(fig)


# ── Serve frontend ────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')


# ── GET all students ──────────────────────────────────────────────────────────
@app.route('/api/students', methods=['GET'])
def get_all_students():
    df = manager.to_dataframe()
    if df.empty:
        return jsonify([])
    df['average'] = df['average'].round(2)
    return jsonify(df.to_dict(orient='records'))


# ── Charts: Average per student (bar & pie) ──────────────────────────────────
@app.route('/api/charts/average/bar', methods=['GET'])
def chart_average_bar():
    df = _avg_dataframe()
    if df is None:
        return jsonify({'success': False, 'message': 'No data to chart.'}), 404
    buf = _bar_chart(df)
    return send_file(buf, mimetype='image/png')


@app.route('/api/charts/average/pie', methods=['GET'])
def chart_average_pie():
    df = _avg_dataframe()
    if df is None:
        return jsonify({'success': False, 'message': 'No data to chart.'}), 404
    buf = _pie_chart(df)
    return send_file(buf, mimetype='image/png')


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
    app.run(host='127.0.0.1', port=5000, debug=False)
