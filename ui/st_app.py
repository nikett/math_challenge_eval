import os
import tempfile

import streamlit as st
from prettytable import PrettyTable
import sys

sys.path.append('.')
sys.path.append('..')
from src import leaderboard

def upload_file(file_desc: str, out_path: str):
    '''

    :param file_desc: e.g. correct answers csv
    :param out_path: where will the uploaded data be stored.
    :return:
    '''
    uploaded_correct_file_content = st.file_uploader(f"Upload {file_desc}", type="csv")
    if uploaded_correct_file_content is not None:
        with open(out_path, 'wb') as outfile:
            for line_num, line in enumerate(uploaded_correct_file_content):
                outfile.write(line)
            if line_num == 0:
                st.write(f"Sample line from {file_desc}\n")
                st.write(line)

def to_markdown_table(pt: PrettyTable):
    """
    credit: https://gist.github.com/dbzm/68256c86c60d70072576
    Print a pretty table as a markdown table

    :param py:obj:`prettytable.PrettyTable` pt: a pretty table object.  Any customization
      beyond int and float style may have unexpected effects

    :rtype: str
    :returns: A string that adheres to git markdown table rules
    """
    _junc = pt.junction_char
    if _junc != "|":
        pt.junction_char = "|"
    markdown = [row[1:-1] for row in pt.get_string().split("\n")[1:-1]]
    pt.junction_char = _junc
    return "\n".join(markdown)

def main():
    st.write("Math Challenge Leaderboard\n")
    temp_dir = tempfile.mkdtemp()
    
    with st.form('form_leaderboard'):
        out_path_correct_ans = os.path.join(temp_dir, f"temp_correct_answers.csv")
        upload_file(file_desc="correct answers csv", out_path=out_path_correct_ans)
        out_path_student_ans = os.path.join(temp_dir, f"temp_student_answers.csv")
        upload_file(file_desc="student answers csv", out_path=out_path_student_ans)
        submitted = st.form_submit_button("Generate Leaderboard")
        if submitted:
            st.write("Leaderboard:")
            leaderboard_list = leaderboard.main(correct_answers_fp=out_path_correct_ans, student_answers_fp=out_path_student_ans)
            st.write(to_markdown_table(leaderboard_list))


if __name__ == '__main__':
    main()
