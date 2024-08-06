import streamlit as st
import json


def display_user_info(user_info):
    """
    Function to display user info in the sidebar with custom styling
    """
    st.sidebar.markdown("""
        <style>
            .user-info {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .user-info h3 {
                color: #333;
                margin-bottom: 10px;
            }
            .user-info p {
                color: #666;
                margin: 5px 0;
                font-size: 14px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
        <div class="user-info">
            <p><strong>User ID:</strong> {user_info['user_id']}</p>
            <p><strong>Username:</strong> {user_info['username']}</p>
            <p><strong>Email:</strong> {user_info['email']}</p>
        </div>
    """, unsafe_allow_html=True)


def is_username(string_input:str) -> bool:
    """
    Check whether the user input is username or email

    username --> True, email --> False
    """

    if "@" in string_input:
        return False
    else:
        return True


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