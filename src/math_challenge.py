import csv
from typing import List, Dict

from src.student_info import StudentInfo


DEFAULT_EMPTY_ANS=-1000000  # if an answer cannot be parsed as an int (e.g., two ducklings or ducklings)


def remove_if_exists(sd, target_challenge_name, student):
    # Timestamps are implicitly represented in the entry order because google sheets appends a new entry at the end.
    # assert not any([x for x in sd[challenge.student] if x.challenge_name == challenge.challenge_name]), f"Repeated entry by the following challenge submission:\n{challenge}"

    #  input = MC1, MC2, MC3, MC4, MC4, MC5, MC6 , check_if_repeated_entry = MC4
    #  output = MC1, MC2, MC3, MC4, MC5, MC6
    all_submissions_by_student = sd[student]  # MC1, MC2, MC3, MC4, MC4, MC5, MC6
    unrepeated_entry = []
    for submission in all_submissions_by_student:  # iterate over all challenge submissions of this student
        if submission.challenge_name != target_challenge_name:
            unrepeated_entry.append(submission)
    sd[student] = unrepeated_entry  # update the master dictionary of student -> list of submissions by removing the duplicate entries.


class Challenge:

    def __init__(self, student: "StudentInfo", answers:List[str], challenge_name: str, is_student_resp: bool, split_ans_on = "__OR__"):
        # TODO: reject a late submission (based on its timestamp, and a deadline dict)
        self.is_student_resp = is_student_resp
        self.challenge_name = challenge_name
        self.answers: List[int] = []
        self.student = student
        for a in answers:
            if a and split_ans_on in a:
                a_s = [self.preprocess_ans(x) for x in a.split(split_ans_on)]
                self.answers.append(a_s)
            else:
                self.answers.append(self.preprocess_ans(a))

    @classmethod
    def preprocess_ans(cls, a) -> int:
        ans = ""
        # answer is 25 ducklings
        # output = 25
        if a:
            for ch in a:
                if ord('0') <= ord(ch) <= ord('9'):
                    ans += ch
            if not ans and len(a) > 0:
                print(f"Check for preprocessing answer: input = {a}, output = {ans}")
        return int(ans) if ans else DEFAULT_EMPTY_ANS

    def __repr__(self):
        return f"challenge name = {self.challenge_name}\nstudent info = {self.student}\n{'' if not self.is_student_resp else 'student_resp:'}\n\t" \
               f"{', '.join([str(a) for a in self.answers])}"

    @classmethod
    def load_gold_answers(cls, fp) -> Dict[str, "Challenge"]:
        alls = {}
        with open(fp) as f_handle:
            for d in csv.DictReader(f_handle):
                challenge_nm = d['Math Challenge name']
                correct_answers = [d[f"Question {x}"] for x in range(1, 19)]
                alls[challenge_nm] = Challenge(student=None,  # gold does not have a student name.
                                               answers=correct_answers,
                                               challenge_name=challenge_nm,
                                               is_student_resp=False)
        return alls

    # TODO set expiration deadlines for challenges.
    @classmethod
    def load_student_answers(cls, fp) -> Dict["StudentInfo", List["Challenge"]]:
        sd: Dict[StudentInfo, List["Challenge"]] = {}
        with open(fp) as f_handle:
            for d in csv.DictReader(f_handle):
                student = StudentInfo(f_name=d['Student first name'], l_name=d['Student last name'], teacher=d["Teacher's name"], grade=d['Grade'], email=d['Username'])
                challenge_nm = d['Math Challenge name']
                correct_answers = [d[f"Question {x}"] for x in range(1, 19)]
                challenge = Challenge(student=student, answers=correct_answers, challenge_name=challenge_nm, is_student_resp=True)
                if challenge.student not in sd:
                    sd[challenge.student] = []
                remove_if_exists(sd=sd, target_challenge_name=challenge.challenge_name, student=challenge.student)
                sd[challenge.student].append(challenge)
        return sd
