import streamlit as st
from streamlit import session_state as ss
# from pages.Login import authenticator

def HomeNav():
    st.sidebar.page_link("Home.py", label="Home")

def switch_Account():
    st.sidebar.page_link("Home.py", label="Switch Role")
    ss.role=None

def loginNav():
    st.sidebar.page_link("pages/Login.py", label="Login")

def logoutNav():
    st.sidebar.page_link("pages/Login.py", label="Logout")

def markAttendanceNav():
    st.sidebar.page_link("pages/Mark_Attendance.py", label="Mark Attendance")

def profileNav():
    st.sidebar.page_link("pages/Profile.py", label="Profile")

def attendanceReportNav():
    st.sidebar.page_link("pages/View_Attendance_Report.py", label="Student Attendance Report")

def teacherAttRepNav():
    st.sidebar.page_link("pages/View_Teacher_Attendance_Report.py", label="Teacher Attendance Report")

def unauthorised_btns():
    HomeNav()
    loginNav()
    markAttendanceNav()

def authorised_btns():
    profileNav()
    logoutNav()
    # HomeNav()
    markAttendanceNav()
    # logoutNav()
    


def admin_btns():
    # HomeNav()
    logoutNav()
    attendanceReportNav()
    teacherAttRepNav()
    

# def logout_btns():
#     HomeNav()
#     # logoutNav()
#     markAttendanceNav()
#     profileNav()


def menu_nav():
    if 'authentication_status' not in ss:
        ss['authentication_status'] = None

    if ss['authentication_status'] is None:
        unauthorised_btns()

    elif 'authentication_status' in ss and ss["authentication_status"]:
        st.sidebar.header(f"**{ss.name}**")
        # authenticator.logout(location='sidebar')
        
        if ss['role'] in ("Teacher", "Student"):
            authorised_btns()
        if ss['role'] == "Teacher":
            attendanceReportNav()
        elif ss['role'] == "Admin":
            admin_btns()

def MenuButtons(user_roles=None):
    if user_roles is None:
        user_roles = {}

    if 'authentication_status' not in ss:
        ss.authentication_status = False

    # Always show the home and login navigators.
    HomeNav()
    loginNav()
    markAttendanceNav()

    # Show the other page navigators depending on the users' role.
    if ss["authentication_status"]:

        teachers = [k for k, v in user_roles.items() if v == 'teacher']

        # Show page 1 if the username that logged in is an admin.
        if ss.username in teachers:
            attendanceReportNav()