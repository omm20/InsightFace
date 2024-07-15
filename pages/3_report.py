import streamlit as st
import pandas as pd
from home import face_recog

# st.set_page_config(page_title="Report")
st.subheader('Report')

# Retrive logs data
name = 'attendance:logs'
def load_logs(name, end=-1):
    # extract data from db
    logs_list = face_recog.r.lrange(name, start=0, end=end) 
    return logs_list

# tabs to show info
tab1, tab2, tab3 = st.tabs(['Registered Data', 'Logs', 'Attendence-Report'])

with tab1:
    if st.button('Refresh Data'):
        # Retrive the data from Redis Db
        with st.spinner('Retriving data from Redis db...'):
            redis_face_db = face_recog.retrive_data(name='academy:register')
            st.dataframe(redis_face_db[['Name', 'Role']])

with tab2: 
    if st.button('Refresh Logs'):
        st.write(load_logs(name=name))


with tab3:
    st.subheader('Attendance Report')

    # load logs
    logs_list = load_logs(name=name)

    # step 1: convert byte to list
    cbtl = lambda x: x.decode('utf-8')
    logs_list = list(map(cbtl, logs_list))

    # step 2: split by @
    split_str = lambda x: x.split('@')
    logs_nested_list = list(map(split_str, logs_list))

    # step 3: convert to dataframe
    logs_df = pd.DataFrame(logs_nested_list, columns = ['Name', 'Role', 'Timestamp'])
    # st.write(logs_df)  

    # 3:Time based analysis or Report
    logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])
    logs_df['Date'] = logs_df['Timestamp'].dt.date

    # 3.1: Calculate in and out time
    report_df = logs_df.groupby(by=['Date','Name','Role']).agg(
        In_time = pd.NamedAgg('Timestamp','min'), # person first tym detected in a day
        Out_time = pd.NamedAgg('Timestamp','max') # person last tym detected in a day
    ).reset_index()

    report_df['In_time'] = pd.to_datetime(report_df['In_time'])
    report_df['Out_time'] = pd.to_datetime(report_df['Out_time'])

    report_df['Duration'] = report_df['Out_time'] - report_df['In_time']
    # st.dataframe(report_df)

    # 4: Mark present or absent
    all_dates = report_df['Date'].unique()
    name_role = report_df[['Name','Role']].drop_duplicates().values.tolist()

    date_name_role_zip = []
    for dt in all_dates:
        for name, role in name_role:
            date_name_role_zip.append([dt,name,role])

    date_name_role_zip_df = pd.DataFrame(date_name_role_zip, columns=['Date','Name','Role'])
    
    # left join with report_df
    date_name_role_zip_df = pd.merge(date_name_role_zip_df, report_df, how='left', on=['Date','Name','Role'])

    # Duration
    # Hours
    date_name_role_zip_df['Duration_secs'] = date_name_role_zip_df['Duration'].dt.seconds
    date_name_role_zip_df['Duration_hrs'] = date_name_role_zip_df['Duration_secs'] / (60*60)

    def status_marker(x):
        if pd.Series(x).isnull().all():
            return 'Absent'
        
        elif x>=0 and x<1:
            return 'Absent (Less than 1 hr)'
        
        elif x>=1 and x<4:
            return 'Half Day (Less than 4 hrs)'
        
        elif x>=4 and x<6:
            return 'Half Day'
        
        elif x>=6:
            return 'Present'
        
    date_name_role_zip_df['Status'] = date_name_role_zip_df['Duration_hrs'].apply(status_marker)

    st.dataframe(date_name_role_zip_df)

