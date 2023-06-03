import streamlit as st
import streamlit_survey as ss
# import pandas as pd
import gspread
import json
import csv

gc = gspread.service_account(filename='creds/survey-bot.json')

SurveyByDate = gc.open_by_key("12jT7RY74jlFLJwBrSymRPGO7i6yUGfwumsMvMN15fFU")
ws = SurveyByDate.get_worksheet(0)
SurveyByPark = gc.open_by_key("10y5NUlQI5Mh8IFnBTC-79W9Nzo4iJisl0S3a6tVX9dw")
SurveyMaster = gc.open_by_key("1E3rIrerqHSpjH5Vq1PSHGljbxxETVG58-v1c7eHItNw")
# st.write(SurveyByDate.sheet1.get('A1')[0][0])
# sh.add_worksheet(title="Park 2", rows=100, cols=20)

survey = ss.StreamlitSurvey()

# text = survey.text_input("Test text", id="ttt")
survey.selectbox("Name", options=["Angela", "Daniel", "Leina"], id="name")
survey.dateinput("Date", id="date")
survey.timeinput("Time", id="time")
survey.radio("District", options=["1", "2", "3", "4", "5"], id="district")
survey.radio("Park/Beach", options=["Park", "Beach"], id="park/beach")
survey.selectbox("Location", options=["","Ala Moana","Aweoweo","Barbers Point","Bellows Field","Black Rocks","Diamond Head","Duke Paoa Kahanamoku","Ehu Kai","Hale'iwa Ali'i","Haleiwa","Hau'ula","Hūnānāniho (Waimānalo Bay)","Joe Lukela","Ka'a'awa","Kahe Point","Kaiaka Bay","Kailua","Kaiona","Kalaeloa","Kalae'o'io","Kalama","Kalaniana'ole","Kapi'olani","Kawaiku'i","Kea'au","Ke'ehi Lagoon","Kokololio","Kualoa","Kūhiō","Kuilei Cliffs","Kuli'ou'ou","La'ielohelohe","Le'ahi","Lualualei","Mā'ili","Mahaka","Makalei","Makapu'u","Makaua","Mauna Lahilahi","Maunalua Bay","Mokule'ia","One'ula","Poka'i Bay","Punalu'u","Pupukea","Pu'uloa","Sandy Beach (Wawamalu)","Sunset","Surfer's","Swanzy","Tracks","Ulehawa","Waiahole","Waiale'e","Wailupe","Waimānalo","Waimea Bay"], id="location")
commAct = survey.selectbox("Type of Commercial Activity", options=["", "Camper van","Exercise class","Kayak","Paddleboard","Scuba","Snorkel","Surf","Swim","Yoga (land)","Yoga (water)","Film","Photography","Food truck","Food sale (small scale)","Luxury picnic","Misc. equipment rental", "Other"], id="typeOfActivity")
if commAct == "Other":
	survey.text_input("Other (please specify)", id="activityOther")
survey.text_input("Company Name", id="companyName")
survey.text_input("PUC", id="PUC")
survey.text_input("Vehicle Description", id="vehicleDescription")
survey.text_input("License Plate #", id="licensePlate")
advert = survey.multiselect("Advertising on Park Property?", options=["Approaching visitors", "Handouts (flyers)", "Vehicle", "Staff clothing", "No"], id="advertising")
if advert == "Other":
	survey.text_input("Other (please specify)", id="advertisingOther")
survey.radio("Did you witness any cash exchange between the operator and consumer at any point during your observation?", options=["Yes", "No"], id="cashExchange")
survey.radio("Recreational Stop? (Watch and time)", options=["Yes", "No"], id="recStop")
survey.radio("Where are the customers located? Are most of the visitors at the bathroom or are most of them out swimming/on the beach?", options=["Rec. Stop appropriate activity (using the bathroom)", "Non-Rec. Stop activity (stopped for purposes other than using the bathroom)"], id="customersLocated")
survey.number_input("Duration of the Rec. Stop in minutes", min_value=0, max_value=99999, value=0, id="recStopDuration")
survey.radio("Intervention?", options=["Yes", "No"], id="intervention")
survey.radio("Accepted education materials?", options=["Yes", "No"], id="acceptedEducationMaterials")
inter = survey.multiselect("Behavior after intervention", options=["Ignored", "Feigning ignorance (making excuses)", "Hostility/Intimidation", "Moved locations (in park or right outside of park)", "Physical Violence", "Threat of physical violence", "Threatening verbiage (calling the mayor, etc.)", "Understanding", "Unaware of rules", "Verbal aggression (yelling, cussing, etc.)", "Other"], id="behaviorAfterIntervention")
if inter == "Other":
	survey.text_input("Other (please specify)", id="behaviorOther")
survey.slider("Rank your feeling of safety based on the individual's response to your intervention", min_value=0, max_value=100, value=0, id="safety")
result = survey.multiselect("Result of the intervention", options=["Called HPD and retreated", "Left without incident", "Perpetrator left the park", "Perpetrator moved locations (in or near park)", "Retreated from situation (no HPD)", "Other"], id="interventionResult")
if result == "Other":
	survey.text_input("Other (please specify)", id="interventionResultOther")
survey.text_area("Any other notes:", id="notes")

headersS = ""
dataS = ""
headers = []
data = []
orig_survey = json.loads(survey.to_json())

if "activityOther" not in orig_survey:
	orig_survey["activityOther"] = {"value": ""}
if "advertisingOther" not in orig_survey:
	orig_survey["advertisingOther"] = {"value": ""}
if "behaviorOther" not in orig_survey:
	orig_survey["behaviorOther"] = {"value": ""}
if "interventionResultOther" not in orig_survey:
	orig_survey["interventionResultOther"] = {"value": ""}

for key in orig_survey:
	headersS += str(key) + ","
	headers.append(key)
	datum = orig_survey[key]["value"]
	if isinstance(datum, list):
		s = '|'.join(datum)
		data.append(s)
		dataS += str(s) + ","
	else:
		data.append(datum)
		dataS += str(datum) + ","

st.write(len(data))
# st.write(headersS + "\n" + str(dataS))
ws.update('A1:Z1', [headers])
ws.update('A2:Z2', [data])
# ws.update('A1:B1', [[5, 6]])
