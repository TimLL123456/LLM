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
@st.cache_resource
def connect_database():
    """
    Create connection to database
    """
    conn = st.connection("supabase", type=SupabaseConnection)
    return conn


def is_valid_login(response:json,
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


def is_username(string_input:str) -> bool:
    """
    Check whether the user input is username or email

    username --> True, email --> False
    """

    if "@" in string_input:
        return False
    else:
        return True


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


def show_login_page(conn):
    with login_section:
        login_section.title("Login")


        username_n_email = st.text_input(label='Username/Email', value='', placeholder="Enter your username/email")
        password = st.text_input(label='Password', value='', placeholder="Enter your user name", type='password')


        if st.button("Log in") and username_n_email != "" and password != "":

            ### When user input is "username"
            if is_username(username_n_email):

                response = execute_query(conn.table("login_information").select("*").eq("username", username_n_email))

                if is_valid_login(response, username=username_n_email, password=password):
                    st.balloons()
                    st.session_state.login_state = "verified"

            ### When user input is "email"
            else:
                response = execute_query(conn.table("login_information").select("*").eq("email", username_n_email))

                if is_valid_login(response, email=username_n_email, password=password):
                    st.balloons()
                    st.session_state.login_state = "verified"
                    st.rerun()


        if st.button("Sign up"):
            st.session_state.login_state = "signup"
            st.rerun()


def show_signup_page(conn):
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
            
            st.session_state.login_state = "login"
            st.rerun()

        if st.button("Back"):

            st.session_state.login_state = "login"
            st.rerun()


def show_interface_page(conn):
    st.header("User interface")

    with interface_section:

        pass


def main():
    conn = connect_database()

    ### login_state = ["login", "signup", "verified"]
    if "login_state" not in st.session_state:
        st.session_state.login_state = "login"


    if st.session_state.login_state == "login":
        show_login_page(conn)
    
    elif st.session_state.login_state == "signup":
        show_signup_page(conn)

    elif st.session_state.login_state == "verified":
        show_interface_page(conn)


main()