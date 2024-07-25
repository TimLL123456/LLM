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


def main():

    st.title("📅 Booking System GUI")


    ### Display date input box
    date = st.date_input("Select a date",
                         value=system_info.today,
                         min_value=system_info.today,
                         max_value=system_info.max_day)


    ### Check available period in that day
    if date:
        response = execute_query(st.session_state.connection.table("booking_history").select("*").eq("date", date),ttl=0)
        
        if response.data:

            data = show_db_data(response.data)
            template_df = data.construct_template(system_info.period)
            booking_record = data.merge_data(date, template_df)


            start_options = booking_record[booking_record["user_id"] == 0]["start"].values.tolist()
            start_time = st.selectbox("Select start time", start_options, index=None)


            end_time_list = booking_record[booking_record["end"] > start_time]["end"].values.tolist()
            end_time = st.selectbox("Select end time", end_time_list, index=None)


            if start_time and end_time:

                user_selected_df = booking_record[(booking_record["start"] >= start_time) & (booking_record["end"] <= end_time)]
                user_selected_df
            
        else:
            st.code("Empty list")


menu()
main()