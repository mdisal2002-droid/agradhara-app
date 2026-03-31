import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# পেজ সেটআপ
st.set_page_config(page_title="অগ্রধারা সমিতি - অনলাইন ডাটাবেস", layout="wide")

st.title("🏦 অগ্রধারা ক্ষুদ্র ব্যবসায়ী সমবায় সমিতি")

# Google Sheets কানেকশন তৈরি
conn = st.connection("gsheets", type=GSheetsConnection)

# ডাটা পড়ার ফাংশন
def load_data():
    return conn.read(worksheet="Sheet1", usecols=list(range(15)))

df = load_data()

# আপনার বাকি হিসাব নিকাশ এবং ইনপুট ফর্ম এখানে থাকবে...
st.write("আপনার বর্তমান সদস্যদের তালিকা:")
st.dataframe(df)

# ডাটা সেভ করার বাটন
if st.button("গুগল শিটে সেভ করুন"):
    # এখানে আপনার আপডেট করা ডাটা পাঠানোর কোড থাকবে
    st.success("সফলভাবে গুগল শিটে জমা হয়েছে!")
