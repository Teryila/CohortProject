from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
from pyngrok import ngrok

app = Flask(__name__)

# In-memory storage for student data
student_data = defaultdict(lambda: defaultdict(float))

# Grading scheme
grading_scheme = {
    "A": (80, 100),
    "B": (70, 79.99),
    "C": (60, 69.99),
    "D": (50, 59.99),
    "F": (0, 49.99)
}

def calculate_grade(score):
    for grade, (low, high) in grading_scheme.items():
        if low <= score <= high:
            return grade
    return "F"

def calculate_exam_status(grades):
    if all(grade in ["A", "B", "C"] for grade in grades):
        return "Pass"
    elif any(grade == "F" for grade in grades):
        return "Fail"
    else:
        return "Retake"

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['student_name']
    course = request.form['course']
    exam_score = float(request.form['exam_score'])

    student_data[student_name][course] = exam_score

    return redirect(url_for('results'))

@app.route('/results')
def results():
    results = []
    for student, courses in student_data.items():
        scores = courses.values()
        average = sum(scores) / len(scores)
        grades = [calculate_grade(score) for score in scores]
        overall_grade = calculate_grade(average)
        exam_status = calculate_exam_status(grades)

        results.append({
            "student": student,
            "courses": courses,
            "average": average,
            "overall_grade": overall_grade,
            "exam_status": exam_status
        })

    return render_template('results.html', results=results)

@app.route('/student/<name>')
def student(name):
    if name in student_data:
        courses = student_data[name]
        scores = courses.values()
        average = sum(scores) / len(scores)
        grades = [calculate_grade(score) for score in scores]
        overall_grade = calculate_grade(average)
        exam_status = calculate_exam_status(grades)

        student_info = {
            "student": name,
            "courses": courses,
            "average": average,
            "overall_grade": overall_grade,
            "exam_status": exam_status
        }

        return render_template('student.html', student=student_info)
    else:
        return "Student not found", 404

if __name__ == '__main__':
    app.run()
