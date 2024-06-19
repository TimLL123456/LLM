import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class mytools:
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
        # st.cache_data.clear()
        # st.rerun()
        
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
        tmp_df = df[(df["Start"] >= start) & (df["End"] <= end)]

        tmp_df

        ### All index of available time period from the dataframe
        _indexes = tmp_df.index[tmp_df["Vacancy"] == "Available"]

        ### Available time period index list
        index_list = _indexes.tolist()

        grouped_period = find_consecutive(index_list)

        for period_start_index, period_end_index in grouped_period:
            result["recommend"].append(f"""{tmp_df.loc[period_start_index, "Start"]} - {tmp_df.loc[period_end_index, "End"]}\n""")
            display_str += f"""* {tmp_df.loc[period_start_index, "Start"]} - {tmp_df.loc[period_end_index, "End"]}  \n"""

        st.warning(display_str)