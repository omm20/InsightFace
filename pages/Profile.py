# import streamlit as st
# import pandas as pd
# import altair as alt
# from datetime import datetime
# from streamlit import session_state as ss
# # from modules.nav import logout_btns, attendanceReportNav, teacherAttRepNav

# st.header('Welcome to Your Profile Page!')

# from modules.nav import menu_nav
# menu_nav()

# # if ss.name:
# #     # st.write(ss.name)

# user_name = ss.get('name', 'No name Found')
# st.header(f"{user_name}")

# try:
#     from Home import face_recog
    
# except ImportError:
#     st.error("Connection Error")


# # Retrive logs data
# name = 'attendance:logs'
# def load_logs(name, end=-1):
#     logs_list = face_recog.r.lrange(name, start=0, end=end) 
#     return logs_list

# logs_list = load_logs(name=name)

# # Calculate status
# def status_marker(duration_hrs):
#     if pd.isnull(duration_hrs):
#         return 'Absent'
#     elif duration_hrs == 0:
#         return 'Absent'
#     elif duration_hrs < 4:
#         return 'Half Day'
#     else:
#         return 'Present'

# # Convert logs data to DataFrame
# cbtl = lambda x: x.decode('utf-8')
# logs_list = list(map(cbtl, logs_list))

# split_str = lambda x: x.split('@')
# logs_nested_list = list(map(split_str, logs_list))

# logs_df = pd.DataFrame(logs_nested_list, columns=['Name', 'Role', 'Timestamp'])

# # Filter only student data
# logs_df = logs_df[logs_df['Role'] == user_role]

# # Convert timestamp to datetime
# logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])

# # Filter logs for the specific student
# student_logs_df = logs_df[logs_df['Name'] == user_name]

# # Daily Attendance Calculation
# student_logs_df['Date'] = student_logs_df['Timestamp'].dt.strftime('%d-%m-%Y')
# daily_report_df = student_logs_df.groupby(['Date', 'Name', 'Role']).agg(
#     In_time=('Timestamp', 'min'),
#     Out_time=('Timestamp', 'max')
# ).reset_index()
# daily_report_df['Duration'] = daily_report_df['Out_time'] - daily_report_df['In_time']
# daily_report_df['Duration_hrs'] = daily_report_df['Duration'].dt.total_seconds() / 3600
# daily_report_df['Status'] = daily_report_df['Duration_hrs'].apply(status_marker)

# # Yearly Attendance Percentage Calculation
# total_days = len(daily_report_df['Date'].unique())
# present_days = len(daily_report_df[daily_report_df['Status'] == 'Present'])
# yearly_attendance_percentage = (present_days / total_days) * 100
# absent_days = total_days - present_days
# absent_percentage = (absent_days / total_days) * 100

# # Weekly Attendance Calculation
# student_logs_df['Week'] = student_logs_df['Timestamp'].dt.isocalendar().week
# weekly_report_df = student_logs_df.groupby(['Week', 'Name', 'Role']).agg(
#     In_time=('Timestamp', 'min'),
#     Out_time=('Timestamp', 'max')
# ).reset_index()
# weekly_report_df['Duration'] = weekly_report_df['Out_time'] - weekly_report_df['In_time']
# weekly_report_df['Days'] = weekly_report_df['Duration'].dt.days + 1

# # Monthly Attendance Calculation
# # Create a DataFrame for all months of the year
# all_months_df = pd.DataFrame({'Month': pd.date_range(start='2023-01-01', end='2023-12-31', freq='MS').strftime('%B')})
# all_months_df['Month'] = pd.Categorical(all_months_df['Month'], categories=all_months_df['Month'], ordered=True)

# student_logs_df['Month'] = student_logs_df['Timestamp'].dt.strftime('%B')
# monthly_report_df = student_logs_df.groupby(['Month', 'Name', 'Role']).agg(
#     In_time=('Timestamp', 'min'),
#     Out_time=('Timestamp', 'max')
# ).reset_index()
# monthly_report_df['Duration'] = monthly_report_df['Out_time'] - monthly_report_df['In_time']
# monthly_report_df['Days'] = monthly_report_df['Duration'].dt.days + 1

# # Merge with all months DataFrame to ensure all months are represented
# monthly_report_df = all_months_df.merge(monthly_report_df, on='Month', how='left').fillna({'Days': 0})

# # Function to create pie chart
# def create_pie_chart(present_days, total_days, title):
#     absent_days = total_days - present_days
#     present_percentage = (present_days / total_days) * 100
#     absent_percentage = (absent_days / total_days) * 100
    
#     attendance_data = pd.DataFrame({
#         'Status': ['Present', 'Absent'],
#         'Percentage': [present_percentage, absent_percentage]
#     })
    
#     pie_chart = alt.Chart(attendance_data).mark_arc().encode(
#         theta=alt.Theta(field="Percentage", type="quantitative"),
#         color=alt.Color(field="Status", type="nominal"),
#         tooltip=['Status', 'Percentage']
#     ).properties(title=title)
    
#     return pie_chart

# tab1, tab2, tab3 = st.tabs(["Yearly", "Monthly", "Weekly"])

# with tab1:
#     st.metric("Yearly Attendance Percentage", f"{yearly_attendance_percentage:.2f}%")
#     yearly_pie_chart = create_pie_chart(present_days, total_days, "Yearly Attendance Status Distribution")
#     st.altair_chart(yearly_pie_chart, use_container_width=True)

# with tab2:
#     monthly_chart = alt.Chart(monthly_report_df.sort_values(by='Month', key=lambda x: all_months_df['Month'].cat.codes)).mark_bar().encode(
#         x=alt.X('Month', sort=all_months_df['Month']),
#         y='Days',
#         tooltip=['Month', 'Days']
#     ).properties(title="Monthly Attendance")
#     st.altair_chart(monthly_chart, use_container_width=True)

# with tab3:
#     weekly_chart = alt.Chart(weekly_report_df).mark_bar().encode(
#         x='Week:O',
#         y='Days',
#         tooltip=['Week', 'Days']
#     ).properties(title="Weekly Attendance")
#     st.altair_chart(weekly_chart, use_container_width=True)









import streamlit as st
import pandas as pd
import altair as alt
from streamlit import session_state as ss
from datetime import datetime



st.header('Welcome to Your Profile Page!')
# authenticator.logout(location='main')

from modules.nav import menu_nav
menu_nav()

# from pages.Login import authenticator
# authenticator.logout(location='main')


user_name = ss.get('name', 'Unavailable')
# st.header(f"{user_name}")

if ss.role:
    user_role = ss.role
    st.write(user_role)

if user_name != 'Unavailable':
    # st.write(if(user_name))
    try:
        from Home import face_recog
    except ImportError:
        st.error("Connection Error")
        face_recog = None

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
    # st.write(logs_list)

    if logs_list:
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

    # Convert logs data to DataFrame
        cbtl = lambda x: x.decode('utf-8')
        logs_list = list(map(cbtl, logs_list))

        split_str = lambda x: x.split('@')
        logs_nested_list = list(map(split_str, logs_list))

        logs_df = pd.DataFrame(logs_nested_list, columns=['Name', 'Role', 'Timestamp'])

        # Filter only student data
        logs_df = logs_df[logs_df['Role'] == user_role]

        # Convert timestamp to datetime
        logs_df['Timestamp'] = pd.to_datetime(logs_df['Timestamp'])

        # Filter logs for the specific student
        student_logs_df = logs_df[logs_df['Name'] == user_name]

        # st.write(student_logs_df)

        if not student_logs_df.empty:

            # Daily Attendance Calculation
            student_logs_df['Date'] = student_logs_df['Timestamp'].dt.strftime('%d-%m-%Y')
            daily_report_df = student_logs_df.groupby(['Date', 'Name', 'Role']).agg(
                In_time=('Timestamp', 'min'),
                Out_time=('Timestamp', 'max')
            ).reset_index()
            daily_report_df['Duration'] = daily_report_df['Out_time'] - daily_report_df['In_time']
            daily_report_df['Duration_hrs'] = daily_report_df['Duration'].dt.total_seconds() / 3600
            daily_report_df['Status'] = daily_report_df['Duration_hrs'].apply(status_marker)

            # Yearly Attendance Percentage Calculation
            total_days = len(daily_report_df['Date'].unique())
            present_days = len(daily_report_df[daily_report_df['Status'] == 'Present'])
            yearly_attendance_percentage = (present_days / total_days) * 100
            absent_days = total_days - present_days
            absent_percentage = (absent_days / total_days) * 100

            # Weekly Attendance Calculation
            student_logs_df['Week'] = student_logs_df['Timestamp'].dt.isocalendar().week
            weekly_report_df = student_logs_df.groupby(['Week', 'Name', 'Role']).agg(
                In_time=('Timestamp', 'min'),
                Out_time=('Timestamp', 'max')
            ).reset_index()
            weekly_report_df['Duration'] = weekly_report_df['Out_time'] - weekly_report_df['In_time']
            weekly_report_df['Days'] = weekly_report_df['Duration'].dt.days + 1

            # Monthly Attendance Calculation
            # Create a DataFrame for all months of the year
            all_months_df = pd.DataFrame({'Month': pd.date_range(start='2023-01-01', end='2023-12-31', freq='MS').strftime('%B')})
            all_months_df['Month'] = pd.Categorical(all_months_df['Month'], categories=all_months_df['Month'], ordered=True)

            student_logs_df['Month'] = student_logs_df['Timestamp'].dt.strftime('%B')

            # student_logs_df['Month'] = student_logs_df['Timestamp'].dt.strftime('%B')
            monthly_report_df = student_logs_df.groupby(['Month', 'Name', 'Role']).agg(
                In_time=('Timestamp', 'min'),
                Out_time=('Timestamp', 'max')
            ).reset_index()
            monthly_report_df['Duration'] = monthly_report_df['Out_time'] - monthly_report_df['In_time']
            monthly_report_df['Days'] = monthly_report_df['Duration'].dt.days + 1

            # Merge with all months DataFrame to ensure all months are represented
            monthly_report_df = all_months_df.merge(monthly_report_df, on='Month', how='left').fillna({'Days': 0})

            # Function to create pie chart
            def create_pie_chart(present_days, total_days, title):
                absent_days = total_days - present_days
                present_percentage = (present_days / total_days) * 100
                absent_percentage = (absent_days / total_days) * 100
                
                attendance_data = pd.DataFrame({
                    'Status': ['Present', 'Absent'],
                    'Percentage': [present_percentage, absent_percentage]
                })
                
                pie_chart = alt.Chart(attendance_data).mark_arc().encode(
                    theta=alt.Theta(field="Percentage", type="quantitative"),
                    color=alt.Color(field="Status", type="nominal"),
                    tooltip=['Status', 'Percentage']
                ).properties(title=title)
                
                return pie_chart
            
            
            # st.subheader(f"Daily Attendance for {current_month}")
            # daily_chart_current_month = alt.Chart(current_month_df).mark_bar().encode(
            #     x='Date',
            #     y='Duration_hrs',
            #     tooltip=['Date', 'Duration_hrs', 'Status']
            # ).properties(title="Daily Attendance")
            # st.altair_chart(daily_chart_current_month, use_container_width=True)




            tab1, tab2, tab3, tab4 = st.tabs(["Yearly", "Monthly", "Weekly", "Daily"])

            with tab1:
                st.metric("Yearly Attendance Percentage", f"{yearly_attendance_percentage:.2f}%", "🔴")
                yearly_pie_chart = create_pie_chart(present_days, total_days, "Yearly Attendance Status Distribution")
                st.altair_chart(yearly_pie_chart, use_container_width=True)

            with tab2:
                sorted_months = all_months_df['Month'].tolist()  # Convert the sorted months to a list
                monthly_chart = alt.Chart(monthly_report_df).mark_bar().encode(
                    x=alt.X('Month', sort=sorted_months),
                    y='Days',
                    tooltip=['Month', 'Days']
                ).properties(title="Monthly Attendance")
                st.altair_chart(monthly_chart, use_container_width=True)

            with tab3:
                weekly_chart = alt.Chart(weekly_report_df).mark_bar().encode(
                    x='Week:O',
                    y='Days',
                    tooltip=['Week', 'Days']
                ).properties(title="Weekly Attendance")
                st.altair_chart(weekly_chart, use_container_width=True)

            with tab4:

                # current_month = datetime.now().strftime('%B')
                # current_month_df = daily_report_df[daily_report_df['Date'].str.contains(datetime.now().strftime('%Y-%m'))]

                # st.subheader(f"Daily Attendance for {current_month}")
                # daily_chart_current_month = alt.Chart(current_month_df).mark_bar().encode(
                #     x='Date',
                #     y='Duration_hrs',
                #     tooltip=['Date', 'Duration_hrs', 'Status']
                # ).properties(title="Daily Attendance")
                # st.altair_chart(daily_chart_current_month, use_container_width=True)


                current_month = datetime.now().strftime('%B')
                # current_month_df = daily_report_df[daily_report_df['Date'].str.contains(datetime.now().strftime('%Y-%m'))]

                daily_chart = alt.Chart(daily_report_df).mark_bar().encode(
                    x='Date',
                    y='Duration_hrs',
                    tooltip=['Date', 'Duration_hrs', 'Status']
                ).properties(title=current_month)
                st.altair_chart(daily_chart, use_container_width=True)

        else:
            st.warning("No attendance data Available")
    else:
        st.warning("No attendance data Available")