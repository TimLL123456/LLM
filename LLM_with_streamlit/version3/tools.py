import json
import pandas as pd
import streamlit as st
from st_supabase_connection import execute_query


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


def is_vaild_booking(df:pd.DataFrame):
    """
    Check if all Vacancy status is available
    """
    return all(i == "available" for i in df["vacancy"].values.tolist())


def recommendation(df, start, end):

    def find_consecutive(lst:list) -> list:
        """
        Return a list of consecutive range
        input: [2, 5, 6, 7]
        output: [(2, 2), (5, 7)]
        """
        
        ### Sorted the list
        sorted_lst = sorted(lst)
        
        ### Find the gaps of non consecutive
        gaps = [[start, end] for start, end in zip(sorted_lst, sorted_lst[1:]) if start + 1 < end]
        
        edges = iter(sorted_lst[:1] + sum(gaps, []) + sorted_lst[-1:])
        
        return list(zip(edges, edges))

    result = {"recommend":[]}
    display_str = "Here is the system recommendation time period (Part of your selected time have been booked):  \n"

    ### User selected time period dataframe
    tmp_df = df[(df["start"] >= start) & (df["end"] <= end)]

    ### All index of available time period from the dataframe
    _indexes = tmp_df.index[tmp_df["user_id"] == 0]
    
    ### Available time period index list
    index_list = _indexes.tolist()

    grouped_period = find_consecutive(index_list)
    
    for period_start_index, period_end_index in grouped_period:
        result["recommend"].append(f"""{tmp_df.loc[period_start_index, "start"]} - {tmp_df.loc[period_end_index, "end"]}\n""")
        display_str += f"""* {tmp_df.loc[period_start_index, "start"]} - {tmp_df.loc[period_end_index, "end"]}  \n"""
    
    st.warning(display_str)


def booking(conn, df:pd.DataFrame, user_id: int):
    """
    Update the status of Vacancy
    """
    df["user_id"] = user_id
    df["vacancy"] = "booked"
    df["date"] = df["date"].astype(str)
    cols = [col for col in df.columns if col not in ("start", "end")]

    records = df[cols].to_dict("records")

    execute_query(conn.table("booking_history").insert(records, count="None"), ttl=0)

    st.balloons()
    st.toast("Booking successful")

    return df


def book_or_cancel_v1(conn, df:pd.DataFrame, date, start, end, action:str):
    """
    Update the status of Vacancy
    """
    ### Find the indexes of all vaild period
    _indexes = df.index[(df["date"] == date) & (df["start"] >= start) & (df["end"] <= end)]
    
    ### Update the vacancy status
    df.loc[_indexes, "Vacancy"] = action

    ### Update DataFrame
    conn.update(worksheet="Booking", data=df)


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


class show_db_data:
    """
    Convert the database response to the template dataframe
    """

    def __init__(self, db_resp:list) -> None:
        self.resp_df = pd.DataFrame(db_resp)


    def construct_template(self, period_range:tuple) -> pd.DataFrame:
        """
        Build empty template dataframe
        """
        ### Create period list
        period_list = [f"{i:02}:00 - {i+1:02}:00" for i in range(period_range[0], period_range[1])]
        rows = len(period_list)
        none_list = [None] * rows
        
        return pd.DataFrame({"user_id": none_list,
                             "date": none_list,
                             "period": period_list,
                             "vacancy": none_list})
    

    def merge_data(self, selected_date:str, template_df:pd.DataFrame) -> pd.DataFrame:
        """
        Merge the database response to the template dataframe
        """
        ### Merge data
        merge_df = pd.merge(template_df, self.resp_df, on='period', how='left', suffixes=('_drop', ''))
        merge_df[["start", "end"]] = merge_df["period"].str.split(" - ", expand=True)

        ### Extract cols
        cols_name = [col for col in merge_df.columns if not (col.endswith("_drop") or col == "id")]
        clean_merge_df = merge_df[cols_name]
        clean_merge_df = clean_merge_df[["user_id", "date", "period", "start", "end", "vacancy"]]

        ### Data cleaning
        clean_merge_df = clean_merge_df.fillna({"date": selected_date, "user_id":0, "vacancy":"available"})
        clean_merge_df["user_id"] = clean_merge_df["user_id"].astype(int)
        # clean_merge_df["start"] = pd.to_datetime(clean_merge_df["start"], format="%H:%M").dt.strftime("%H:%M") ### 08:00. 09:00
        # clean_merge_df["end"] = pd.to_datetime(clean_merge_df["end"], format="%H:%M").dt.strftime("%H:%M")

        return clean_merge_df
