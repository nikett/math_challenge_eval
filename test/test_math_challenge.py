import unittest
from typing import Dict, List

from src.math_challenge import Challenge, DEFAULT_EMPTY_ANS
from src.student_info import StudentInfo


class TestChallenge(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(Challenge.preprocess_ans("a. 37th floor, b. 42nd floor, c. 39th floor, d. 40th floor"), 37423940)
        self.assertEqual(Challenge.preprocess_ans("answer is 25 ducklings"), 25)
        self.assertEqual(Challenge.preprocess_ans("4 c.1"), 41)
        self.assertEqual(Challenge.preprocess_ans(a="abcd efgh. ij"), DEFAULT_EMPTY_ANS)
        self.assertEqual(Challenge.preprocess_ans(a="5 blue. ", text_retain_dict={"blue":1}), 51)
        self.assertEqual(Challenge.preprocess_ans(a="5 {blue}. __OR__ 6 {brown}", text_retain_dict={"blue":0, "brown":1}), 5061)
        self.assertEqual(Challenge.preprocess_ans(a="5 blue. ", text_retain_dict={"blue":1}), 51)

    def test_gold_loading(self):
        g, challenge_wise_retaining = Challenge.load_gold_answers(fp="test_data/test_correct_answers.csv")
        assert len(g) == 2
        assert g["MC2"].challenge_name == "MC2"
        assert not g["MC2"].student  # Gold has no student name.
        # We did not pass any retaining text (i.e., usually all text
        # except numbers is removed, except the special retaining strings)
        assert challenge_wise_retaining["MC2"][8] == {"blue":0, "red":1}

    def test_student_ans_loading(self):
        s: Dict[StudentInfo, List["Challenge"]] = Challenge.load_student_answers(fp="test_data/test_student_answers.csv", challenge_wise_retaining={})
        assert len(s) == 5, f"There should be 5 student entries, assuming no repeated entries in the test file."


if __name__ == '__main__':
    unittest.main()
