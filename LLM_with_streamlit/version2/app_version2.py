import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import json

### Pages
### =====
login_section = st.container(border=True)
signup_section = st.container(border=True)
interface_section = st.container()


### Connect to database
### ===================
conn = st.connection("supabase", type=SupabaseConnection)


def is_username(string_input:str) -> bool:
    """
    Check whether the user input is username or email

    username --> True, email --> False
    """

    if "@" in string_input:
        return False
    else:
        return True


def show_login_page():
    with login_section:
        login_section.title("Login")


        username_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')


        if st.button("Login") and username_n_email != "" and password != "":

            ### When user input is "username"
            if is_username(username_n_email):

                response = execute_query(conn.table("login_information").select("*").eq("username", username_n_email))


    pass


def show_signup_page():
    pass


def show_interface_page():
    pass


def main():

    ### login_state = ["login", "signup", "verified"]
    if "login_state" not in st.session_state:
        st.session_state.login_state = "login"


    if st.session_state.login_state == "login":
        show_login_page()
    
    elif st.session_state.login_state == "signup":
        show_signup_page()

    elif st.session_state.login_state == "verified":
        show_signup_page()

main()