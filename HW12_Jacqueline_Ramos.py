"""
    Jacqueline Ramos
    810 HW12: This program contains code that queries a database and reads an html template, 
    then creates a web page returning the desired info in a table from the database. 
"""

import sqlite3
from flask import Flask, render_template
from typing import Dict, List, Tuple

DB_FILE='HW11_Database.db'

app=Flask(__name__)

@app.route('/student_summary')
def student_summary() -> str:
    """ This function connects to the HW11 database file and queries the database file for student info
    including the student's name, cwid, course, grade, and instructor's name. This information is iterated through
    and stored in the dictionary named 'data'.

    The render_template method is then used to input the student's info into the student_summary html template.
    This template inputs the databse info into a table and this table is then presented on a webpage.
    """

    db = sqlite3.connect(DB_FILE)
    
    query = "select s.Name, s.CWID, g.Course, g.Grade, i.Name from Students s join Grades g on s.CWID=g.StudentCWID join Instructors i on i.CWID=g.InstructorCWID order by s.Name"

    data: Dict[str, str] = [{'name': name, 'cwid': cwid, 'course': course, 'grade': grade, 'instructor': instructor} for name, cwid, course, grade, instructor in db.execute(query)]
    
    db.close()

    return render_template('student_summary.html', title='Stevens Repository', table_title='Student, Course, Grade, and Instructor', students=data)

app.run(debug=True)