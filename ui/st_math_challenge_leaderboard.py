import os
import tempfile

import streamlit as st
import sys

from ui.utils import upload_file, to_markdown_table

sys.path.append('.')
sys.path.append('..')
from src import math_challenge_leaderboard


def main():
    st.write("Math Challenge Leaderboard\n")
    temp_dir = tempfile.mkdtemp()
    
    with st.form('form_leaderboard'):
        out_path_correct_ans = os.path.join(temp_dir, f"temp_correct_answers.csv")
        upload_file(file_desc="correct answers csv", out_path=out_path_correct_ans, st=st)
        out_path_student_ans = os.path.join(temp_dir, f"temp_student_answers.csv")
        st.write("Hint: to upload data for entries download as csv : https://docs.google.com/forms/d/1ywFv-27_6tyZLipJF5jbhpTyZun_fq9YzzGzYtu5QJs/edit#question=1353810161&field=1006510729")
        upload_file(file_desc="student answers csv", out_path=out_path_student_ans, st=st)
        submitted = st.form_submit_button("Generate Leaderboard")
        if submitted:
            st.write("Leaderboard:")
            leaderboard_list = math_challenge_leaderboard.main(correct_answers_fp=out_path_correct_ans, student_answers_fp=out_path_student_ans)
            st.write(to_markdown_table(leaderboard_list))
            st.write(f"\n\n\nHint: paste this output in https://docs.google.com/spreadsheets/d/15sJ6MhJLbW5Vv27Ifr1dBhkIWGna8_23xSX-PI0yAzs/edit#gid=0")


if __name__ == '__main__':
    main()
