import streamlit as st
import streamlit_survey as ss
# import pandas as pd
import gspread

gc = gspread.service_account(filename='creds/survey-bot.json')

SurveyByDate = gc.open_by_key("12jT7RY74jlFLJwBrSymRPGO7i6yUGfwumsMvMN15fFU")
# SurveyByPark = gc.open("")
# SurveyMaster = gc.open("")
st.write(SurveyByDate.sheet1.get('A1')[0][0])
# sh.add_worksheet(title="Park 2", rows=100, cols=20)

survey = ss.StreamlitSurvey()

text = survey.text_input("Test text", id="ttt")
survey.selectbox("Selection box:", options=["Option 1", "Option 2", "Option 3", "etc"])
survey.multiselect("Multiple choice:", options=["Option 1", "Option 2", "Option 3", "etc"])
survey.checkbox("Check box")
survey.dateinput("Date input:")
survey.timeinput("Time input:")
survey.text_area("Area input:")
st.number_input("Number input:", min_value=0, max_value=100, value=50)

st.write(survey.to_json())
