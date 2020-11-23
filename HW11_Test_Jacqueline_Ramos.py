"""
    Jacqueline Ramos
    810 HW11 TEST: This program contains the test code logic for the newly added student grades summary method 
"""

from typing import Dict, List
import unittest
import os
import sqlite3

from HW11_Jacqueline_Ramos import UniversityRepository


class RepositoryTest(unittest.TestCase):
    # added code logic for the database table information

    def test_student_grades(self) -> None:
        """tests student grade summary info from database is accurately depicted in pretty table
        """
        DB_FILE: str = os.getcwd() + '/HW11_Database.db'
        db: sqlite3.Connection = sqlite3.connect(DB_FILE)
        query: str = """select s.Name as Student, s.CWID, g.Course, g.Grade, i.Name as Instructor
                from students s
                    join grades g on s.CWID=g.StudentCWID
                    join instructors i on i.CWID=g.InstructorCWID
                    order by Student"""

        table_info = {row for row in db.execute(query)}
        exp = {('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'),
               ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
               ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
               ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
               ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
               ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
               ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
               ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
               ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S')
               }
        self.assertEqual(table_info, exp)


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
