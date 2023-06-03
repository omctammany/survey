import streamlit as st
# import streamlit_survey as ss
# import pandas as pd
import gspread

gc = gspread.service_account(filename='creds/survey-bot.json')

sh = gc.open("Survey By Date")
st.write(sh.sheet1.get('A1'))

# survey = ss.StreamlitSurvey()

# text = survey.text_input("Test text", id="ttt")
# survey.selectbox("Selection box:", options=["Option 1", "Option 2", "Option 3", "etc"])
# survey.multiselect("Multiple choice:", options=["Option 1", "Option 2", "Option 3", "etc"])
# survey.checkbox("Check box")
# survey.dateinput("Date input:")
# survey.timeinput("Time input:")
# survey.text_area("Area input:")
# st.number_input("Number input:", min_value=0, max_value=100, value=50)

# survey.to_json()


# gc = gspread.service_account()
# wks = gc.open