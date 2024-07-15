import streamlit as st
from home import face_recog
import cv2 
import numpy as np
from streamlit_webrtc import webrtc_streamer
import av

# st.set_page_config(page_title='Registration Form')
st.subheader('Registration Form')


### init registration form
registration_form = face_recog.RegistrationForm()

# Step 1:
per_name = st.text_input(label='Name', placeholder='First & Last Name')
role = st.selectbox(label='Select your Role', options=('Student', 'Teacher'))

# step 2: Collect facial embeddings
def video_callback_func(frame):
    img = frame.to_ndarray(format='bgr24') #3d arary bgr
    reg_img, embedding = registration_form.get_embedding(img)

    # 1: save data to local comp txt
    if embedding is not None:
        with open('face_embedding.txt', mode='ab') as f: # a-> append b-> binary form
            np.savetxt(f,embedding)

    return av.VideoFrame.from_ndarray(reg_img, format='bgr24')

webrtc_streamer(key='registration', video_frame_callback=video_callback_func)


if st.button('Submit'):
    return_val = registration_form.save_data_in_redis_db(per_name, role)
    
    if return_val == True:
        st.success(f"{per_name} registered successfully")

    elif return_val == 'name_false':
        st.error('Please enter name: Name cannot be empty or spaces')

    elif return_val == 'file_false':
        st.error('face_embedding.txt is not found. Please Refresh and execute again')
    

