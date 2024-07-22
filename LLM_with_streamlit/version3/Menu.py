import streamlit as st


def unauthenticated():
    st.sidebar.page_link("pages/login_page.py",label="Login")
    st.sidebar.page_link("pages/signup_page.py",label="Signup")

def authenticated():
    st.sidebar.page_link("pages/Booking_version2.py",label="Booking")
    st.sidebar.page_link("pages/LLM_version2.py",label="Booking with AI")


def menu():

    if st.session_state.login_state in ["login", "signup"]:
        unauthenticated()

    if st.session_state.login_state == "verified":
        authenticated()
