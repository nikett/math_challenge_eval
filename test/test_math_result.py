import unittest

from src import math_leaderboard
from src.math_challenge import Challenge
from src.math_challenge_result import MathChallengeResult
from src.student_info import StudentInfo


class TestChallenge(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(MathChallengeResult.passed_as_per_grade(num_correct=5, grade="Kindergarten"), True)
        self.assertEqual(MathChallengeResult.passed_as_per_grade(num_correct=0, grade="Kindergarten"), False)
        self.assertEqual(MathChallengeResult.passed_as_per_grade(num_correct=3, grade="Kindergarten"), True)
        self.assertEqual(MathChallengeResult.passed_as_per_grade(num_correct=5, grade="Fourth grade"), False)
        self.assertEqual(MathChallengeResult.passed_as_per_grade(num_correct=15, grade="Fourth grade"), True)

    def test_summarize(self):
        r1 = MathChallengeResult()
        r1.passed = True
        r1.num_correct = 4
        r1.num_wrong = 18 - 4
        results = [r1, r1, r1]
        self.assertEqual(MathChallengeResult.summarize(results)["total_num_passed"], 3)
        self.assertEqual(MathChallengeResult.summarize(results)["total_num_correct"], 12)

    def test_score(self):
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        student_ans = Challenge(student=top1_student, answers=["ans is 1", "2", "3", "4"], challenge_name="MC2", is_student_resp=True)
        gold_ans = Challenge(student=None, answers=["1", "0", "3", "4"], challenge_name="MC2", is_student_resp=False)
        r1 = MathChallengeResult()
        r1.passed = True
        r1.num_correct = 3
        r1.num_wrong = 4 - r1.num_correct
        self.assertEqual(MathChallengeResult.result(student_ans, gold_ans).__repr__(), r1.__repr__())

    def test_score_when_multiple_correct_gold(self):
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        student_ans = Challenge(student=top1_student, answers=["ans is 1", "2", "3", "4"], challenge_name="MC2", is_student_resp=True)
        gold_ans = Challenge(student=None, answers=["1", "0 __OR__ 2", "3", "4"], challenge_name="MC2", is_student_resp=False)
        r1 = MathChallengeResult()
        r1.passed = True
        r1.num_correct = 4
        r1.num_wrong = 4 - r1.num_correct
        self.assertEqual(MathChallengeResult.result(student_ans, gold_ans).__repr__(), r1.__repr__())

    def test_create_leaderboard(self):
        r1 = MathChallengeResult()
        r1.passed = True
        r1.num_correct = 4
        r1.num_wrong = 18 - 4
        r2 = MathChallengeResult()
        r2.passed = False
        r2.num_correct = 2
        r2.num_wrong = 18 - 2
        results1 = [r1, r1, r1]
        results2 = [r1, r2, r2]
        results3 = [r2, r2, r2]

        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        top2_student = StudentInfo(f_name="Top2", l_name="Tandon", grade="Kindergarten", teacher="Ms. Kathy Madden", email="blah@blah.com")
        top3_student = StudentInfo(f_name="Top3", l_name="Tandon", grade="Kindergarten", teacher="Ms. Erica Madden", email="blah@blah.com")

        student_scores = {
            top1_student: results1,
            top2_student: results2,
            top3_student: results3
        }
        leaderboard = MathChallengeResult.create_leaderboard(student_scores=student_scores)
        self.assertEqual(leaderboard[2][0], top3_student)
        self.assertEqual(leaderboard[0][0], top1_student)

    # def test_create_leaderboard_from_file(self):
    #     p =leaderboard.main(correct_answers_fp="data/bug/bugfix_correct_ans.csv",
    #                         # student_answers_fp="data/bug/bugfix_user_resp.csv"
    #                         student_answers_fp="data/bug/all-resp-until-mc2.csv"
    #                         )


if __name__ == '__main__':
    unittest.main()
