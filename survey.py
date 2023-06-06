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

global survey
survey = ss.StreamlitSurvey("Data Collection Form")
# survey.from_json("temp/clear.json")

defaults = {
	"Location": "",
	"Time": "",
	"Type of Activity": "",
	"activityOther": "",
	"Vehicle": "No",
	"Vehicle Description": "",
	"Company Name": "",
	"PUC": "",
	"License Plate": "",
	"Vehicle Notes": "",
	"Advertising": [],
	"advertisingOther": "",
	"Cash Exchange": "No",
	"Rec Stop": "No",
	"Customer Location": "",
	"Rec Stop Duration": "",
	"Intervention": "No",
	"Accepted Education Materials": "",
	"Behavior After Intervention": "",
	"behaviorOther": "",
	"Feeling of Safety": 0,
	"Intervention Result": "",
	"interventionResultOther": "",
	"Notes": "",
}

def clear_survey():
	global survey
	orig_survey = json.loads(survey.to_json())
	name = orig_survey["Ranger Name"]["value"]
	date = orig_survey["Date"]["value"]
	park = orig_survey["Park"]["value"]
	district = orig_survey["District"]["value"]
	survey["Ranger Name"]
	# for key in defaults:
	# 	orig_survey[key]["value"] = defaults[key]
	# path = "temp/clear.json"
	# with open(path,"w") as f: 
	# 	f.write(json.dumps(orig_survey))
	# survey.from_json(path)
	# print(survey.to_json())


st.header("Data Collection Form")

rangerName = ss.SelectBox(survey, "Ranger Name", options=["Angela", "Daniel", "Leina"], id="Ranger Name")
date = ss.DateInput(survey, "Date", id="Date")
park = ss.SelectBox(survey, "Park", options=["","Ala Moana","Aweoweo","Barbers Point","Bellows Field","Black Rocks","Diamond Head","Duke Paoa Kahanamoku","Ehu Kai","Hale'iwa Ali'i","Haleiwa","Hau'ula","Hūnānāniho (Waimānalo Bay)","Joe Lukela","Ka'a'awa","Kahe Point","Kaiaka Bay","Kailua","Kaiona","Kalaeloa","Kalae'o'io","Kalama","Kalaniana'ole","Kapi'olani","Kawaiku'i","Kea'au","Ke'ehi Lagoon","Kokololio","Kualoa","Kūhiō","Kuilei Cliffs","Kuli'ou'ou","La'ielohelohe","Le'ahi","Lualualei","Mā'ili","Mahaka","Makalei","Makapu'u","Makaua","Mauna Lahilahi","Maunalua Bay","Mokule'ia","One'ula","Poka'i Bay","Punalu'u","Pupukea","Pu'uloa","Sandy Beach (Wawamalu)","Sunset","Surfer's","Swanzy","Tracks","Ulehawa","Waiahole","Waiale'e","Wailupe","Waimānalo","Waimea Bay"], id="Park")
district = ss.Radio(survey, "District", options=["1", "2", "3", "4", "5"], id="District")
st.divider()
# st.button("Clear", on_click=clear_survey)
location = ss.TextArea(survey, "Location", id="Location")
time = ss.TextInput(survey, "Time", id="Time")
# ss.Radio("Park/Beach", options=["Park", "Beach"], id="Park/Beach")
commAct = ss.SelectBox(survey, "Observed Activity", options=["", "Camper van","Exercise class","Kayak","Paddleboard","Scuba","Snorkel","Surf","Swim","Yoga (land)","Yoga (water)","Film","Photography","Food truck","Food sale (small scale)","Luxury picnic","Misc. equipment rental", "Other"], id="Type of Activity")
activityOther = ss.TextInput(survey, "Other (please specify)", id="activityOther")
vehicle = ss.Radio(survey, "Vehicle Involved", options=["No", "Yes"], id="Vehicle")
vehicleDescription = ss.TextInput(survey, "Vehicle Description", id="Vehicle Description")
companyName = ss.TextInput(survey, "Company Name", id="Company Name")
puc = ss.TextInput(survey, "PUC", id="PUC")
licensePlate = ss.TextInput(survey, "License Plate #", id="License Plate")
vehicleNotes = ss.TextArea(survey, "Additional Notes", id="Vehicle Notes")
advert = ss.MultiSelect(survey, "Advertising on Park Property?", options=["Approaching visitors", "Handouts (flyers)", "Vehicle", "Staff clothing", "No", "Other"], id="Advertising")
advertisingOther = ss.TextInput(survey, "Other (please specify)", id="advertisingOther")
cashExchange = ss.Radio(survey, "Did you witness any cash exchange between the operator and consumer at any point during your observation?", options=["No", "Yes"], id="Cash Exchange")
recStop = ss.Radio(survey, "Recreational Stop? (Watch and time)", options=["No", "Yes"], id="Rec Stop")
customerLocation = ss.Radio(survey, "Where are the customers located? Are most of the visitors at the bathroom or are most of them out swimming/on the beach?", options=["Rec. Stop appropriate activity (using the bathroom)", "Non-Rec. Stop activity (stopped for purposes other than using the bathroom)"], id="Customer Location")
recStopDuration = ss.TextInput(survey, "Duration of the Rec. Stop in minutes", id="Rec Stop Duration")
intervention = ss.Radio(survey, "Intervention?", options=["No", "Yes"], id="Intervention")
acceptedEducationMaterial = ss.Radio(survey, "Accepted education materials?", options=["No", "Yes"], id="Accepted Education Materials")
inter = ss.MultiSelect(survey, "Behavior after intervention", options=["Ignored", "Feigning ignorance (making excuses)", "Hostility/Intimidation", "Moved locations (in park or right outside of park)", "Physical Violence", "Threat of physical violence", "Threatening verbiage (calling the mayor, etc.)", "Understanding", "Unaware of rules", "Verbal aggression (yelling, cussing, etc.)", "Other"], id="Behavior After Intervention")
behaviorOther = ss.TextInput(survey, "Other (please specify)", id="behaviorOther")
safety = ss.SelectSlider(survey, "Rank your feeling of safety based on the individual's response to your intervention", options=["Very Unsafe", "Moderately Unsafe", "Neutral", "Moderately Safe", "Very Safe"], id="Feeling of Safety")
result = ss.MultiSelect(survey, "Result of the intervention", options=["Called HPD and retreated", "Left without incident", "Perpetrator left the park", "Perpetrator moved locations (in or near park)", "Retreated from situation (no HPD)", "Other"], id="Intervention Result")
resultOther = ss.TextInput(survey, "Other (please specify)", id="interventionResultOther")
notes = ss.TextArea(survey, "Any other notes:", id="Notes")

rangerName.display()
date.display()
park.display()
district.display()
st.divider()
location.display()
time.display()
ca = commAct.display()
if "Other" in ca:
	activityOther.display()
vyes = vehicle.display() == "Yes"
if vyes:
	vehicleDescription.display()
	companyName.display()
	puc.display()
	licensePlate.display()
	vehicleNotes.display()
a = advert.display()
if "Other" in a:
	advertisingOther.display()
cashExchange.display()
recyes = recStop.display() == "Yes"
if recyes:
	customerLocation.display()
	recStopDuration.display()
interyes = intervention.display() == "Yes"
if interyes:
	acceptedEducationMaterial.display()
	inte = inter.display()
	if "Other" in inte:
		behaviorOther.display()
	safety.display()
	r = result.display()
	if "Other" in r:
		resultOther.display()
notes.display()

def submit():
	global survey
	# first parse the survey into the right format for writing
	headers = []
	data = []
	orig_survey = json.loads(survey.to_json())

	# add the data in others to the lists, instead of having it be a separate column
	if ca == "Other":
		orig_survey["Type of Activity"]["value"] = orig_survey["activityOther"]["value"]
	if "Other" in a:
		orig_survey["Advertising"]["value"].remove("Other")
		orig_survey["Advertising"]["value"].append(orig_survey["advertisingOther"]["value"])
	if interyes and "Other" in inte:
		orig_survey["Behavior After Intervention"]["value"].remove("Other")
		orig_survey["Behavior After Intervention"]["value"].append(orig_survey["behaviorOther"]["value"])
	if interyes and "Other" in r:
		orig_survey["Intervention Result"]["value"].remove("Other")
		orig_survey["Intervention Result"]["value"].append(orig_survey["interventionResultOther"]["value"])

	# clear conditional questions
	if not vyes:
		orig_survey["Vehicle Description"]["value"] = ""
		orig_survey["Company Name"]["value"] = ""
		orig_survey["PUC"]["value"] = ""
		orig_survey["License Plate"]["value"] = ""
		orig_survey["Vehicle Notes"]["value"] = ""
	if not recyes:
		orig_survey["Customer Location"]["value"] = ""
		orig_survey["Rec Stop Duration"]["value"] = ""
	if not interyes:
		orig_survey["Accepted Education Materials"]["value"] = ""
		orig_survey["Behavior After Intervention"]["value"] = ""
		orig_survey["Feeling of Safety"]["value"] = ""
		orig_survey["Intervention Result"]["value"] = ""


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

	# convert json to csv
	for key in orig_survey:
		if "Other" in key:
			continue
		headers.append(key)
		datum = orig_survey[key]["value"]
		if key == "Pictures":
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
		wsPark = SurveyByPark.worksheet(orig_survey["Park"]["value"])
	except:
		wsPark = SurveyByPark.add_worksheet(title=orig_survey["Park"]["value"], rows=10000, cols=27)

	SurveyMaster = gc.open_by_key("1E3rIrerqHSpjH5Vq1PSHGljbxxETVG58-v1c7eHItNw")
	wsMaster = SurveyMaster.get_worksheet(0)

	# write to the worksheets, adding the headers if they don't exist
	wss = [wsDate, wsPark, wsMaster]
	for ws in wss:
		cols = ws.col_values(1)
		l = len(cols)

		if len(cols) < 1:
			ws.update('A1:AA1', [headers])
			l = 1

		ws.update('A'+str(l+1)+':AA'+str(l+1), [data])
	st.success("Successfully uploaded survey")

	# clear_survey()


pics = st.file_uploader("Add picture", accept_multiple_files=True, type=["jpg", "png"])

st.button("Submit", on_click=submit)
