import unittest

from src.challenge import Challenge
from src.result import Result
from src.student_info import StudentInfo


class TestChallenge(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(Result.passed_as_per_grade(num_correct=5, grade="Kindergarten"), True)
        self.assertEqual(Result.passed_as_per_grade(num_correct=0, grade="Kindergarten"), False)
        self.assertEqual(Result.passed_as_per_grade(num_correct=3, grade="Kindergarten"), True)
        self.assertEqual(Result.passed_as_per_grade(num_correct=5, grade="Fourth grade"), False)
        self.assertEqual(Result.passed_as_per_grade(num_correct=15, grade="Fourth grade"), True)

    def test_summarize(self):
        r1 = Result()
        r1.passed = True
        r1.num_correct = 4
        r1.num_wrong = 18 - 4
        results = [r1, r1, r1]
        self.assertEqual(Result.summarize(results)["total_num_passed"], 3)
        self.assertEqual(Result.summarize(results)["total_num_correct"], 12)

    def test_score(self):
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl")
        student_ans = Challenge(student=top1_student, answers=["ans is 1", "2", "3", "4"], challenge_name="MC2", is_student_resp=True)
        gold_ans = Challenge(student=None, answers=["1", "0", "3", "4"], challenge_name="MC2", is_student_resp=False)
        r1 = Result()
        r1.passed = True
        r1.num_correct = 3
        r1.num_wrong = 4 - 3
        self.assertEqual(Result.score(student_ans, gold_ans).__repr__(), r1.__repr__())

    def test_create_leaderboard(self):
        r1 = Result()
        r1.passed = True
        r1.num_correct = 4
        r1.num_wrong = 18 - 4
        r2 = Result()
        r2.passed = False
        r2.num_correct = 2
        r2.num_wrong = 18 - 2
        results1 = [r1, r1, r1]
        results2 = [r1, r2, r2]
        results3 = [r2, r2, r2]

        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl")
        top2_student = StudentInfo(f_name="Top2", l_name="Tandon", grade="Kindergarten", teacher="Ms. Kathy Madden")
        top3_student = StudentInfo(f_name="Top3", l_name="Tandon", grade="Kindergarten", teacher="Ms. Erica Madden")

        student_scores = {
            top1_student: results1,
            top2_student: results2,
            top3_student: results3
        }
        leaderboard = Result.create_leaderboard(student_scores=student_scores)
        self.assertEqual(leaderboard[2][0], top3_student)
        self.assertEqual(leaderboard[0][0], top1_student)


if __name__ == '__main__':
    unittest.main()
