import streamlit as st
import streamlit_survey as ss
import gspread
import json
import csv
from PIL import Image
import os, shutil
import cloudinary
# import cloudinary.file_uploader
# import cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# Config
cloudinary.config(
  cloud_name = "dnrxpsxic",
  api_key = "947682472312968",
  api_secret = "EJ4SC2G8ORcX_2cQWMFBrNwiXBY",
  secure = True
)

st.header("Data Collection Form")

survey = ss.StreamlitSurvey()

survey.selectbox("Name", options=["Angela", "Daniel", "Leina"], id="Name")
survey.dateinput("Date", id="Date")
survey.timeinput("Time", id="Time")
survey.radio("District", options=["1", "2", "3", "4", "5"], id="District")
survey.radio("Park/Beach", options=["Park", "Beach"], id="Park/Beach")
survey.selectbox("Location", options=["","Ala Moana","Aweoweo","Barbers Point","Bellows Field","Black Rocks","Diamond Head","Duke Paoa Kahanamoku","Ehu Kai","Hale'iwa Ali'i","Haleiwa","Hau'ula","Hūnānāniho (Waimānalo Bay)","Joe Lukela","Ka'a'awa","Kahe Point","Kaiaka Bay","Kailua","Kaiona","Kalaeloa","Kalae'o'io","Kalama","Kalaniana'ole","Kapi'olani","Kawaiku'i","Kea'au","Ke'ehi Lagoon","Kokololio","Kualoa","Kūhiō","Kuilei Cliffs","Kuli'ou'ou","La'ielohelohe","Le'ahi","Lualualei","Mā'ili","Mahaka","Makalei","Makapu'u","Makaua","Mauna Lahilahi","Maunalua Bay","Mokule'ia","One'ula","Poka'i Bay","Punalu'u","Pupukea","Pu'uloa","Sandy Beach (Wawamalu)","Sunset","Surfer's","Swanzy","Tracks","Ulehawa","Waiahole","Waiale'e","Wailupe","Waimānalo","Waimea Bay"], id="Location")
commAct = survey.selectbox("Type of Commercial Activity", options=["", "Camper van","Exercise class","Kayak","Paddleboard","Scuba","Snorkel","Surf","Swim","Yoga (land)","Yoga (water)","Film","Photography","Food truck","Food sale (small scale)","Luxury picnic","Misc. equipment rental", "Other"], id="Type of Activity")
if "Other" in commAct:
	survey.text_input("Other (please specify)", id="activityOther")
survey.text_input("Company Name", id="Company Name")
survey.text_input("PUC", id="PUC")
survey.text_input("Vehicle Description", id="Vehicle Description")
survey.text_input("License Plate #", id="License Plate")
advert = survey.multiselect("Advertising on Park Property?", options=["Approaching visitors", "Handouts (flyers)", "Vehicle", "Staff clothing", "No", "Other"], id="Advertising")
if "Other" in advert:
	survey.text_input("Other (please specify)", id="advertisingOther")
survey.radio("Did you witness any cash exchange between the operator and consumer at any point during your observation?", options=["Yes", "No"], id="Cash Exchange")
survey.radio("Recreational Stop? (Watch and time)", options=["Yes", "No"], id="Rec Stop")
survey.radio("Where are the customers located? Are most of the visitors at the bathroom or are most of them out swimming/on the beach?", options=["Rec. Stop appropriate activity (using the bathroom)", "Non-Rec. Stop activity (stopped for purposes other than using the bathroom)"], id="Customer Location")
survey.number_input("Duration of the Rec. Stop in minutes", min_value=0, max_value=99999, value=0, id="Rec Stop Duration")
survey.radio("Intervention?", options=["Yes", "No"], id="Intervention")
survey.radio("Accepted education materials?", options=["Yes", "No"], id="Accepted Education Materials")
inter = survey.multiselect("Behavior after intervention", options=["Ignored", "Feigning ignorance (making excuses)", "Hostility/Intimidation", "Moved locations (in park or right outside of park)", "Physical Violence", "Threat of physical violence", "Threatening verbiage (calling the mayor, etc.)", "Understanding", "Unaware of rules", "Verbal aggression (yelling, cussing, etc.)", "Other"], id="Behavior After Intervention")
if "Other" in inter:
	survey.text_input("Other (please specify)", id="behaviorOther")
survey.slider("Rank your feeling of safety based on the individual's response to your intervention", min_value=0, max_value=100, value=0, id="Feeling of Safety")
result = survey.multiselect("Result of the intervention", options=["Called HPD and retreated", "Left without incident", "Perpetrator left the park", "Perpetrator moved locations (in or near park)", "Retreated from situation (no HPD)", "Other"], id="Intervention Result")
if "Other" in result:
	survey.text_input("Other (please specify)", id="interventionResultOther")
survey.text_area("Any other notes:", id="Notes")

def submit():
	# first parse the survey into the right format for writing
	headers = []
	data = []
	orig_survey = json.loads(survey.to_json())

	if "Other" in commAct:
		orig_survey["Type of Activity"]["value"].remove("Other")
		orig_survey["Type of Activity"]["value"].append(orig_survey["activityOther"]["value"])
	if "Other" in advert:
		orig_survey["Advertising"]["value"].remove("Other")
		orig_survey["Advertising"]["value"].append(orig_survey["advertisingOther"]["value"])
	if "Other" in inter:
		orig_survey["Behavior After Intervention"]["value"].remove("Other")
		orig_survey["Behavior After Intervention"]["value"].append(orig_survey["behaviorOther"]["value"])
	if "Other" in result:
		orig_survey["Intervention Result"]["value"].remove("Other")
		orig_survey["Intervention Result"]["value"].append(orig_survey["interventionResultOther"]["value"])

	# delete previous picures in the temp folder so we don't go over 1gb resource limit
	for pic in os.listdir("temp"):
		file_path = os.path.join("temp", pic)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path):
				shutil.rmtree(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


	# upload pics to cloudinary
	urls = []
	for pic in pics:
		file_details = {"FileName":pic.name,"FileType":pic.type}
		img = Image.open(pic)
		path = os.path.join("temp",pic.name)
		with open(path,"wb") as f: 
			f.write(pic.getbuffer())

		ret = upload(path, public_id=pic.name)
		urls.append(ret["url"])

	orig_survey["Pictures"] = {"value": urls}

	for key in orig_survey:
		if "Other" in key:
			continue
		headers.append(key)
		datum = orig_survey[key]["value"]
		if key == "pictures":
			s = '\n'.join(datum)
			data.append(s)
		elif isinstance(datum, list):
			s = '|'.join(datum)
			data.append(s)
		else:
			data.append(datum)

	# get setup with the service account for google sheets
	gc = gspread.service_account(filename='creds/survey-bot.json')

	# check if the worksheet already exists, and create one if it doesn't
	SurveyByDate = gc.open_by_key("12jT7RY74jlFLJwBrSymRPGO7i6yUGfwumsMvMN15fFU")
	try:
		wsDate = SurveyByDate.worksheet(orig_survey["Date"]["value"])
	except:
		wsDate = SurveyByDate.add_worksheet(title=orig_survey["Date"]["value"], rows=10000, cols=27)

	SurveyByPark = gc.open_by_key("10y5NUlQI5Mh8IFnBTC-79W9Nzo4iJisl0S3a6tVX9dw")
	try:
		wsPark = SurveyByPark.worksheet(orig_survey["Location"]["value"])
	except:
		wsPark = SurveyByPark.add_worksheet(title=orig_survey["Location"]["value"], rows=10000, cols=27)

	SurveyMaster = gc.open_by_key("1E3rIrerqHSpjH5Vq1PSHGljbxxETVG58-v1c7eHItNw")
	wsMaster = SurveyMaster.get_worksheet(0)

	# write to the worksheets, adding the headers if they don't exist
	wss = [wsDate, wsPark, wsMaster]
	for ws in wss:
		cols = ws.col_values(1)
		l = len(cols)

		if len(cols) < 1:
			ws.update('A1:W1', [headers])
			l = 1

		ws.update('A'+str(l+1)+':W'+str(l+1), [data])
	st.success("Successfully uploaded survey")


pics = st.file_uploader("Add picture", accept_multiple_files=True, type=["jpg", "png"])

st.button("Submit", on_click=submit)
