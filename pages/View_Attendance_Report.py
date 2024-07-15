from datetime import datetime
import streamlit as st

from modules.nav import menu_nav
menu_nav()

import pandas as pd

st.header('Student_Attendance_Report')

try:
    from Home import face_recog
    
except ImportError:
    st.error("Connection Error")

# Retrieve logs data
name = 'attendance:logs'

def load_logs(name, end=-1):
    try:
        if face_recog:
            logs_list = face_recog.r.lrange(name, start=0, end=end) 
            return logs_list
    except:
        st.error("Check your network connection.")
        return []

logs_list = load_logs(name=name)

if logs_list:
    # Tabs to show different information
    tab1, tab2 = st.tabs(['Registered Students','Attendence-Report'])

    with tab1:
        if st.button('Refresh Data'):
            # Retrive the data from Redis Db
            with st.spinner('Retriving data from Redis db...'):
                redis_face_db = face_recog.retrive_data(name='academy:register')
                # st.dataframe(redis_face_db[['Name', 'Role']])

                # Filter the DataFrame to only include rows where the role is 'Student'
                student_data = redis_face_db[redis_face_db['Role'] == 'Student']

                # Display the filtered DataFrame
                st.dataframe(student_data[['Name', 'Role']])

    with tab2: 
        # load logs
        logs_list = load_logs(name=name)

    # Function to calculate status
        def status_marker(duration_hrs):
            if pd.isnull(duration_hrs):
                return 'Absent'
            elif duration_hrs == 0:
                return 'Absent'
            elif duration_hrs < 4:
                return 'Half Day'
            else:
                return 'Present'

        report_type = st.sidebar.selectbox("Select Report Type", ["Daily", "Weekly", "Monthly"])

    # Main app
        with st.container():
            # step 1: convert byte to list
            cbtl = lambda x: x.decode('utf-8')
            logs_list = list(map(cbtl, logs_list))

            # step 2: split by @
            split_str = lambda x: x.split('@')
            logs_nested_list = list(map(split_str, logs_list))

            # step 3: convert to dataframe
            logs_df = pd.DataFrame(logs_nested_list, columns = ['Name', 'Role', 'Timestamp'])

            # Filter only student data
            logs_df = logs_df[logs_df['Role'] == 'Student']

            # Convert timestamp to datetime
            logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])

            
            """   Absent data nhih show horeaaa """


            # Generate report based on selected report type
            if report_type == "Daily":
                # Extract date
                logs_df['Date'] = logs_df['Timestamp'].dt.strftime('%d-%m-%Y')

                # Group by date, name, and role to calculate in and out times
                report_df = logs_df.groupby(['Date', 'Name', 'Role']).agg(
                    In_time=('Timestamp', 'min'),  # First time detected in a day
                    Out_time=('Timestamp', 'max')  # Last time detected in a day
                ).reset_index()

                report_df['Duration'] = report_df['Out_time'] - report_df['In_time']
                report_df['Duration_hrs'] = report_df['Duration'].dt.total_seconds() / 3600
                report_df['Status'] = report_df['Duration_hrs'].apply(status_marker)

                report_df = report_df[['Date', 'Name', 'Status', 'In_time', 'Out_time', 'Duration', 'Duration_hrs']]
                st.dataframe(report_df)

                # Add date input widget for searching
                selected_date = st.date_input("Select a date", value=datetime.today().date())
                selected_date_str = selected_date.strftime('%d-%m-%Y')
                filtered_report_df = report_df[report_df['Date'] == selected_date_str]

                st.dataframe(filtered_report_df)

            elif report_type == "Weekly":
                # Extract week number, year, and month
                logs_df['Week'] = logs_df['Timestamp'].dt.isocalendar().week
                logs_df['Year'] = logs_df['Timestamp'].dt.isocalendar().year.astype(str)
                # logs_df['Month'] = logs_df['Timestamp'].dt.strftime('%B')

                # Group by week, name, role, and month to calculate in and out times
                report_df = logs_df.groupby(['Week', 'Year', 'Name', 'Role']).agg(
                    In_time=('Timestamp', 'min'),  # First time detected in a week
                    Out_time=('Timestamp', 'max')  # Last time detected in a week
                ).reset_index()

                report_df['Duration'] = report_df['Out_time'] - report_df['In_time']
                report_df['Days'] = report_df['Duration'].dt.days + 1

                # # Select only necessary columns
                report_df = report_df[['Week', 'Year', 'Name', 'Days']]
                # Show report
                st.dataframe(report_df)

                # Add widgets for selecting week number and year
                weeks = report_df['Week'].unique()
                years = report_df['Year'].unique()

                selected_week = st.selectbox("Select a week number", weeks)
                selected_year = st.selectbox("Select a year", years)

                filtered_report_df = report_df[(report_df['Week'] == selected_week) & (report_df['Year'] == selected_year)]
                
                mod_report_df = (filtered_report_df[['Name', 'Days']])
                st.dataframe(mod_report_df)

            elif report_type == "Monthly":
                # Extract month and year
                logs_df['Month'] = logs_df['Timestamp'].dt.strftime('%B')
                logs_df['Year'] = logs_df['Timestamp'].dt.year.astype(str)

                # Group by month, name, and role to calculate in and out times
                report_df = logs_df.groupby(['Month', 'Year', 'Name']).agg(
                    In_time=('Timestamp', 'min'),  # First time detected in a month
                    Out_time=('Timestamp', 'max')  # Last time detected in a month
                ).reset_index()

                report_df['Duration'] = report_df['Out_time'] - report_df['In_time']
                report_df['Days'] = report_df['Duration'].dt.days + 1

                report_df = report_df[['Month', 'Year', 'Name', 'Days']]
                st.dataframe(report_df) 

                months = report_df['Month'].unique()
                years = report_df['Year'].unique()

                selected_month = st.selectbox("Select a month", months)
                selected_year = st.selectbox("Select a year", years)

                filtered_report_df = report_df[(report_df['Month'] == selected_month) & (report_df['Year'] == selected_year)]
                
                mod_report_df = filtered_report_df[['Name', 'Days']]
                st.dataframe(mod_report_df)


    """end"""