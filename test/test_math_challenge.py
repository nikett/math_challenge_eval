import unittest
from typing import Dict, List

from src.math_challenge import Challenge, DEFAULT_EMPTY_ANS
from src.student_info import StudentInfo


class TestChallenge(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(Challenge.preprocess_ans("answer is 25 ducklings"), 25)
        self.assertEqual(Challenge.preprocess_ans("4 c.1"), 41)
        self.assertEqual(Challenge.preprocess_ans("abcd efgh. ij"), DEFAULT_EMPTY_ANS)

    def test_gold_loading(self):
        g: Dict[str, Challenge] = Challenge.load_gold_answers(fp="test_data/test_correct_answers.csv")
        assert len(g) == 2
        assert g["MC2"].challenge_name == "MC2"
        assert not g["MC2"].student  # Gold has no student name.

    def test_student_ans_loading(self):
        s: Dict[StudentInfo, List["Challenge"]] = Challenge.load_student_answers(fp="test_data/test_student_answers.csv")
        assert len(s) == 5, f"There should be 5 student entries, assuming no repeated entries in the test file."


if __name__ == '__main__':
    unittest.main()
