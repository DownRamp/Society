import streamlit as st
import pysondb
import os
import json


# report bad/weird things around you
def report(title, status, description, date, country, city, intersection, location):
    # check if path exists for each part
    check_directory(country, city)
    path = f"data/{country}/{city}/{intersection}.json"
    report_db = pysondb.getDb(path)
    report_db.add({"title": title, "status": status, "description": description, "date": date, "location": location})


def check_directory(country, city):
    path_sub1 = f"data/{country}"
    path_sub2 = f"data/{country}/{city}"

    is_exist1 = os.path.exists(path_sub1)
    if is_exist1:
        is_exist2 = os.path.exists(path_sub2)
        if not is_exist2:
            create_folder(path_sub2)
    else:
        create_folder(path_sub2)


# if directory doesn't already exist for search
# data/location
def create_folder(path):
    os.makedirs(path)


def app():
    with st.form("my_form"):
        st.title('Create a report')
        title = st.text_input("Title")
        status = st.selectbox("Status", ('Good', 'Bad'))
        description = st.text_area("Description")
        date = st.date_input("Date")
        country = st.text_input("Country")
        city = st.text_input("City")
        intersection = st.text_input("Intersection")
        location = st.text_input("Location")
        submitted = st.form_submit_button("Submit")

        if submitted:
            intersection = intersection.replace(" ", "")
            formatted_datetime = date.isoformat()

            json_datetime = json.dumps(formatted_datetime)
            json_datetime = json_datetime.replace("-", "")

            report(title.lower(), status.lower(), description.lower(), json_datetime,
                   country.lower(), city.lower(), intersection.lower(),
                   location.lower())
            st.success("Added To Data")
