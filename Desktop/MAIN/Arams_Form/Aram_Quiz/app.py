import streamlit as st
import requests
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, JsCode


DAILY_QUIZ_API_URL = "https://api.aramiasacademy.com/api/quiz"
DAILY_QUIZ_UPDATE_API_URL="https://api.aramiasacademy.com/api/quiz"
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer c5b96872070d0cb990332234df9e9bdc50d91eac3d8c0ad6a7a68bd1f08553683dcaa26da2506b05e36131c91e59002d804694f9beeca8fafeeaba38db9ba126ce7e615747b2b4da194a7b85af51577cda42b34161a89857784f659093bd6824e4b818a1db4259ae9b67c227ee2ee4ea33fd8cf0a5f300517a7b15e1d041a2e8'
}

# Function to fetch data from API
def fetch_data():
    response = requests.get(DAILY_QUIZ_API_URL)
    data = response.json()
    return data["data"]["attributes"]


def update_data(updated_data):
    data = {
        "Title": "Your Title",
        "Subtitle": "Your Subtitle",
        "Quizpoints": ["Today's Subject - Subject Name"],
        "Quiz": updated_data.to_dict(orient="records")
    }
    response = requests.put("DAILY_QUIZ_UPDATE_API_URL", json={"data": data},headers=HEADERS)
    if response.status_code == 200:
        st.success("Data updated successfully!")
    else:
        st.error("Failed to update data.")

        
def display_data(data):
    st.write("## Quiz Data Table")
    df = pd.DataFrame(data["Quiz"])
    # Specify the order of columns
    column_order = ["S_No", "question", "options", "correctAnswer", "explanation", "questionpoint"]
    
    # Add serial number column
    df['S_No'] = range(1, len(df) + 1)
    df = df[column_order]
    
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
    gridOptions = gb.build()
    gridOptions['rowHeight'] = 80  # Set row height
    gridOptions['fontSize'] = 80   # Set font size
    gridOptions['style_data_conditional'] = [{
        'if': {'state': 'active'},  # Apply styles to active state
        'backgroundColor': '#FFDD00',  # Yellow background for active state
        'color': 'black'  # Black text color
    }]
    return AgGrid(df, gridOptions=gridOptions)

# Main function
def main():
    st.title("ARAM IAS ACADEMY-DAILY QUIZ")

    # Fetch data
    data = fetch_data()

    # Display data and allow editing
    edited_data = display_data(data)

    # Submit button to update changes
    if st.button("Submit"):
        updated_data = data
        updated_data["Quiz"] = edited_data.get("data")
        response = update_data(updated_data)
        if response.status_code == 200:
            st.success("Data updated successfully!")
        else:
            st.error("Failed to update data. Please try again.")

if __name__ == "__main__":
    main()