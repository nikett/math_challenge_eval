# student info, make a class and read from csv; pre-process teacher name
# list of student answers : read from csv,  make a challenge class (correct_ans, challenge_name); make a challengeResponse (student_ans) and pre-process;; ((make a list of challenge that holds all challenges))
# list of correct answers : read from csv
# give pass/fail and score based on grade : create result object and compare a1, a2 and maintain a grade wise map
from typing import Dict, List, Tuple

from prettytable import PrettyTable

from src.challenge import Challenge
from src.result import Result
from src.student_info import StudentInfo


def main(correct_answers_fp, student_answers_fp):
    correct_challenges_dict = Challenge.load_gold_answers(fp=correct_answers_fp)
    student_challenges_list_dict = Challenge.load_student_answers(fp=student_answers_fp)
    student_scores = Result.compute_student_scores(correct_challenges_dict=correct_challenges_dict,
                                                   student_list_challenges_dict=student_challenges_list_dict)
    leaderboard: List[Tuple[StudentInfo, List["Result"]]] = Result.create_leaderboard(student_scores=student_scores)

    print(f"\n\nLeaderboard")
    p = PrettyTable()
    p.field_names = ["student name", "points", "grade", "student info", "ignore_this_minus_points", 'successful submissions', 'num correct']
    for (student, list_results) in leaderboard:
        total_pass = Result.summarize(list_results)['total_num_passed']
        total_correct = Result.summarize(list_results)['total_num_correct']
        p.add_row([student.get_formal_abbreviated_name(),  100* int(total_pass), student.grade, student.__repr__(), -100* int(total_pass), total_pass, total_correct])
    p.reversesort = False
    p.sortby = "ignore_this_minus_points"
    p.align['student info'] = 'l'
    print(p)
    return p


if __name__ == '__main__':
    main(correct_answers_fp="data/correct_answers.csv", student_answers_fp="data/student_answers.csv")
