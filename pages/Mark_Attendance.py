import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import time

# st.set_page_config(page_title="Attendance System", layout='centered')
st.subheader('Real Time Attendance System')

from modules.nav import menu_nav
menu_nav()

try:
    from Home import face_recog
except:
    st.write("Connection Error")
    face_recog = None

# Retrive data from database
with st.spinner('Retriving Data from Redis DB...'):
    try:
        redis_face_db = face_recog.retrive_data(name='academy:register')
        st.dataframe(redis_face_db)
        st.success('Data Successfully retrieved from Redis')
    except:
        st.warning("No Connection")


# time
waitTime = 30 # in secs
setTime = time.time()
realtimepred = face_recog.RealTimePred() # real time pred class

# Real Time Prediction
def video_frame_callback(frame):
    global setTime
    img = frame.to_ndarray(format="bgr24") # 3d numpy array

    pred_img = realtimepred.face_prediction(img, redis_face_db, 'facial_features',
                                          ['Name','Role'], thresh=0.5)
    
    # print(pred_img)

    timenow = time.time()
    difftime = timenow-setTime

    if difftime >= waitTime:
        print("in")
        realtimepred.saveLogs_redis()
        setTime = time.time() # redis time

        st.success('Save Data to redis Database')

    return av.VideoFrame.from_ndarray(pred_img, format="bgr24")


webrtc_streamer(key="realtimeprediction", video_frame_callback=video_frame_callback)
