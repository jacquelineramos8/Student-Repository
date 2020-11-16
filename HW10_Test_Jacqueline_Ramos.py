"""
    Jacqueline Ramos
    810 HW10 Test code: This program contains tests for the data printed in the student, instructor, and majors pretty tables
"""


from typing import Dict, List
import unittest

from HW10_Jacqueline_Ramos import UniversityRepository

path_to_test_folder = 'UniversityFiles'
repo_response: UniversityRepository = UniversityRepository(path_to_test_folder)


class Test(unittest.TestCase):
    # this class holds the tests for the student, instructor, and majors info

    def test_data_for_Student(self):
        # tests the student info output 
        calculated: List = [
            ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.44],
            ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.81],
            ['10172', 'Forbes, I', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'],
             3.88],
            ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'],
             ['CS 501', 'CS 513', 'CS 545'], 3.58],
            ['10183', 'Chapman, O', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],
             ['CS 501', 'CS 513', 'CS 545'], 4.0],
            ['11399', 'Cordova, I', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 3.0],
            ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'],
             ['SSW 540', 'SSW 565', 'SSW 810'], 3.92],
            ['11658', 'Kelly, P', [], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 0.0],
            ['11714', 'Morton, A', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'],
             ['SSW 540', 'SSW 565', 'SSW 810'], 3.0],
            ['11788', 'Fuller, E', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 4.0]]

        resp: List = [student.info() for cwid, student in repo_response._students.items()]
        self.assertEqual(calculated, resp)

    def test_data_for_Instructor(self):
        # tests the instructor info output

        calculated: List = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                            ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3],
                            ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3],
                            ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3],
                            ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1],
                            ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1],
                            ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1],
                            ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1],
                            ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                            ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                            ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],
                            ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]

        self.assertEqual(repo_response.instructor_pretty_table(), calculated)


    def test_data_for_Major(self):
        # tests the major info output 

        calculated: List = [['SFEN', ['SSW 540', 'SSW 564', 'SSW 555', 'SSW 567'], ['CS 501', 'CS 513', 'CS 545']],
                            ['SYEN', ['SYS 671', 'SYS 612', 'SYS 800'], ['SSW 810', 'SSW 565', 'SSW 540']]]


        resp: List = [course.info() for major, course in repo_response._majors.items()]
        self.assertEqual(calculated, resp)



if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
