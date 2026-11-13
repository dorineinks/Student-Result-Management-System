
from flask import Flask, render_template_string, request, redirect, url_for
from student import Student
from results import SUBJECTS, calculate_total, calculate_average, assign_grade
from storage import save_students, load_students
from datetime import datetime

app = Flask(__name__)
students = load_students()

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EduManage | Student Management</title>

<style>
* { margin:0; padding:0; box-sizing:border-box; }

body {
    font-family:'Segoe UI',Arial,sans-serif;
    background:#f5f7fb;
    color:#202b3c;
}

.layout { display:flex; min-height:100vh; }

.sidebar {
    width:245px;
    background:#14213d;
    color:white;
    padding:30px 18px;
    position:fixed;
    height:100vh;
}

.brand {
    font-size:22px;
    font-weight:700;
    margin:0 0 45px 10px;
}

.brand span { color:#60a5fa; }

.menu-label {
    color:#94a3b8;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1.5px;
    margin:20px 10px 12px;
}

.nav-link {
    display:block;
    color:#cbd5e1;
    text-decoration:none;
    padding:13px 14px;
    border-radius:8px;
    margin-bottom:7px;
    font-size:14px;
}

.nav-link:hover,.nav-link.active {
    background:#253b60;
    color:white;
}

.main {
    margin-left:245px;
    width:calc(100% - 245px);
    padding:35px 40px;
}

.topbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:30px;
    gap:15px;
}

.topbar h1 { font-size:25px; }

.topbar p {
    color:#8491a5;
    font-size:13px;
    margin-top:6px;
}

.profile {
    background:white;
    padding:10px 16px;
    border-radius:9px;
    font-size:13px;
    font-weight:600;
}

.welcome {
    background:linear-gradient(120deg,#1d3557,#315b91);
    color:white;
    padding:28px;
    border-radius:13px;
    margin-bottom:28px;
}

.welcome h2 { font-size:21px; margin-bottom:8px; }
.welcome p { color:#dbeafe; font-size:14px; }

.stats {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:20px;
    margin-bottom:28px;
}

.stat-card {
    background:white;
    padding:23px;
    border-radius:12px;
    border:1px solid #edf0f5;
}

.stat-card p {
    color:#8491a5;
    font-size:13px;
    margin-bottom:13px;
}

.stat-card h2 { font-size:29px; color:#172b4d; }
.stat-icon { font-size:22px; margin-bottom:12px; }

.panel {
    background:white;
    padding:24px;
    border-radius:12px;
    border:1px solid #edf0f5;
    margin-bottom:25px;
}

.panel-heading {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:22px;
    gap:12px;
}

.panel-heading h2 { font-size:17px; }

table { width:100%; border-collapse:collapse; }

th {
    text-align:left;
    padding:14px 10px;
    color:#8491a5;
    font-size:12px;
    background:#f8fafc;
}

td {
    padding:15px 10px;
    border-bottom:1px solid #edf0f5;
    font-size:13px;
}

.badge {
    background:#eaf2ff;
    color:#2563eb;
    padding:6px 10px;
    border-radius:20px;
    font-size:11px;
}

.form-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
}

.field label {
    display:block;
    font-size:13px;
    font-weight:600;
    margin-bottom:8px;
}

.field input,.field select {
    width:100%;
    padding:13px;
    border:1px solid #dce2eb;
    border-radius:7px;
    outline:none;
    font-size:13px;
}

.field input:focus,.field select:focus { border-color:#2563eb; }

.full { grid-column:1 / -1; }

.btn {
    display:inline-block;
    background:#1d4ed8;
    color:white;
    border:none;
    padding:11px 18px;
    border-radius:7px;
    cursor:pointer;
    font-size:13px;
    font-weight:600;
    text-decoration:none;
}

.btn:hover { background:#1e40af; }

.btn-danger { background:#dc2626; }
.btn-danger:hover { background:#b91c1c; }

.btn-secondary {
    background:#e8edf5;
    color:#26364d;
}
.btn-secondary:hover { background:#dbe3ef; }

.action-link {
    color:#2563eb;
    text-decoration:none;
    font-weight:600;
    margin-right:9px;
}

.alert {
    background:#fee2e2;
    color:#991b1b;
    padding:14px;
    border-radius:8px;
    margin-bottom:20px;
    font-size:13px;
}

.success {
    background:#dcfce7;
    color:#166534;
    padding:14px;
    border-radius:8px;
    margin-bottom:20px;
    font-size:13px;
}

.empty {
    color:#8491a5;
    text-align:center;
    padding:30px;
    font-size:13px;
}

.search-form {
    display:flex;
    gap:10px;
    margin-bottom:20px;
}

.search-form input {
    flex:1;
    min-width:0;
    padding:12px;
    border:1px solid #dce2eb;
    border-radius:7px;
}

.report-header {
    text-align:center;
    border-bottom:2px solid #1d3557;
    padding-bottom:20px;
    margin-bottom:25px;
}

.report-header h2 {
    color:#1d3557;
    margin-bottom:7px;
}

.report-info {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:15px;
    margin-bottom:25px;
    font-size:14px;
}

.report-info p { padding:7px 0; }

.result-summary {
    background:#f0f5ff;
    padding:20px;
    border-radius:10px;
    margin-top:20px;
}

.result-summary h3 { margin-bottom:15px; }

.result-summary p {
    padding:6px 0;
    font-size:14px;
}

footer {
    color:#94a3b8;
    text-align:center;
    font-size:12px;
    padding:20px;
}

@media print {
    .sidebar,.topbar,.no-print,footer { display:none !important; }
    .main { margin:0; width:100%; padding:0; }
    body { background:white; }
    .panel { border:none; box-shadow:none; }
}

@media(max-width:850px) {
    .sidebar { width:190px; }
    .main {
        margin-left:190px;
        width:calc(100% - 190px);
        padding:25px 20px;
    }
    .stats { grid-template-columns:1fr 1fr; }
}

@media(max-width:600px) {
    .layout { display:block; }
    .sidebar {
        position:relative;
        width:100%;
        height:auto;
        padding:15px;
    }
    .brand { margin:0 0 15px; }
    .menu-label { display:none; }
    .sidebar nav { display:flex; flex-wrap:wrap; gap:5px; }
    .nav-link { margin:0; padding:9px; }
    .main { margin:0; width:100%; padding:20px 14px; }
    .stats,.form-grid,.report-info { grid-template-columns:1fr; }
    .full { grid-column:auto; }
    .panel { overflow-x:auto; }
    table { min-width:550px; }
    .search-form { flex-wrap:wrap; }
}
</style>
</head>

<body>
<div class="layout">

<aside class="sidebar">
    <div class="brand">Edu<span>Manage.</span></div>

    <p class="menu-label">Main Menu</p>
    <nav>
        <a class="nav-link {{ 'active' if view == 'dashboard' else '' }}" href="/">▦ &nbsp; Dashboard</a>
        <a class="nav-link {{ 'active' if view == 'add' else '' }}" href="/add">＋ &nbsp; Add Student</a>
        <a class="nav-link {{ 'active' if view in ['students','edit'] else '' }}" href="/students">👥 &nbsp; Students</a>
        <a class="nav-link {{ 'active' if view in ['scores','edit_scores'] else '' }}" href="/scores">▣ &nbsp; Manage Scores</a>
        <a class="nav-link {{ 'active' if view in ['results','report'] else '' }}" href="/results">▤ &nbsp; Student Results</a>
        <a class="nav-link {{ 'active' if view == 'statistics' else '' }}" href="/statistics">▥ &nbsp; Class Statistics</a>
    </nav>
</aside>

<div class="main">

<div class="topbar">
    <div>
        <h1>{{ heading }}</h1>
        <p>Student Result Management System</p>
    </div>
    <div class="profile">Administrator</div>
</div>

{% if message %}
<div class="{{ 'success' if success else 'alert' }}">{{ message }}</div>
{% endif %}

{% if view == 'dashboard' %}

<div class="welcome">
    <h2>Welcome to EduManage</h2>
    <p>Manage student records and monitor academic performance from one place.</p>
</div>

<div class="stats">
    <div class="stat-card">
        <p>Total Registered Students</p>
        <h2>{{ total_students }}</h2>
    </div>
    <div class="stat-card">
        <p>Students With Results</p>
        <h2>{{ students_with_results }}</h2>
    </div>
    <div class="stat-card">
        <p>Overall Class Average</p>
        <h2>{{ overall_average }}%</h2>
    </div>
</div>

<div class="panel">
    <div class="panel-heading">
        <h2>Recently Registered Students</h2>
        <a href="/students">View All →</a>
    </div>
    <table>
        <tr>
            <th>STUDENT ID</th>
            <th>FULL NAME</th>
            <th>CLASS</th>
            <th>GENDER</th>
        </tr>
        {% for student in recent_students %}
        <tr>
            <td>{{ student.student_id }}</td>
            <td>{{ student.full_name }}</td>
            <td>{{ student.class_form }}</td>
            <td>{{ student.gender }}</td>
        </tr>
        {% else %}
        <tr><td colspan="4" class="empty">No students registered yet.</td></tr>
        {% endfor %}
    </table>
</div>

{% elif view == 'add' or view == 'edit' %}

<div class="panel">
    <div class="panel-heading">
        <h2>{{ 'Edit Student Details' if view == 'edit' else 'Register a New Student' }}</h2>
    </div>

    <form method="POST">
        <div class="form-grid">

            <div class="field">
                <label>Student ID</label>
                <input name="student_id"
                    value="{{ student.student_id if student else '' }}"
                    {% if student %}readonly{% endif %} required>
            </div>

            <div class="field">
                <label>Full Name</label>
                <input name="name"
                    value="{{ student.full_name if student else '' }}" required>
            </div>

            <div class="field">
                <label>Class / Form</label>
                <input name="class_form"
                    value="{{ student.class_form if student else '' }}" required>
            </div>

            <div class="field">
                <label>Gender</label>
                <select name="gender" required>
                    <option value="">Select Gender</option>
                    <option value="Male" {% if student and student.gender == 'Male' %}selected{% endif %}>Male</option>
                    <option value="Female" {% if student and student.gender == 'Female' %}selected{% endif %}>Female</option>
                </select>
            </div>

            <div class="field full">
                <label>Date of Birth</label>
                <input type="date" name="dob"
                    value="{{ dob_value }}" required>
            </div>

            <div class="full">
                <button class="btn" type="submit">
                    {{ 'Save Changes' if view == 'edit' else 'Register Student' }}
                </button>
                <a href="/students" class="btn btn-secondary">Cancel</a>
            </div>

        </div>
    </form>
</div>

{% elif view == 'students' %}

<div class="panel">
    <div class="panel-heading">
        <h2>Registered Students</h2>
        <a href="/add" class="btn">+ Add Student</a>
    </div>

    <form method="GET" class="search-form">
        <input type="text" name="search" placeholder="Search by student ID or name..." value="{{ search }}">
        <button class="btn">Search</button>
        <a href="/students" class="btn btn-secondary">Clear</a>
    </form>

    <table>
        <tr>
            <th>STUDENT ID</th>
            <th>FULL NAME</th>
            <th>CLASS</th>
            <th>GENDER</th>
            <th>ACTIONS</th>
        </tr>

        {% for student in student_list %}
        <tr>
            <td>{{ student.student_id }}</td>
            <td>{{ student.full_name }}</td>
            <td>{{ student.class_form }}</td>
            <td>{{ student.gender }}</td>
            <td>
                <a class="action-link" href="/report/{{ student.student_id }}">Report</a>
                <a class="action-link" href="/edit/{{ student.student_id }}">Edit</a>
                <form method="POST" action="/delete/{{ student.student_id }}" style="display:inline"
                    onsubmit="return confirm('Are you sure you want to delete this student?')">
                    <button class="btn btn-danger" style="padding:7px 10px">Delete</button>
                </form>
            </td>
        </tr>
        {% else %}
        <tr><td colspan="5" class="empty">No matching students found.</td></tr>
        {% endfor %}
    </table>
</div>

{% elif view == 'scores' %}

<div class="panel">
    <div class="panel-heading"><h2>Select a Student to Manage Scores</h2></div>
    <table>
        <tr>
            <th>STUDENT ID</th>
            <th>FULL NAME</th>
            <th>CLASS</th>
            <th>ACTION</th>
        </tr>
        {% for student in students %}
        <tr>
            <td>{{ student.student_id }}</td>
            <td>{{ student.full_name }}</td>
            <td>{{ student.class_form }}</td>
            <td><a class="action-link" href="/scores/{{ student.student_id }}">Manage Scores →</a></td>
        </tr>
        {% else %}
        <tr><td colspan="4" class="empty">No students registered.</td></tr>
        {% endfor %}
    </table>
</div>

{% elif view == 'edit_scores' %}

<div class="panel">
    <div class="panel-heading"><h2>Record / Update Scores</h2></div>
    <p>{{ student.full_name }} ({{ student.student_id }})</p>
    <br>
    <form method="POST">
        <div class="form-grid">
            {% for subject in subjects %}
            <div class="field">
                <label>{{ subject }}</label>
                <input type="number" name="{{ subject }}"
                    min="0" max="100" step="0.1"
                    value="{{ student.scores.get(subject, '') }}" required>
            </div>
            {% endfor %}
            <div class="full">
                <button class="btn">Save Scores</button>
            </div>
        </div>
    </form>
</div>

{% elif view == 'results' %}

<div class="panel">
    <div class="panel-heading">
        <h2>Academic Performance</h2>
        <span class="badge">{{ result_rows|length }} Students</span>
    </div>
    <table>
        <tr>
            <th>STUDENT ID</th>
            <th>STUDENT NAME</th>
            <th>TOTAL SCORE</th>
            <th>AVERAGE</th>
            <th>GRADE</th>
            <th>REPORT</th>
        </tr>
        {% for item in result_rows %}
        <tr>
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.total }}</td>
            <td>{{ item.average }}%</td>
            <td><span class="badge">{{ item.grade }}</span></td>
            <td><a class="action-link" href="/report/{{ item.id }}">View</a></td>
        </tr>
        {% else %}
        <tr><td colspan="6" class="empty">No student results available yet.</td></tr>
        {% endfor %}
    </table>
</div>

{% elif view == 'report' %}

<div class="panel" id="report-card">
    <div class="report-header">
        <h2>EDUMANAGE</h2>
        <p>STUDENT ACADEMIC REPORT CARD</p>
    </div>

    <div class="report-info">
        <p><strong>Student ID:</strong> {{ student.student_id }}</p>
        <p><strong>Full Name:</strong> {{ student.full_name }}</p>
        <p><strong>Class:</strong> {{ student.class_form }}</p>
        <p><strong>Gender:</strong> {{ student.gender }}</p>
        <p><strong>Date of Birth:</strong> {{ student.date_of_birth }}</p>
        <p><strong>Academic Session:</strong> Current Session</p>
    </div>

    <h3 style="margin-bottom:15px">Subject Performance</h3>

    <table>
        <tr>
            <th>SUBJECT</th>
            <th>SCORE</th>
            <th>GRADE</th>
        </tr>
        {% for subject, score in student.scores.items() %}
        <tr>
            <td>{{ subject }}</td>
            <td>{{ score }}</td>
            <td>{{ assign_grade(score) }}</td>
        </tr>
        {% endfor %}
    </table>

    {% if student.scores %}
    <div class="result-summary">
        <h3>Academic Summary</h3>
        <p><strong>Total Score:</strong> {{ total }}</p>
        <p><strong>Average Score:</strong> {{ average }}%</p>
        <p><strong>Overall Grade:</strong> {{ grade }}</p>
    </div>
    {% else %}
    <p class="empty">No scores have been recorded for this student.</p>
    {% endif %}

    <div class="no-print" style="margin-top:25px">
        <button class="btn" onclick="window.print()">Print Report Card</button>
        <a href="/students" class="btn btn-secondary">Back to Students</a>
    </div>
</div>

{% elif view == 'statistics' %}

<div class="welcome">
    <h2>Class Performance Overview</h2>
    <p>A summary of students' academic performance.</p>
</div>

<div class="stats">
    <div class="stat-card">
        <p>Total Registered Students</p>
        <h2>{{ total_students }}</h2>
    </div>

    <div class="stat-card">
        <p>Students With Results</p>
        <h2>{{ students_with_results }}</h2>
    </div>

    <div class="stat-card">
        <p>Class Average</p>
        <h2>{{ class_average }}%</h2>
    </div>
</div>

<div class="panel">
    <div class="panel-heading">
        <h2>Academic Performance Statistics</h2>
    </div>

    {% if highest_student %}
    <table>
        <tr>
            <th>PERFORMANCE</th>
            <th>STUDENT NAME</th>
            <th>STUDENT ID</th>
            <th>AVERAGE</th>
        </tr>

        <tr>
            <td>Highest Average</td>
            <td>{{ highest_student.name }}</td>
            <td>{{ highest_student.id }}</td>
            <td>{{ highest_student.average }}%</td>
        </tr>

        <tr>
            <td>Lowest Average</td>
            <td>{{ lowest_student.name }}</td>
            <td>{{ lowest_student.id }}</td>
            <td>{{ lowest_student.average }}%</td>
        </tr>
    </table>
    {% else %}
    <p class="empty">No student results are available yet.</p>
    {% endif %}
</div>
{% endif %}

<footer>EduManage Student Management System | Built with Python and Flask</footer>

</div>
</div>
</body>
</html>
"""


def show_page(view, heading, message="", success=False, **extra):
    result_rows = []

    for student in students:
        if student.scores:
            total = calculate_total(student)
            average = calculate_average(student)

            result_rows.append({
                "id": student.student_id,
                "name": student.full_name,
                "total": round(total, 2),
                "average": round(average, 2),
                "grade": assign_grade(average)
            })

    averages = [item["average"] for item in result_rows]

    data = {
        "view": view,
        "heading": heading,
        "message": message,
        "success": success,
        "total_students": len(students),
        "students_with_results": len(result_rows),
        "overall_average": round(sum(averages) / len(averages), 2) if averages else 0,
        "recent_students": list(reversed(students[-5:])),
        "result_rows": result_rows,
        "students": students,
        "subjects": SUBJECTS,
        "student_list": students,
        "search": "",
        "dob_value": ""
    }

    data.update(extra)

    return render_template_string(
    TEMPLATE,
    assign_grade=assign_grade,
    **data
)


@app.route("/")
def dashboard():
    return show_page("dashboard", "Dashboard")


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student_id = request.form["student_id"].strip()
        name = request.form["name"].strip()
        class_form = request.form["class_form"].strip()
        gender = request.form["gender"]
        dob = request.form["dob"]

        if any(s.student_id.lower() == student_id.lower() for s in students):
            return show_page("add", "Add Student", "Student ID already exists.")

        if not all([student_id, name, class_form, gender, dob]):
            return show_page("add", "Add Student", "Please complete all fields.")

        if gender not in ["Male", "Female"]:
            return show_page("add", "Add Student", "Invalid gender.")

        try:
            parsed_date = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return show_page("add", "Add Student", "Invalid date of birth.")

        student = Student(
            student_id, name, class_form, gender,
            parsed_date.strftime("%d/%m/%Y")
        )

        students.append(student)
        save_students(students)

        return redirect(url_for("dashboard"))

    return show_page("add", "Add Student")


@app.route("/students")
def view_students():
    search = request.args.get("search", "").strip().lower()

    student_list = [
        s for s in students
        if search in s.student_id.lower()
        or search in s.full_name.lower()
    ]

    return show_page(
        "students", "Student Management",
        student_list=student_list,
        search=search
    )


@app.route("/edit/<student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    student = next(
        (s for s in students if s.student_id == student_id),
        None
    )

    if student is None:
        return "Student not found", 404

    if request.method == "POST":
        name = request.form["name"].strip()
        class_form = request.form["class_form"].strip()
        gender = request.form["gender"]
        dob = request.form["dob"]

        if not all([name, class_form, gender, dob]):
            return show_page(
                "edit", "Edit Student",
                "Please complete all fields.",
                student=student,
                dob_value=""
            )

        if gender not in ["Male", "Female"]:
            return show_page(
                "edit", "Edit Student",
                "Invalid gender.",
                student=student,
                dob_value=""
            )

        try:
            parsed_date = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return show_page(
                "edit", "Edit Student",
                "Invalid date.",
                student=student,
                dob_value=""
            )

        student.full_name = name
        student.class_form = class_form
        student.gender = gender
        student.date_of_birth = parsed_date.strftime("%d/%m/%Y")

        save_students(students)

        return redirect(url_for("view_students"))

    try:
        dob_value = datetime.strptime(
            student.date_of_birth, "%d/%m/%Y"
        ).strftime("%Y-%m-%d")
    except ValueError:
        dob_value = ""

    return show_page(
        "edit", "Edit Student",
        student=student,
        dob_value=dob_value
    )


@app.route("/delete/<student_id>", methods=["POST"])
def delete_student(student_id):
    student = next(
        (s for s in students if s.student_id == student_id),
        None
    )

    if student is None:
        return "Student not found", 404

    students.remove(student)
    save_students(students)

    return redirect(url_for("view_students"))


@app.route("/scores")
def manage_scores():
    return show_page("scores", "Manage Scores")


@app.route("/scores/<student_id>", methods=["GET", "POST"])
def edit_student_scores(student_id):
    student = next(
        (s for s in students if s.student_id == student_id),
        None
    )

    if student is None:
        return "Student not found", 404

    if request.method == "POST":
        new_scores = {}

        try:
            for subject in SUBJECTS:
                score = float(request.form[subject])

                if not 0 <= score <= 100:
                    raise ValueError

                new_scores[subject] = score

        except (ValueError, KeyError):
            return show_page(
                "edit_scores", "Manage Student Scores",
                "Invalid scores. Enter numbers between 0 and 100.",
                student=student
            )

        student.scores = new_scores
        save_students(students)

        return redirect(url_for("view_results"))

    return show_page(
        "edit_scores", "Manage Student Scores",
        student=student
    )


@app.route("/results")
def view_results():
    return show_page("results", "Student Results")


@app.route("/report/<student_id>")
def student_report(student_id):
    student = next(
        (s for s in students if s.student_id == student_id),
        None
    )

    if student is None:
        return "Student not found", 404

    total = calculate_total(student) if student.scores else 0
    average = calculate_average(student) if student.scores else 0
    grade = assign_grade(average) if student.scores else "N/A"

    return show_page(
        "report", "Individual Report Card",
        student=student,
        total=round(total, 2),
        average=round(average, 2),
        grade=grade
    )

@app.route("/statistics")
def class_statistics():

    result_students = []

    for student in students:
        if student.scores:
            average = calculate_average(student)

            result_students.append({
                "id": student.student_id,
                "name": student.full_name,
                "average": round(average, 2)
            })

    if result_students:
        highest_student = max(
            result_students,
            key=lambda student: student["average"]
        )

        lowest_student = min(
            result_students,
            key=lambda student: student["average"]
        )

        class_average = round(
            sum(student["average"] for student in result_students)
            / len(result_students), 2
        )
    else:
        highest_student = None
        lowest_student = None
        class_average = 0

    return show_page(
        "statistics",
        "Class Statistics",
        highest_student=highest_student,
        lowest_student=lowest_student,
        class_average=class_average,
        students_with_results=len(result_students)
    )

if __name__ == "__main__":
    app.run(debug=True)

