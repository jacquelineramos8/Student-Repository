"""
    Jacqueline Ramos
    810 HW11: This program contains the same classes from HW10:
    Student which stores student information (cwid, name, major) as well a dictionary of their courses and grades
    Instructor which stores instructor information (cwid, name, department) as well as a dictionary of their courses and how many students are in each course
    Major which stores the required and elective courses for each major
    UniversityRepository which reads and stores all students, instructors, grades, and majors info then prints them using pretty table
    ***but adds a method in UniversityRepository that extracts data (student grade summary) from a database and prints it using pretty table
"""

from typing import Dict, DefaultDict, List,Tuple
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Jacqueline_Ramos import file_reader
import os, sys
from statistics import mean
import sqlite3

DB_File = '/Users/jacquelineramos/HW11.db'
db = sqlite3.connect(DB_File)


class Student:
    # this class stores student information (cwid, name, major) as well as a dictionary of their courses and grades
    def __init__(self, cwid: str, name: str, major: str, required:List, elective:List) -> None:
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = dict() #courses[course_name] = grade
        self.stu_course: List = []
        self.stu_grades: List = []
        self.pass_gpa: Dict = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 'C': 2.0}
        self.required: List[str] = required
        self.elective: List[str] = elective

    def store_course_grade(self, course: str, grade: str) -> None:
        # adds student's grade for their course to lists
        if grade in self.pass_gpa:
            self._courses[course] = grade
            self.stu_course.append(course)
            self.stu_grades.append(self.pass_gpa[grade])


    def info(self):
        # this function calculates the student's gpa and required/elective courses
        gpa: float = 0
        if len(self.stu_grades) > 0:
            gpa = round(sum(self.stu_grades)/len(self.stu_grades), 2)
        else:
            gpa = 0.0

        self.required = set(self.required) - set(self._courses)
        if set(self._courses).intersection(set(self.elective)):
            self.elective = []

        return[self._cwid, self._name, sorted(self.stu_course), sorted(self.required), sorted(self.elective), gpa]


class Instructor:
    # this class stores the instructor information (cwid, name, department)
    def __init__(self, cwid: str, name: str, dept: str) -> None:
        self.cwid: str = cwid
        self.name: str = name
        self.dept: str = dept
        self.courses: DefaultDict[str, int] = defaultdict(int) #courses[course_name] = of students who have taken the course.
        self.stu_course: dict = {}


    def store_course_student(self, course: str):
        # dictionary of the course and the number of students in that course
        self.courses[course] += 1


class Major:
    # this class stores major information like the required and elective courses for a major
    def __init__(self, major: str) -> None:
        self._major: str = major
        self._req_courses: List = []
        self._elec_courses: List = []
        self._courses: Dict[str, Dict] = dict()

    def add_course(self, major: str, flag: str, course: str) -> None:
        # this function defines 'R' courses as required and 'E' courses as electives
        if flag == 'R':
            self._req_courses.append(course)
            self._courses[flag] = self._req_courses


        if flag == 'E':
            self._elec_courses.append(course)
            self._courses[flag] = self._elec_courses


    def req_course(self):
        # this function returns a list of the required courses for a major
        return list(self._req_courses)

    def elec_course(self): return list(self._elec_courses)
        # this function returns a list of the elective courses for a major

    def info(self):
        return[self._major, Major.req_course(self), Major.elec_course(self)]


class UniversityRepository:
    # this class reads and stores all the student, instructor, grades, and majors info and prints the info in pretty tables
    def __init__(self, path: str) -> None:
        self._path: str = path
        self._students: Dict[str, Student] = dict()
        self._instructors: Dict[str, Instructor] = dict()
        self._majors: Dict[str, Major] = dict()

        self._read_major(self._path)
        self._read_instructors(self._path)
        self._read_students(self._path)
        self._read_grades(self._path)

        self.student_pretty_table()
        self.instructor_pretty_table()
        self.major_pretty_table()
        self.students_grades_table_db()

    def _read_major(self, path: str) -> None:
        # this function reads each line from file majors.txt and creates an instance of class Major
        try:
            for major, flag, course in file_reader(os.path.join(self._path, 'majors.txt'), 3, "\t", True):
                if major not in self._majors.keys():
                    self._majors[major] = Major(major)
                self._majors[major].add_course(major, flag, course)

        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_students(self, path: str) -> None:
        # this function reads each line from file students.txt and creates an instance of class student
        try:
            for cwid, name, major in file_reader(os.path.join(self._path, 'students.txt'), 3, "\t", True):
                if major in self._majors[major]._major:
                    required = self._majors[major].req_course()
                    elective = self._majors[major].elec_course()
                    self._students[cwid] = Student(cwid, name, major, required, elective)


        except (FileNotFoundError, ValueError) as e:
            print(e)

    def _read_instructors(self, path: str) -> None:
        # this function reads each line from file instructors.txt and creates an instance of class instructor
        try:
            for cwid, name, department in file_reader(os.path.join(self._path, 'instructors.txt'), 3, "\t", True):
                self._instructors[cwid] = Instructor(cwid, name, department)
        except (FileNotFoundError, ValueError) as e:
            print(e)


    def _read_grades(self, path: str) -> None:
        # this function reads the student courses/grades info
        try:
            for student_cwid, course, grades, instructor_cwid in file_reader(os.path.join(self._path, 'grades.txt'), 4, "\t", True):
                if student_cwid in self._students.keys():
                    stu: Student = self._students[student_cwid]
                    stu.store_course_grade(course, grades)
                else:
                    print(f"The Student with CWID : {student_cwid} is unknown.")
                if instructor_cwid in self._instructors.keys():
                    inst: Instructor = self._instructors[instructor_cwid]
                    inst.store_course_student(course)
                else:
                    print(f"The Instructor with CWID : {instructor_cwid} is unknown.")
        except (FileNotFoundError, ValueError) as e:
            if FileNotFoundError:
                print(e)

    def student_pretty_table(self) -> None:
        # this function prints the student info in a pretty table
        pt = PrettyTable(field_names= ['CWID', 'Name', 'Completed Courses', 'Remaining Reuired', 'Remaining Elective', 'GPA'])
        for stu in self._students.values():
            pt.add_row(stu.info())
        print("Student Summary")
        print(pt, "\n")

    def instructor_pretty_table(self) -> None:
        # this function prints the instructor info in a pretty table
        lst1: List = []
        pt = PrettyTable(field_names= ['CWID', 'Name', 'Department', 'Courses', 'Number of Students'])
        for inst in self._instructors.values():
            for k, v in inst.courses.items():
                pt.add_row([inst.cwid, inst.name, inst.dept, k, v])
                lst1.append([inst.cwid, inst.name, inst.dept, k, v])
        print("Instructor Summary")
        print(pt)
        return lst1

    def major_pretty_table(self) -> None:
        # this function prints the majors info in a pretty table
        pt = PrettyTable(field_names=['Major', 'Required Courses', 'Elective Courses'])
        for inst in self._majors.values():
            pt.add_row(inst.info())
        print("Majors Summary")
        print(pt)
    
    def students_grades_table_db(self) -> None:
        # this function prints the student grade summary info from the specified database in a pretty table
        DB_File = 'HW11_Database.db'
        try:
            db = sqlite3.connect(DB_File)
        except sqlite3.OperationalError:
            print('SQLite database not found!')
        else:
            pt = PrettyTable(field_names=['Name', 'CWID', 'Course', 'Grade', 'Instructor'])
            query = "select s.Name, s.CWID, g.Course, g.Grade, i.Name from Students s join Grades g on s.CWID=g.StudentCWID join Instructors i on i.CWID=g.InstructorCWID order by s.Name"
        
            try:
                for row in db.execute(query):
                    pt.add_row(row)
                print('Student Grades')
                print(pt)
            except sqlite3.OperationalError:
                print('SQLite database not found!')



if __name__ == '__main__':
    stevens: UniversityRepository = UniversityRepository("UniversityFiles")