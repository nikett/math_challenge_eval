import os
import tempfile

import streamlit as st
import sys

from src.utils import split_csv
from ui.utils import upload_file

sys.path.append('.')
sys.path.append('..')
from src import judges_platform


def main():
    st.write("Reflections judges_platform\n")
    temp_dir = tempfile.mkdtemp()
    
    with st.form('form_judges_platform'):
        data_entries_fp = os.path.join(temp_dir, f"data_entries.csv")
        upload_file(file_desc="data entries file (csv)", out_path=data_entries_fp, st=st)
        website_base_addr = st.text_input('Where will the forms be hosted', 'file://')
        judges_csv = st.text_input('First names of judges (comma separated)', 'Dhivya, Shweta, Thom, Trisha, Whitney')
        form_action = st.text_input('Web app from Google sheets (scripts editor)', 'https://script.google.com/macros/s/AKfycbxM03CgaCSU5PsWahgEa6RLpPZXIm8mhDMEPofdkDJ-1iLjZCv1HiJxr_BU3NlunTYJoQ/exec')
        submitted = st.form_submit_button("Generate judges_platform")

        if submitted:
            out_dir = os.path.join(temp_dir, "judges_forms")
            st.write(f"judges_platform at : {out_dir}")
            judges_platform_cnt = judges_platform.main(data_entries_fp=data_entries_fp,
                                                        out_dir=out_dir,
                                                        website_base_addr=website_base_addr,
                                                        judges=split_csv(judges_csv),
                                                        form_action=form_action
                                                        )
            st.write(f"{judges_platform_cnt} new forms (referenced in the index.html) are stored at the local directory: {out_dir}")


if __name__ == '__main__':
    main()
