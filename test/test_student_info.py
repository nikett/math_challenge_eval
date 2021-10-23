import unittest

from src.student_info import StudentInfo


class TestStudentInfo(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(StudentInfo.preprocess_teacher_name("Mrs. Garl"), "garl")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Mrs. Erica Garl"), "garl")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Erica Garl"), "garl")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Erica G."), "g")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Garl, Erica"), "erica")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Erica"), "erica")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Ms.garl"), "garl")
        self.assertEqual(StudentInfo.preprocess_teacher_name("Mrs. Smnis"), StudentInfo.preprocess_teacher_name("Smnis"))


if __name__ == '__main__':
    unittest.main()
