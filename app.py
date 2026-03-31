import streamlit as st
import pandas as pd
from datetime import date
import os

# পেজ সেটআপ
st.set_page_config(page_title="অগ্রধারা সমিতি - মাস্টার এডিশন", layout="wide")

# ফাইল পাথ
DB_FILE = "samity_master_db.csv"

# সব প্রয়োজনীয় কলামের লিস্ট (যাতে KeyError না আসে)
cols = ["আইডি", "নাম", "মোবাইল", "ধরণ", "মূল ঋণ", "সার্ভিস চার্জ", "সঞ্চয়", "কিস্তি", "কল্যাণ তহবিল", "বই ফি", "ভর্তি ফি", "সময়কাল", "ভর্তির তারিখ", "কিস্তির তারিখ", "তারিখ"]

# ডেটা লোড করার নিরাপদ ফাংশন
def load_data():
    if os.path.exists(DB_FILE):
        try:
            temp_df = pd.read_csv(DB_FILE)
            # যদি কলাম মিসিং থাকে তবে অটো অ্যাড হবে
            for col in cols:
                if col not in temp_df.columns:
                    temp_df[col] = 0 if col in ["মূল ঋণ", "সার্ভিস চার্জ", "সঞ্চয়", "কিস্তি", "কল্যাণ তহবিল"] else ""
            return temp_df[cols]
        except:
            return pd.DataFrame(columns=cols)
    else:
        return pd.DataFrame(columns=cols)

# তারিখ চেক করার ফাংশন (যাতে NaT এরর না আসে)
def safe_date(date_val):
    try:
        if pd.isna(date_val) or date_val == "" or date_val == "nan":
            return date.today()
        return pd.to_datetime(date_val).date()
    except:
        return date.today()

df = load_data()

st.title("🏦 অগ্রধারা ক্ষুদ্র ব্যবসায়ী সমবায় সমিতি")

menu = ["অ্যাডমিন প্যানেল", "সদস্য ভিউ প্যানেল"]
choice = st.sidebar.selectbox("মেনু নির্বাচন", menu)

# --- ১. অ্যাডমিন প্যানেল ---
if choice == "অ্যাডমিন প্যানেল":
    admin_id = st.sidebar.text_input("অ্যাডমিন আইডি", value="admin")
    admin_pw = st.sidebar.text_input("পাসওয়ার্ড", type="password")
    
    if admin_id == "admin" and admin_pw == "1234":
        st.success("অ্যাডমিন লগইন সফল")
        t1, t2, t3, t4 = st.tabs(["📋 দৈনিক কালেকশন", "💰 নতুন ঋণ প্রদান", "📊 আজকের রিপোর্ট", "⚙️ এডিট অপশন"])
        
        with t1: # দৈনিক কালেকশন
            with st.form("daily_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                d_id = c1.text_input("সদস্য আইডি*")
                d_name = c2.text_input("সদস্যের নাম*")
                col_s, col_k = st.columns(2)
                d_sanchay = col_s.number_input("সঞ্চয় জমা", min_value=0)
                d_kisti = col_k.number_input("ঋণের কিস্তি", min_value=0)
                if st.form_submit_button("কালেকশন সেভ করুন"):
                    if d_id and d_name:
                        new_data = [d_id, d_name, "", "কালেকশন", 0, 0, d_sanchay, d_kisti, 0, 0, 0, "", "", "", date.today()]
                        df = pd.concat([df, pd.DataFrame([new_data], columns=cols)], ignore_index=True)
                        df.to_csv(DB_FILE, index=False)
                        st.success(f"সফলভাবে {d_name}-এর কালেকশন জমা হয়েছে।")

        with t2: # নতুন ঋণ প্রদান (ভর্তির তারিখ ও কিস্তির তারিখ সহ)
            st.subheader("নতুন ঋণ এন্ট্রি ফরম")
            with st.form("loan_form", clear_on_submit=True):
                l_c1, l_c2 = st.columns(2)
                l_id = l_c1.text_input("সদস্য আইডি*")
                l_name = l_c1.text_input("নাম*")
                l_mob = l_c2.text_input("মোবাইল নাম্বার*")
                
                l_col1, l_col2, l_col3 = st.columns(3)
                l_amt = l_col1.number_input("ঋণের মূল টাকা", min_value=0)
                l_charge = l_col2.number_input("সার্ভিস চার্জ", min_value=0)
                l_kalyan = l_col3.number_input("কল্যাণ তহবিল", min_value=0)
                
                l_date1, l_date2 = st.columns(2)
                l_join_date = l_date1.date_input("ভর্তির তারিখ", date.today())
                l_kisti_date = l_date2.date_input("কিস্তি নেওয়ার তারিখ", date.today())
                
                if st.form_submit_button("ঋণ এন্ট্রি সেভ করুন"):
                    if l_id and l_name:
                        new_loan = [l_id, l_name, l_mob, "নতুন ঋণ", l_amt, l_charge, 0, 0, l_kalyan, 0, 0, "", l_join_date, l_kisti_date, date.today()]
                        df = pd.concat([df, pd.DataFrame([new_loan], columns=cols)], ignore_index=True)
                        df.to_csv(DB_FILE, index=False)
                        st.success("নতুন ঋণ সফলভাবে সেভ হয়েছে।")

        with t3: # আজকের রিপোর্ট (সুন্দর ও পেশাদার)
            today_str = str(date.today())
            today_df = df[df['তারিখ'].astype(str) == today_str]
            st.markdown(f"### 📊 আজকের রিপোর্ট - {today_str}")
            
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("💰 মোট সঞ্চয়", f"{int(today_df['সঞ্চয়'].sum())} ৳")
            r2.metric("📉 মোট কিস্তি", f"{int(today_df['কিস্তি'].sum())} ৳")
            r3.metric("💳 মোট ঋণ বিতরণ", f"{int(today_df['মূল ঋণ'].sum())} ৳")
            r4.metric("🏦 সার্ভিস চার্জ", f"{int(today_df['সার্ভিস চার্জ'].sum())} ৳")
            
            st.divider()
            st.dataframe(today_df, use_container_width=True)

        with t4: # এডিট অপশন (সব ঘর সহ)
            st.subheader("⚙️ সদস্য তথ্য সংশোধন (এডিট)")
            search_id = st.text_input("আইডি লিখে সার্চ দিন")
            if search_id:
                match = df[df['আইডি'].astype(str) == search_id]
                if not match.empty:
                    idx = match.index[-1]
                    with st.form("edit_master_form"):
                        e_c1, e_c2 = st.columns(2)
                        en_name = e_c1.text_input("নাম", value=str(df.at[idx, 'নাম']))
                        en_mob = e_c2.text_input("মোবাইল", value=str(df.at[idx, 'মোবাইল']))
                        
                        ec1, ec2, ec3 = st.columns(3)
                        en_amt = ec1.number_input("মূল ঋণ", value=int(df.at[idx, 'মূল ঋণ']))
                        en_charge = ec2.number_input("সার্ভিস চার্জ", value=int(df.at[idx, 'সার্ভিস চার্জ']))
                        en_kalyan = ec3.number_input("কল্যাণ তহবিল", value=int(df.at[idx, 'কল্যাণ তহবিল']))
                        
                        ed1, ed2 = st.columns(2)
                        en_join = ed1.date_input("ভর্তির তারিখ", value=safe_date(df.at[idx, 'ভর্তির তারিখ']))
                        en_kisti = ed2.date_input("কিস্তির তারিখ", value=safe_date(df.at[idx, 'কিস্তির তারিখ']))
                        
                        if st.form_submit_button("এডিট আপডেট করুন"):
                            df.at[idx, 'নাম'] = en_name
                            df.at[idx, 'মোবাইল'] = en_mob
                            df.at[idx, 'মূল ঋণ'] = en_amt
                            df.at[idx, 'সার্ভিস চার্জ'] = en_charge
                            df.at[idx, 'কল্যাণ তহবিল'] = en_kalyan
                            df.at[idx, 'ভর্তির তারিখ'] = str(en_join)
                            df.at[idx, 'কিস্তির তারিখ'] = str(en_kisti)
                            df.to_csv(DB_FILE, index=False)
                            st.success("✅ এডিট সেভ হয়েছে")
                else:
                    st.warning("এই আইডিতে কোনো তথ্য পাওয়া যায়নি।")

# --- ২. সদস্য ভিউ প্যানেল ---
elif choice == "সদস্য ভিউ প্যানেল":
    st.subheader("🔍 সদস্যের বিস্তারিত তথ্য")
    search_q = st.text_input("আইডি বা মোবাইল নাম্বার দিয়ে সার্চ করুন")
    if search_q:
        res = df[(df['আইডি'].astype(str) == search_q) | (df['মোবাইল'].astype(str) == search_q)]
        if not res.empty:
            st.info(f"সদস্যের নাম: {res.iloc[0]['নাম']}")
            
            # অবশিষ্ট ঋণ ক্যালকুলেশন
            t_loan = res['মূল ঋণ'].sum()
            t_charge = res['সার্ভিস চার্জ'].sum()
            t_paid = res['কিস্তি'].sum()
            rem = (t_loan + t_charge) - t_paid
            
            v1, v2, v3 = st.columns(3)
            v1.metric("মোট সঞ্চয় জমা", f"{res['সঞ্চয়'].sum()} ৳")
            v2.metric("মোট কিস্তি জমা", f"{t_paid} ৳")
            v3.metric("অবশিষ্ট ঋণের টাকা", f"{rem} ৳")
            
            st.divider()
            st.write("📜 লেনদেনের ইতিহাস:")
            st.dataframe(res[["তারিখ", "ধরণ", "সঞ্চয়", "কিস্তি", "ভর্তির তারিখ", "কিস্তির তারিখ"]], use_container_width=True)
        else:
            st.error("দুঃখিত, কোনো তথ্য পাওয়া যায়নি।")