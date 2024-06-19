import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import pandas as pd
import numpy as np

#############################################################################
### Tools ###
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
    
#############################################################################

def connect_to_gspreadsheet(date):
    """
    Read the ./.streamlit/secrets.toml to get api info
    Connect & Extract data from the google spreadsheets 
    """
    ### Refresh whole page
    st.cache_data.clear()
    
    ### Connect to the google spreadsheet
    url = st.secrets['connections']['gsheets']['spreadsheet']
    conn = st.connection("gsheets", type=GSheetsConnection)

    ### Read as DataFrame, Drop None, Transform data type
    df = conn.read(spreadsheet=url, worksheet="Booking", usecols=list(range(5)))
    df = df.dropna()
    df["Start"] = pd.to_datetime(df["Start"], format="%H:%M").dt.strftime("%H:%M") ### 08:00. 09:00
    df["End"] = pd.to_datetime(df["End"], format="%H:%M").dt.strftime("%H:%M")
    
    print(f"Connect to spreadsheet")

    return conn, df

def is_vaild_booking(df:pd.DataFrame):
    """
    Check if all Vacancy status is available
    """
    return all(i == "Available" for i in df["Vacancy"].values.tolist())

def book_or_cancel(conn, df:pd.DataFrame, date, start, end, action:str):
    """
    Update the status of Vacancy
    """
    ### Find the indexes of all vaild period
    _indexes = df.index[(df["Date"] == date) & (df["Start"] >= start) & (df["End"] <= end)]
    
    ### Update the vacancy status
    df.loc[_indexes, "Vacancy"] = action

    ### Update DataFrame
    conn.update(worksheet="Booking", data=df)

    ### Refresh whole page
    st.cache_data.clear()
    st.rerun()

def recommendation(df, start, end):
    result = {"recommend":[]}
    display_str = "Here is the system recommendation time period (Part of your selected time have been booked):  \n"

    ### User selected time period dataframe
    tmp_df = df[(df["Start"] >= start) & (df["End"] <= end)]

    ### All index of available time period from the dataframe
    _indexes = tmp_df.index[tmp_df["Vacancy"] == "Available"]
    
    ### Available time period index list
    index_list = _indexes.tolist()

    grouped_period = find_consecutive(index_list)
    
    for period_start_index, period_end_index in grouped_period:
        result["recommend"].append(f"""{tmp_df.loc[period_start_index, "Start"]} - {tmp_df.loc[period_end_index, "End"]}\n""")
        display_str += f"""* {tmp_df.loc[period_start_index, "Start"]} - {tmp_df.loc[period_end_index, "End"]}  \n"""
    
    st.warning(display_str)

def main():
    ### Set page tab config
    st.set_page_config(page_title="Booking System version2",
                       page_icon="📅")

    st.title("📅 Booking System version2")

    ### Display date input box
    date = st.date_input("Select a date", value=None)

    if date:
        
        ### Connect to google spreadsheet & Extract data
        conn, full_df = connect_to_gspreadsheet(date)
        date = str(date)

        ### Extract Start & End Time
        filter_df = full_df[full_df["Date"] == date]

        ### Check if the date is available
        if not filter_df.empty:
            ### Input start & end time
            ### Display start time
            start_time = st.selectbox("Select start time", filter_df["Start"].values.tolist(), index=None)

            ### Display end time that later than start time
            end_time_list = filter_df[filter_df["End"] > start_time]["End"].values.tolist()
            end_time = st.selectbox("Select end time", end_time_list, index=None)
            
            ### Check if user already inputed the start and end time
            if start_time and end_time:

                ### Display selected period
                user_selected_df = filter_df[(filter_df["Start"] >= start_time) & (filter_df["End"] <= end_time)]

                if is_vaild_booking(user_selected_df):
                    if st.button("Book"):
                        book_or_cancel(conn, full_df, date, start_time, end_time, "Booked")
                else:
                    recommendation(filter_df, start_time, end_time)
                    
                    if st.button("Cancel"):
                        book_or_cancel(conn, full_df, date, start_time, end_time, "Available")
                        

                #user_selected_df
        else:
            ### Return "Not Data Yet" for empty DataFrame
            st.markdown("<h4 style='text-align: center; '>Not Data Yet</h4>", unsafe_allow_html=True)

############################################################
############################################################
main()
