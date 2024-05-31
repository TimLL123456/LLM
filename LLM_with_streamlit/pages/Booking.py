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
    df = conn.read(spreadsheet=url, worksheet="Booking", usecols=list(range(5)))

    return conn, df

def book_or_cancel(conn, full_df, df, date, selected_period, action:str) -> None:
    """Book or Cancel service booking

    Args:
        conn (_type_): Connection of the google spreadsheets
        full_df (_type_): Full DataFrame extract from the google spreadsheets
        df (_type_): Selected period DataFrame extract from the google spreadsheets
        date (_type_): date that user selected
        selected_period (_type_): Period that user selected
        action (str): "available / cancel"
    """
    ### Change period vacancy status in the dataframe to "available / cancel"
    ### 2024-05-22 | 07:00 - 08:00 | available -> 2024-05-22 | 07:00 - 08:00 | booked
    _index = df.index[df["Period"] == selected_period].values[0]
    df.loc[_index, "Vacancy"] = action

    ### Update the new df to the full df
    _indexes = full_df.index[full_df["Date"] == str(date)].values
    full_df.loc[_indexes, "Vacancy"] = df["Vacancy"].values

    ### Update DataFrame
    conn.update(worksheet="Booking", data=full_df)

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
    conn, full_df = connect_to_gspreadsheet(date)

    ### Extract the booking info for the date
    df = full_df[full_df["Date"].astype(str) == str(date)]

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

            if vacancy_status == "Available":
                st.success("This period is Available")

                if st.button("Book"):
                    ### Change that period vacancy status
                    book_or_cancel(conn, full_df, df, date, selected_period, "booked")

            if vacancy_status == "booked":
                st.error("This period is booked")

                if st.button("Cancel"):
                    ### Change that period vacancy status
                    book_or_cancel(conn, full_df, df, date, selected_period, "Available")
        
        ### Highlight the period for selected time period
        st.dataframe(df.style.applymap(lambda x: "background-color: yellow" if x == selected_period else None), width=600, height=600, hide_index=True)
    
    else:
        
        ### Return "Not Data Yet" for empty DataFrame
        st.markdown("<h4 style='text-align: center; '>Not Data Yet</h4>", unsafe_allow_html=True)