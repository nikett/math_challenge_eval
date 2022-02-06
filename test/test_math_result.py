import unittest
from typing import Dict, List

from src import math_challenge_leaderboard
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

    def test_score_for_equal_sign(self):
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        student_ans = Challenge(student=top1_student, answers=["0+0.5+0.5=1", "U, Y, and Z", "3", "4"], challenge_name="MC2", is_student_resp=True)
        gold_ans = Challenge(student=None, answers=["1", "{Y}{U}{Z} __OR__ {U}{Z}{Y} __OR__ {U}{Y}{Z}", "3", "4"], challenge_name="MC2", is_student_resp=False)
        r1 = MathChallengeResult()
        r1.passed = True
        self.assertEqual(MathChallengeResult.result(student_ans, gold_ans).__repr__(), r1.__repr__())

    def test_score_with_text_in_ans(self):
        # gold: a. {6–(4+2)+4} b. {4+3–(5+2)+4} c. {(3-1)+4–2+2–2}
        # student: a 6-(4+2)+4 b. 4+3-(5+2)+4 c. (3-1)+4-2+2-2
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        gold_ans, challenge_wise_retaining = Challenge.load_gold_answers(fp="test_data/correct-answers-till4-new.csv")
        student_ans = Challenge.load_student_answers(fp="test_data/test_replacement_student_ans.csv", challenge_wise_retaining=challenge_wise_retaining)
        student_scores: Dict[StudentInfo, List[MathChallengeResult]] = MathChallengeResult.compute_student_scores(correct_challenges_dict=gold_ans, student_list_challenges_dict=student_ans)
        assert student_scores[top1_student][0].num_correct == 12

    def test_score_with_text_in_ans_YZU_question(self):
        # gold: a. {6–(4+2)+4} b. {4+3–(5+2)+4} c. {(3-1)+4–2+2–2}
        # student: a 6-(4+2)+4 b. 4+3-(5+2)+4 c. (3-1)+4-2+2-2
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        gold_ans, challenge_wise_retaining = Challenge.load_gold_answers(fp="test_data/correct-answers-of-mc8.csv")
        student_ans = Challenge.load_student_answers(fp="test_data/test_replacement_student_ans-YZU.csv", challenge_wise_retaining=challenge_wise_retaining)
        student_scores: Dict[StudentInfo, List[MathChallengeResult]] = MathChallengeResult.compute_student_scores(correct_challenges_dict=gold_ans, student_list_challenges_dict=student_ans)
        assert student_scores[top1_student][0].num_correct == 8

    def test_score_when_multiple_correct_gold(self):
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        student_ans = Challenge(student=top1_student, answers=["ans is 1", "2", "3", "4"], challenge_name="MC2", is_student_resp=True)
        gold_ans = Challenge(student=None, answers=["1", "0 __OR__ 2", "3", "4"], challenge_name="MC2", is_student_resp=False)
        r1 = MathChallengeResult()
        r1.passed = True
        r1.num_correct = 4
        r1.num_wrong = 4 - r1.num_correct
        self.assertEqual(MathChallengeResult.result(student_ans, gold_ans).__repr__(), r1.__repr__())

    def test_score_text_ans(self):
        top1_student = StudentInfo(f_name="Top1", l_name="Tandon", grade="First grade", teacher="Ms. Erica Garl", email="blah@blah.com")
        student_ans = Challenge(student=top1_student, answers=["ans is 1", "2", "3", "4"], challenge_name="MC2", is_student_resp=True)
        gold_ans = Challenge(student=None, answers=["1", "0 {blue} __OR__ 2 {grey}", "3", "4"], challenge_name="MC2", is_student_resp=False)
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
