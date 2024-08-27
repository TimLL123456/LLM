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

    Return:
        True: equal to username
        False: equal to email
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

    Return:
        True: valid
        False: invalid
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

    Return:
        True: if (username, email, password_1, password_2) != "" & "@" in email & password_1 == password_2
    """

    if ('' not in (username, email, password_1, password_2)) and \
        (not is_username(email)) and (password_1 == password_2):

        return True
    
    return False


def book(user_id, booking_date, booking_start, booking_end):
    input_dict = {"booking_id": 30,
                  "user_id": user_id,
                  "room_id": 1,
                  "booking_date": str(booking_date),
                  "booking_starttime": booking_start,
                  "booking_endtime": booking_end,
                  "totalcost": 0.0,
                  "status_id": 1
                  }

    
    st.session_state.connection.table("bookings").insert(input_dict).execute()


def recommend(start:int, end:int, json_data:list) -> tuple:
    """
    Recommend the available booking period

    Input:
        start(int): the start time of booking
        end(int): the end time of booking
        booked_period(list): a list of booked period

    Return:
        message(str): recommendation period message
        gap(list): a list of all available period in that day
    """

    display_str = "Here is the system recommendation time period (Part of your selected time have been booked):  \n"

    booked_period = [(int(record["booking_starttime"].split(":")[0]), int(record["booking_endtime"].split(":")[0])) for record in json_data]

    ### Find gap between each booked period
    gap = [(first[-1], second[0]) for first, second in zip(booked_period, booked_period[1:]) if first[-1] != second[0]]

    ### Insert the start/end period
    gap.insert(0, (start, booked_period[0][0])) if start < booked_period[0][0] else None
    gap.append((booked_period[-1][-1], end)) if end > booked_period[-1][-1] else None
    
    for period in gap:
        display_str += f"* {period[0]} - {period[1]}  \n"

    return display_str, gap