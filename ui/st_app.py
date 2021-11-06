import sys

sys.path.append('.')
sys.path.append('..')

from ui import st_reflections_judges_input, st_reflections_judges_results

import streamlit as st
import sys

import st_math_challenge_leaderboard


sys.path.append(".")

FUNCTIONALITIES = {
    "Math challenge leaderboard": st_math_challenge_leaderboard,
    "Reflections judges platform": st_reflections_judges_input,
    "Reflections results": st_reflections_judges_results
}


def main():
    st.title("Discovery Elementary volunteering related")
    fn = st.radio("What do you want to do?", list(FUNCTIONALITIES.keys()))
    if fn:
        FUNCTIONALITIES[fn].main()
    else:
        st.write("Please make a selection")


if __name__ == '__main__':
    main()
