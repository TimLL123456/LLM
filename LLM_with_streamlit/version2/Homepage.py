import streamlit as st

def login():
    """
    This function display the GUI of Log in
    """
    st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)

    ### Input email and password
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    ### Display 2 button in same line
    col1, col2 = st.columns(2)

    with col1:
        login_button = st.button("Login", use_container_width=True)

        ### Log in
        if login_button:
            st.markdown("Login")

    with col2:
        signin_button = st.button("Signup", use_container_width=True)

        ### Sign up account and move to "sign up" page
        if signin_button:
            st.session_state.page_status = "signup"
            st.rerun()

def signup():
    """
    This function display the GUI of Sign in
    """
    st.markdown("<h1 style='text-align: center;'>Signup</h1>", unsafe_allow_html=True)

    ### Input email and password
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    ### Display 2 button in same line
    col1, col2 = st.columns(2)

    with col1:
        create_account_button = st.button("Create account", use_container_width=True)

        if create_account_button:
            st.markdown("Created")

    with col2:
        back_button = st.button("Back", use_container_width=True)

        ### Move back to "log in" page
        if back_button:
            st.session_state.page_status = "login"
            st.rerun()


if "page_status" not in st.session_state.keys():
    st.session_state.page_status = "login"

if st.session_state.page_status == "login":
    login()

elif st.session_state.page_status == "signup":
    signup()