import pandas as pd
import streamlit as st
import sqlite3
from PIL import Image

DATA_BASE_NAME = "sample-database.db"


def get_connection():
    return sqlite3.connect(DATA_BASE_NAME)


st.set_page_config(
    layout="wide",
    page_title="Data Dashboard",
    page_icon=":bar_chart:"
)


st.title("Student Info. DATA PREVIEW")
st.markdown("_Beta v1.3_")


conn = get_connection()


def load_data(path: str):
    data = pd.read_sql("SELECT * FROM students", conn)
    return data


# Sidebar
with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

# Stop execution until file is uploaded
if uploaded_file is None:
    st.info(" Upload a file through config")
    st.stop()

df = load_data(uploaded_file)


with st.expander("📄 Data Preview"):

    st.subheader("Student Data")

    # Column headers
    header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([2, 2, 2, 2, 3])
    header_col1.markdown("**First Name**")
    header_col2.markdown("**Middle Initial**")
    header_col3.markdown("**Last Name**")
    header_col4.markdown("**ID**")
    header_col5.markdown("**QR Code**")

    for index, row in df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 3])

        with col1:
            st.write(row["First_Name"])
        with col2:
            st.write(row["Middle_Initial"])
        with col3:
            st.write(row["Last_Name"])
        with col4:
            st.write(row["ID"])

        with col5:
            img = Image.open(row["QR_Path"])
            img_large = img.resize((250, 250))
            st.image(row["QR_Path"], width=60)

if st.button("Refresh Data"):
    st.cache_data.clear()

df = load_data(uploaded_file)
