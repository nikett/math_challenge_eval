import csv
import os
from typing import List, Dict, Any

from prettytable import PrettyTable

from src.student_info import StudentInfo

# todo in the future: fix bug in forms.html -- missing art title
# todo add _OR_ in answers of math challenge when answers are a list.

class ReflectionsJudge:
    def __init__(self, judge_name: str, expertise_in_category: str):
        self.judge_name = judge_name.lower().strip()
        self.expertise_in_category = expertise_in_category.lower().strip()
        self.is_expert = self.expertise_in_category != ""

    def __hash__(self):
        return hash(self.judge_name)

    def __eq__(self, other: "ReflectionsJudge"):
        return self.judge_name == other.judge_name

class ReflectionsJudgeScore:
    def __init__(self, judge: ReflectionsJudge, csv_entry_dict: Dict[str, Any]):
        self.judge = judge
        self.interpretation: int = int(csv_entry_dict['interpretation'].lower().strip())
        self.interpretation_comments = csv_entry_dict['interpretation_comments']
        self.creativity: int = int( csv_entry_dict['creativity'].lower().strip())
        self.creativity_comments = csv_entry_dict['creativity_comments']
        self.technique: int = int( csv_entry_dict['technique'].lower().strip())
        self.technique_comments = csv_entry_dict['technique_comments']
        self.other_comments = csv_entry_dict['other_comments']
        self.is_coi: bool = csv_entry_dict['coi'].lower().strip() == "yes"
        self.confidence = csv_entry_dict['confidence']  # Sort of confident, Not confident, Very confident
        self.entry_category = csv_entry_dict['entry_category']
        self.unweighted_score = self.compute_total_score()
        self.weighted_score = self.compute_weighted_score()

    def compute_total_score(self):
        return self.interpretation + self.creativity + self.technique

    def compute_weighted_score(self):
        wt = 0.0
        if self.confidence == "Sort of confident":
            wt = 0.66
        elif self.confidence == "Very confident":
            wt = 1.0
        elif self.confidence == "Not confident":
            wt = 0.33

        if self.judge.expertise_in_category == self.entry_category:
            wt = 2.0 * wt
        return wt * self.unweighted_score

    def __repr__(self):
        return f"{self.judge.judge_name}: {self.unweighted_score}"

class ReflectionsEntry:
    def __init__(self,
                 entry_id,
                 student_info: StudentInfo,
                 judges_scores: List[ReflectionsJudgeScore],
                 entry_file_types,
                 entry_urls,
                 entry_category,
                 entry_statement
                 ):
        self.entry_id = entry_id
        self.student_info = student_info
        self.judges_scores = []
        for j in judges_scores:
            self.add_judge_score(j)
        self.urls = entry_urls
        self.file_types = entry_file_types
        self.category = entry_category
        self.statement = entry_statement

    def add_judge_score(self, judge_score: ReflectionsJudgeScore):
        # do not allow repeated entries, remove the previous entry for this judge, and add the new entry.
        duplicate_indices = []
        for idx, x in enumerate(self.judges_scores):
            if x.judge == judge_score.judge:
                duplicate_indices.append(idx)
        for idx in duplicate_indices:
            self.judges_scores.pop(idx)
        self.judges_scores.append(judge_score)

    def __hash__(self):
        return hash(self.entry_id)

    def __eq__(self, other: "ReflectionsEntry"):
        return self.entry_id == other.entry_id


class ReflectionsResult:
    def __init__(self, entry: ReflectionsEntry, ignore_coi: bool, min_num_judges_per_entry:int):
        # retain the last judge scoring entry from csv only
        self.entry = entry
        self.judges_scores = entry.judges_scores
        self.ignore_coi = ignore_coi
        self.min_num_judges_per_entry = min_num_judges_per_entry
        self.scoring_complete: bool = self.scoring_complete_for_entry()
        self.num_judges = len(self.judges_scores)
        self.weighted_avg_score = self.get_weighted_sum_of_scores()/self.num_judges
        self.unweighted_avg_score = self.get_unweighted_sum_of_scores()/self.num_judges
        self.max_formula_score = self.get_max_formula_sum_of_scores()/self.num_judges

    def scoring_complete_for_entry(self):
        # Atleast one expert judge has scored. Make sure the judge has not marked it as a COI if we care about COIs.
        expert_looked_at_it = any([judge_score.judge.is_expert and (self.ignore_coi or not judge_score.is_coi) for judge_score in self.judges_scores])
        sufficient_judges = len(self.judges_scores) >= self.min_num_judges_per_entry
        return expert_looked_at_it and sufficient_judges

    def get_max_formula_sum_of_scores(self):
        non_expert_scores = [judge_score for judge_score in self.judges_scores if not judge_score.judge.is_expert]
        expert_scores = [judge_score for judge_score in self.judges_scores if judge_score.judge.is_expert]
        return max([x.weighted_score for x in non_expert_scores]) + sum([x.weighted_score for x in expert_scores])

    def get_weighted_sum_of_scores(self):
        return sum([x.weighted_score for x in self.judges_scores])

    def get_unweighted_sum_of_scores(self):
        return sum([x.unweighted_score for x in self.judges_scores])

    def __repr__(self):
        return f"scoring complete = {self.scoring_complete}, weighted score = {self.weighted_avg_score}, unweighted_score={self.unweighted_avg_score}, dict of scores = {self.judges_scores}"

    @classmethod
    def mk_pretty_table(cls, result_list: List["ReflectionsResult"]) -> PrettyTable:
        p = PrettyTable()
        p.field_names = ["evaluation completed", "student name", "points_weighted", "points_unweighted", "points_max_formula", "grade", "list of scores", "student info"]
        for result in result_list:
            p.add_row([result.scoring_complete, result.entry.student_info.get_formal_abbreviated_name(), result.weighted_avg_score, result.unweighted_avg_score, result.max_formula_score, result.entry.student_info.grade, result.entry.judges_scores, result.entry.student_info.__repr__()])
        p.reversesort = True
        p.sortby = "points_max_formula"
        p.align['student info'] = 'l'
        return p

def create_entries(judges_scores_fp: str, judges_expertise: Dict[str, str]) -> List[ReflectionsEntry]:
    # one student can have multiple entries, and multiple entries can be selected from one student.
    d: Dict[ReflectionsEntry, List[ReflectionsJudgeScore]] = {}

    with open(judges_scores_fp) as infile:
        for j in csv.DictReader(infile):
            student_info = StudentInfo(f_name = j['entry_student_first_name'],
                                       l_name = j['entry_student_last_name'],
                                       teacher = j['entry_student_teacher_name'],
                                       grade = j['entry_grade'],
                                       email = j['entry_parent_email_id']
                                       )
            entry = ReflectionsEntry(entry_id=j['entry_id'],
                                     entry_category=j['entry_category'],
                                     entry_file_types=j['entry_file_types'],
                                     entry_urls=j['entry_urls'],
                                     entry_statement=j['entry_statement'],
                                     student_info=student_info,
                                     judges_scores=[])
            judge_name = j['judge_name'].lower().strip()
            assert judge_name in judges_expertise, f"Judge name {judge_name} not found in {judges_expertise}"
            judge = ReflectionsJudge(judge_name=judge_name, expertise_in_category=judges_expertise[judge_name])
            if entry not in d:
                d[entry] = []
            d[entry].append(ReflectionsJudgeScore(judge=judge, csv_entry_dict=j))

    # create entries to evaluate
    entries: List[ReflectionsEntry] = []
    for entry, judge_scores in d.items():
        for j in judge_scores:
            entry.add_judge_score(j)
        entries.append(entry)
    return entries

def main(judges_scores_fp: str, judges_expertise: Dict[str, str], ignore_coi: bool, min_num_judges_per_entry:int) -> PrettyTable:
    judges_expertise = {k.lower(): v for k,v in judges_expertise.items()}
    assert os.path.exists(judges_scores_fp), f"Check judges scores file path: {judges_scores_fp}"
    reflections_entries = create_entries(judges_scores_fp=judges_scores_fp, judges_expertise=judges_expertise)
    reflections_results = [ReflectionsResult(entry=entry, ignore_coi=ignore_coi, min_num_judges_per_entry=min_num_judges_per_entry) for entry in reflections_entries]
    return ReflectionsResult.mk_pretty_table(reflections_results)


# if __name__ == '__main__':
#     # Visual Arts
#     # Music composition
#     # Literature
#     # Film/Video
#     # Photography
#     sample_judges_expertise: Dict[str, str] = {
#         "shweta": "Visual Arts",
#         "whitney": "Music composition",
#         "thom": "Literature",
#         "trisha": "",
#         "dhivya priya v": ""
#     }
#     main(judges_scores_fp="data/judges_output/scores-submission-v2-data.csv",
#          judges_expertise=sample_judges_expertise,
#          min_num_judges_per_entry=3,
#          ignore_coi=False
#          )
