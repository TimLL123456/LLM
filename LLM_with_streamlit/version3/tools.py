import json
import pandas as pd


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

        print(clean_merge_df.dtypes)

        return clean_merge_df
