import streamlit as st
from streamlit_gsheets import GSheetsConnection

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
