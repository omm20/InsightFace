import streamlit as st

from modules.nav import menu_nav
menu_nav()

st.header('Welcome to Face Recognition Attendance System')

with st.spinner('Loading Models and connecting to Redis db...'):
    try:
        import face_recog
    except:
        st.error('Failed to import models')


































# if "role" not in ss:
#     ss.role = None

# st.session_state._role = st.session_state.role

# def set_role():
#     st.session_state.role = st.session_state._role

# # choose role
# # global selected_role

# selected_role = st.selectbox(
#     "Select your role:",
#     ["Student", "Teacher", "Admin"],
#     key="_role",
#     on_change=set_role,
# )

# # 1. Select Role
# print(f"selected role is {selected_role}")


# # 2. Login as selected role/
# if selected_role is not None:
#     # st.switch_page("pages/Login.py")
#     if st.button("Select"):
#         params = urlencode({"role": selected_role})
#         login_url = f"/Login?{params}"
        
#         # st.experimental_set_query_params(role=selected_role)
#         # st.experimental_rerun()
#         st.markdown(f"[Login]({login_url})")















# selected_role = st.selectbox(
#     "Select your role:",
#     ["Student", "Teacher", "Admin"],
#     key="_role",
# )


    # login(selected_role)

# if selected_role:
#     ss.role = selected_role
#     st.write(f"Selected role: {selected_role}")
    
#     if st.button("Login"):
#         ss.login_requested = True
#         # ss.selected_role = selected_role
#         # st.experimental_rerun()

# else:
#     st.warning("Please select a role.")

# if ss.role:
#     st.sidebar.button("switch account")
#     ss.role = None

# # Handle redirection to login page if login is requested
# if "login_requested" in st.session_state:
#     if st.session_state.login_requested:
#         # st.rerun()

# if st.session_state.role:
#     st.sidebar.title("Options")
#     if st.sidebar.button("Switch Account"):
#         st.session_state.role = None

#



# if role matches with selected role then
    # menu()