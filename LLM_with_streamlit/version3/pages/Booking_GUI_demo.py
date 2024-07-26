import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
from Menu import menu
from tools import *
from st_supabase_connection import execute_query
from datetime import date, datetime


### Booking range: today + 1 month
class system_info:
    today = date.today()
    max_day = datetime(today.year, today.month+1, today.day)
    period = (7, 23)
    conn = st.session_state.connection
    curr_user_id = st.session_state.user_info["user_id"]


def main():

    st.title("📅 Booking System GUI")


    ### Display date input box
    date = st.date_input("Select a date",
                         value=system_info.today,
                         min_value=system_info.today,
                         max_value=system_info.max_day)


    if date:
        ### Check date available in database
        response = execute_query(system_info.conn.table("booking_history").select("*").eq("date", date),ttl=0)
        

        ### While response not empty
        if response.data:


            ### Construct dataframe template & merge database response to template
            data = show_db_data(response.data)
            template_df = data.construct_template(system_info.period)
            booking_record = data.merge_data(date, template_df)


            ### Display selectbox & Generate start_time list that available (user_id == 0)
            start_options = booking_record[booking_record["user_id"] == 0]["start"].values.tolist()
            start_time = st.selectbox("Select start time", start_options, index=None)


            ### Display selectbox & Generate end_time list that available (user_id == 0) and end_time > start_time
            end_time_list = booking_record[booking_record["end"] > start_time]["end"].values.tolist()
            end_time = st.selectbox("Select end time", end_time_list, index=None)


            ### While start_time & end_time selectbox not NULL
            if start_time and end_time:


                ### Generate dataframe within start and end time
                user_selected_df = booking_record[(booking_record["start"] >= start_time) & \
                                                  (booking_record["end"] <= end_time)]
                

                ### Validate if dataframe is valid
                if is_vaild_booking(user_selected_df):

                    if st.button("Book"):
                        booking(system_info.conn, user_selected_df, system_info.curr_user_id)
                        st.rerun()


                else:
                    recommendation(user_selected_df, start_time, end_time)

                    user_selected_df

            
        else:
            st.markdown("<h4 style='text-align: center; '>No Data Yet</h4>", unsafe_allow_html=True)


menu()
main()