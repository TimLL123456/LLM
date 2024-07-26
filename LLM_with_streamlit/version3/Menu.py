import streamlit as st
from tools import display_user_info


### Display the sidebar menu before login
def unauthenticated():
    st.sidebar.page_link("pages/login_page.py",label="Login")
    st.sidebar.page_link("pages/signup_page.py",label="Signup")


### Display the sidebar menu after login
def authenticated():
    display_user_info(st.session_state.user_info)
    st.sidebar.page_link("pages/Booking_GUI.py",label="Booking")
    st.sidebar.page_link("pages/LLM_version2.py",label="Booking with AI")
    st.sidebar.page_link("pages/logout_page.py",label="Logout")


def menu():
    ### Non-verified sidebar menu
    if st.session_state.login_state in ["login", "signup"]:
        unauthenticated()


    ### Verified sidebar menu
    if st.session_state.login_state == "verified":
        authenticated()
