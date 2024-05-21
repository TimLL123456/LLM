import streamlit as st
from streamlit_gsheets import GSheetsConnection
import datetime

def connect_to_gspreadsheet(date):
    """
    Read the ./.streamlit/secrets.toml to get api info
    Connect & Extract data from the google spreadsheets 
    """
    ### Connect to the google spreadsheet
    url = st.secrets['connections']['gsheets']['spreadsheet']
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url, worksheet="Booking", usecols=list(range(3)))

    ### Extract the booking info for the date
    df = df[df["Date"].astype(str) == str(date)]

    return conn, df

def book_or_cancel(conn, df, action:str) -> None:
    """Book or Cancel service booking

    Args:
        conn (_type_): Connection of the google spreadsheets
        df (_type_): DataFrame extract from the google spreadsheets
        action (str): "available / cancel"
    """
    ### Change period vacancy status in the dataframe to "available / cancel"
    _index = df.index[df["Period"] == selected_period].values[0]
    df.loc[_index, "Vacancy"] = action

    ### Update DataFrame
    conn.update(worksheet="Booking", data=df)

    ### Refresh whole page
    st.cache_data.clear()
    st.rerun()

### Set page tab config
st.set_page_config(page_title="Booking System",
                   page_icon="📅")

st.title("📅 Booking System")

# Date
date = st.date_input("Select a date", value=None)

### Check if the date input is None
if date:

    ### Connect to google spreadsheet & Extract data
    conn, df = connect_to_gspreadsheet(date)

    ### Check if the DataFrame is None
    if not df.empty:

        ### Create select box for user book service
        selected_period = st.selectbox("Select a period:",
                                        df['Period'],
                                        index=None,
                                        placeholder="Choose an option")

        ### Check if the period input is None
        if selected_period:

            ### Get the vacancy status for the specificed period
            vacancy_status = df[df["Period"] == selected_period]["Vacancy"].values[0]

            if vacancy_status == "available":
                st.success("This period is available")

                if st.button("Book"):
                    ### Change that period vacancy status
                    book_or_cancel(conn, df, "booked")

            if vacancy_status == "booked":
                st.error("This period is booked")

                if st.button("Cancel"):
                    ### Change that period vacancy status
                    book_or_cancel(conn, df, "available")
        
        ### Highlight the period for selected time period
        st.dataframe(df.style.applymap(lambda x: "background-color: yellow" if x == selected_period else None), width=600, height=600, hide_index=True)
    
    else:
        
        ### Return "Not Data Yet" for empty DataFrame
        st.markdown("<h4 style='text-align: center; '>Not Data Yet</h4>", unsafe_allow_html=True)