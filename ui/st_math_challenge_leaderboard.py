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
        st.write("Hint: to upload correct answers- download as csv : https://docs.google.com/spreadsheets/d/1Q1LbHEtnZ9LlkRTv4h-UGBLF22QJ4XAXA2ZbAtwIglA/edit#gid=0")
        out_path_correct_ans = os.path.join(temp_dir, f"temp_correct_answers.csv")
        upload_file(file_desc="correct answers csv", out_path=out_path_correct_ans, st=st)
        out_path_student_ans = os.path.join(temp_dir, f"temp_student_answers.csv")
        st.write("Hint: to upload data for entries download as csv : https://docs.google.com/spreadsheets/d/1C_HqLD5SbaUKsPlFLdZ8qfbbdOgyV7u9caqqbCxagRg/edit?resourcekey#gid=1661621218")
        upload_file(file_desc="student answers csv", out_path=out_path_student_ans, st=st)
        diagnostics_for_mc_challenge = st.text_input("produce diagnostics for this particular mc challenge", "MC1")
        submitted = st.form_submit_button("Generate Leaderboard")
        if submitted:
            st.write("Leaderboard:")
            leaderboard_list, diagnostics = math_challenge_leaderboard.main(correct_answers_fp=out_path_correct_ans, student_answers_fp=out_path_student_ans, diagnostics_for_mc_challenge=diagnostics_for_mc_challenge)
            st.write(to_markdown_table(leaderboard_list))
            st.write(f"\n\n\nHint: paste this output in https://docs.google.com/spreadsheets/d/15sJ6MhJLbW5Vv27Ifr1dBhkIWGna8_23xSX-PI0yAzs/edit#gid=0")
            st.write("\n\n")
            st.write(to_markdown_table(diagnostics))



if __name__ == '__main__':
    main()
