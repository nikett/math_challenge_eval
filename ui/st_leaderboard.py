import os
import tempfile

import streamlit as st
import sys

from ui.utils import upload_file, to_markdown_table

sys.path.append('.')
sys.path.append('..')
from src import leaderboard


def main():
    st.write("Math Challenge Leaderboard\n")
    temp_dir = tempfile.mkdtemp()
    
    with st.form('form_leaderboard'):
        out_path_correct_ans = os.path.join(temp_dir, f"temp_correct_answers.csv")
        upload_file(file_desc="correct answers csv", out_path=out_path_correct_ans, st=st)
        out_path_student_ans = os.path.join(temp_dir, f"temp_student_answers.csv")
        upload_file(file_desc="student answers csv", out_path=out_path_student_ans, st=st)
        submitted = st.form_submit_button("Generate Leaderboard")
        if submitted:
            st.write("Leaderboard:")
            leaderboard_list = leaderboard.main(correct_answers_fp=out_path_correct_ans, student_answers_fp=out_path_student_ans)
            st.write(to_markdown_table(leaderboard_list))


if __name__ == '__main__':
    main()
