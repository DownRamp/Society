import streamlit as st
import geocoder
from streamlit_autorefresh import st_autorefresh
import pysondb
import os
import pytz

st_autorefresh(interval=5 * 60 * 1000, key="framerefresh")

data_show = []
g = geocoder.ip('me')
user_city = g.json["city"].lower()
user_country = pytz.country_names[g.json["country"]].lower()


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def fetch_files(dirName):
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        list_of_files += [os.path.join(dirpath, file) for file in filenames if file.endswith('.json')]
    return list_of_files


# fill search data
def retrieve_all_reports():
    # walk through subdirectories and fetch all files
    files = fetch_files("/data")
    # open files and put into data_show
    for file in files:
        data_show.extend(pysondb.getDb(file).getAll())


def retrieve_reports():
    # fetch all places
    path = f"data/{user_country.lower()}/{user_city.lower()}"
    if os.path.exists(path):
        files = fetch_files(path)
        reports = []
        for file in files:
            reports.extend(pysondb.getDb(file).getAll())
        return reports
    return []


def split_reports(reports):
    good, bad = [], []
    for report in reports:
        if report["status"] == "good":
            good.append(report)
        else:
            bad.append(report)
    return good, bad


def search(stat_type, value):
    filter_data = []
    for data in data_show:
        if value in data[stat_type]:
            filter_data.append(data)
    return filter_data


def app():
    local_css("assets/style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    st.title('Show Report')
    col1, col2 = st.columns((3, 1))
    query = col1.text_input("", "Ex. location:123 blah street")
    ok = col2.button("OK")
    st.text("Tags:[title, description, date, location]")
    retrieve_all_reports()
    if not ok:
        good, bad = split_reports(retrieve_reports())
        st.write("Good news: ")
        st.write(good)
        st.write("Bad news: ")
        st.write(bad)
    else:
        st.success("Results found")
        stat_type, value = query.split(":")
        good, bad = split_reports(search(stat_type.strip(), value.strip()))
        st.write("Good news: ")
        st.write(good)
        st.write("Bad news: ")
        st.write(bad)
