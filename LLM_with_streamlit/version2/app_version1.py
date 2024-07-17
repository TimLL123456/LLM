from turtle import onclick
import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
import json

### reference: [supabase in streamlit] - https://github.com/SiddhantSadangi/st_supabase_connection


### Things to do:
### 1. Change validation function options > 2 (X True/False)
### 2. Change login status function options > 2 (X True/False)


### Pages
### =====
login_section = st.container(border=True)
signup_section = st.container(border=True)
user_interface_section = st.container()


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


def check_valid_login(response:json,
                      email:str = None,
                      username:str = None,
                      password:str = None):
    """
    Check username/email and password if a valid login

    Valid --> True, Invalid --> False
    """

    if (email != None) and (password != None):
        email_db = response.data[0]['email']
        password_db = response.data[0]['password']

        if (email_db == email) and (password_db == password):
            return True

    if (username != None) and (password != None):
        username_db = response.data[0]['username']
        password_db = response.data[0]['password']

        if (username_db == username) and (password_db == password):
            return True
        
    return False


def is_valid_signup(username:str, email:str, password_1:str, password_2:str) -> bool:
    """
    check if valid to sign up account

    Return True
        username, email, password_1, password_2 != ""
        "@" in email
        password_1 == password_2
    """

    if ('' not in (username, email, password_1, password_2)) and \
        (not is_username(email)) and (password_1 == password_2):

        return True
    
    return False


def show_login_page() -> None:
    """
    Display the login page
    """

    with login_section:
        login_section.title("Login")

        username_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')

        if st.button("Login") and username_n_email != "" and password != "":

            ### When user input is "username"
            if is_username(username_n_email):

                response = execute_query(conn.table("login_information").select("*").eq("username", username_n_email))

                if check_valid_login(response, username=username_n_email, password=password):
                    st.balloons()
                    st.session_state.user_interface = True
                    st.session_state.login_state = False

            ### When user input is "email"
            else:
                response = execute_query(conn.table("login_information").select("*").eq("email", username_n_email))
                
                if check_valid_login(response, email=username_n_email, password=password):
                    st.balloons()
                    st.session_state.user_interface = True
                    st.session_state.login_state = False

        if st.button("Sign up"):
            st.session_state.login_state = False
            st.rerun()


def show_signup_page() -> None:
    """
    Display the sign up page
    """

    with signup_section:
        signup_section.title("Sign up")

        user_name = st.text_input(label='Username', value='', placeholder="Enter your username")
        email = st.text_input(label='Email', value='', placeholder="Enter your email")
        password = st.text_input(label='Password', value='', placeholder="Enter your password", type="password")
        retype_password = st.text_input(label='Confirm password', value='', placeholder="Confirm your password", type="password")

        ### When (user_name not null), (email valid), (password == retype_password)
        if st.button("Create") and is_valid_signup(user_name, email, password, retype_password):
            execute_query(conn.table("login_information").insert([{"username":user_name, "email":email, "password":password}], count="None"), ttl=0)
            
            st.session_state.login_state = True
            st.rerun()

        if st.button("Back"):

            st.session_state.login_state = True
            st.rerun()


def user_interface_page() -> None:
    with user_interface_section:
        st.text_input(label='testing', value='', placeholder="testing")


def main():
    
    if "login_state" not in st.session_state:
        st.session_state.login_state = True


    if "user_interface" not in st.session_state:
        st.session_state.user_interface = False


    if st.session_state.login_state:
        ### Display the login page
        show_login_page()
    else:
        ### Display the sign up page
        show_signup_page()


    if st.session_state.user_interface:
        user_interface_page()

main()