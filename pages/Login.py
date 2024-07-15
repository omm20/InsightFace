import streamlit as st
from streamlit import session_state as ss
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

# from modules.menu import menu
from modules.nav import menu_nav
menu_nav()

# if ss.authentication_status:
#     def sidebar_header():
#         st.sidebar.header(f"**{name}**")


    
CONFIG_FILENAME = 'config.yaml'

def load_config():
    try:
        with open(CONFIG_FILENAME) as file:
            return yaml.load(file, Loader=SafeLoader)
    except Exception as e:
        st.warning(f"Error loading config: {e}")
        return None

config = load_config()

# st.write(config)
# st.write(f"Available usernames in config: {list(config['credentials']['usernames'].keys())}")

if config is None:
    st.error("Failed to load configuration.")
    st.stop()

st.header('Account page')

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if "role" not in ss:
    ss.role = None

# ss._role = ss.role

def set_role():
    ss.role = ss._role

login_tab, register_tab = st.tabs(['LOGIN', 'SIGNUP'])

with login_tab:
    # try:
        selected_role = st.selectbox(
            "Select your role",
            ["Student", "Teacher", "Admin"],
            key="_role",
            on_change=set_role,
            index=["Student", "Teacher", "Admin"].index(
                ss.role) 
                if ss.role is not None else 0
        )

        # st.info(f"Role Selected is {selected_role}")
        # authenticator.logout(location='main')

        if selected_role:
            name, authentication_status, username = authenticator.login(location='main', 
                                                                        clear_on_submit=True)
            # st.write(username)
            # st.write(authentication_status)
            # st.write(name)

            if username:
                if username in config['credentials']['usernames']:
                    user_role = config['credentials']['usernames'][username]['role']
                    # if user_role == selected_role:
                    if authentication_status:
                        if user_role != selected_role:
                            st.info(f"You are authorized as Your registered {user_role} Role")
                            ss.role = user_role
                            selected_role = user_role
                        
                        st.success(f"Welcome {name}!")
                        # st.sidebar.header(f"**{name}**")
                        authenticator.logout(location='main')
                        # Add code here to handle successful authentication and role match
                    else:
                        st.error("Username/password is incorrect")
                else:
                    st.error("Username not found")
                    # st.experimental_rerun()
            else:
                st.warning("Please enter your username and password")
        else:
            st.warning("Select a Role")      


with register_tab:
    if not ss["authentication_status"]:
        try:
            selected_role = st.selectbox(
                "Select your role",
                ["Student", "Teacher"],
            )

            email, username, name = authenticator.register_user(pre_authorization=False)
            config["credentials"]["usernames"][username]["role"] = selected_role
            # Add select box to select a row
            
            st.write(name)
            
            if email:
                st.success('User registered successfully')
                with open(CONFIG_FILENAME, 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.switch_page("pages/Register_Face_Data.py")
            else:
                st.warning("Info Incorrect")
        except Exception as e:
            # st.error(e)
            st.warning('Info Incorrect')

    


        
























                # st.write(username)
                # st.write(authentication_status)
                # st.write(name)

                    # if authentication_status:
                    #     ss["authentication_status"] = True
                    #     ss["name"] = name
                    #     ss["username"] = username
                    #     ss["role"] = user_role
                    #     st.success(f"Welcome {name}")
                    #     st.write(f'Logged in as {username} with role {user_role}')
                    #         # Call your menu function or redirect the user to the main application
                    #     # menu()
                    #     authenticator.logout(location='main')
                    #     st.info(ss["authentication_status"])  
                        
                    #     menu()  
                    #     st.write(f'Welcome {ss["name"]}')
                    #     st.write(f'Hi {ss}')
                   
                    # elif authentication_status is None:
                    #     st.warning('Please enter your username and password')

                    # else:
                    #     st.error('Username/password is incorrect')
        #         
        
        
        
        
  # def get_roles():
#     """Gets user roles based on config file."""
#     with open(CONFIG_FILENAME) as file:
#         config = yaml.load(file, Loader=SafeLoader)

#     if config is not None:
#         cred = config['credentials']
#     else:
#         cred = {}

# #  usernames as keys and their corresponding roles as values.
#     return {username: user_info['role'] for username, 
#             user_info in cred['usernames'].items() if 'role' in user_info}
          
        
        
        
        # else:
        #             st.error("You are not registered as this role.")
        #     else:
        #         st.warning('Please enter your username and password')
        # else:
        #     st.warning('Please select a role.')
                         
            
            # elif selected_role:
            #     st.error("Authentication failed.")
            # else:
            #     authentication_status=False
            #     st.error("You are not registered as this role.")
            
                
            #     # teachers = [k for k, v in user_roles.items() if v == 'teacher']

            # elif ss["authentication_status"] is None:
            #     st.warning('Please enter your username and password')

            # elif ss["authentication_status"] is False:
            #     st.error('Username/password is incorrect')

        # except Exception as e:
        #     st.error("err")

    # 1. Select Role
    # print(f"selected role is {selected_role}")


    # 2. Login as selected role/
    # if selected_role is not None:
    #     pass

    # if selected_role:
    #     st.write(f"Selected role: {selected_role}")
    # else:
    #     st.error("Role not found.")


    # if ss["authentication_status"]:

    #         teachers = [k for k, v in user_roles.items() if v == 'teacher']

    #         # Show page 1 if the username that logged in is an admin.
    #         if ss.username in teachers:
    #             attendanceReportNav()

    # MenuButtons(get_roles())