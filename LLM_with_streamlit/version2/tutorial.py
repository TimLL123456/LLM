import pickle
import os
from streamlit_authenticator.utilities.hasher import Hasher
import streamlit_authenticator as stauth
import streamlit as st

import yaml
from yaml.loader import SafeLoader

# https://github.com/mkhorasani/Streamlit-Authenticator/tree/main?tab=readme-ov-file#authenticatelogin

#names = ["Amy", "Benny", "Candy"]
#usernames = ["AAmy", "BBenny", "CCandy"]
#passwords = ["abc123", "bcd123", "cde123"]

def encrypt_passwords(passwords):
    hashed_passwords = Hasher(passwords).generate()

    file_path = os.path.join(os.getcwd(), "hashed_pw.pkl")

    with open(file_path, "wb") as file:
        pickle.dump(hashed_passwords, file)

def decrypt_passwords():
    file_path = os.path.join(os.getcwd(), "hashed_pw.pkl")

    with open(file_path, "rb") as file:
        hashed_passwords = pickle.load(file)

def login_form():
    hashed_passwords = Hasher(['abc', 'def']).generate()

    with open('.\config_template.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    name, authentication_status, username = authenticator.login()

    if st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')

    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)

    try:
        username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password()
        if username_of_forgotten_password:
            st.success('New password to be sent securely')
            # The developer should securely transfer the new password to the user.
        elif username_of_forgotten_password == False:
            st.error('Username not found')
    except Exception as e:
        st.error(e)

    with open('.\config_template.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

login_form()