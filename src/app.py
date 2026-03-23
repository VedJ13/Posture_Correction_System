import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from posture_engine import analyze_posture
import mediapipe as mp
import pyttsx3
import time
import threading
from queue import Queue

# -------------------- VOICE SYSTEM  --------------------

engine = pyttsx3.init()
alert_queue = Queue()
speech_lock = threading.Lock()

def voice_worker():
    while True:
        message = alert_queue.get()
        if message:
            with speech_lock:   # prevents crash
                try:
                    engine.say(message)
                    engine.runAndWait()
                except:
                    pass  # prevent app crash


threading.Thread(target=voice_worker, daemon=True).start()

# -------------------- ALERT VARIABLES --------------------


alert_interval = 5
trigger_time = 3

# -------------------- MEDIAPIPE --------------------

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# -------------------- STREAMLIT UI --------------------

st.title("PostureSense")
st.write("Real-time posture monitoring system")

enable_voice = st.checkbox("Enable Voice Alert", value=True)

# -------------------- VIDEO PROCESSOR --------------------

class PostureProcessor(VideoProcessorBase):

    def __init__(self):
        self.last_alert_time = 0
        self.bad_posture_start_time = None

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        posture_text, color, angle, results = analyze_posture(img)

        current_time = time.time()

        # -------------------- SMART ALERT LOGIC --------------------

        if enable_voice:

            if posture_text == "Bad Posture":

                # Start timer
                if self.bad_posture_start_time is None:
                    self.bad_posture_start_time = current_time

                # Trigger only after continuous bad posture
                if current_time - self.bad_posture_start_time > trigger_time:

                    # Repeat every interval
                    if current_time - self.last_alert_time > alert_interval:

                        alert_queue.put("Please correct your posture")

                        self.last_alert_time = current_time

            else:
                # Reset if posture improves
                self.bad_posture_start_time = None

        # -------------------- DRAW SKELETON --------------------

        if results.pose_landmarks:

            mp_drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=3, circle_radius=4),
                mp_drawing.DrawingSpec(color=color, thickness=3)
            )

        # -------------------- TEXT DISPLAY --------------------

        cv2.putText(img,
                    posture_text,
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2)

        cv2.putText(img,
                    f"Angle: {int(angle)}",
                    (30, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# -------------------- START STREAM --------------------

webrtc_streamer(
    key="posture",
    video_processor_factory=PostureProcessor,
    media_stream_constraints={"video": True, "audio": False},
)







































































# import streamlit as st
# import cv2
# import av
# from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
# from pose_detector import analyze_posture
# import mediapipe as mp

# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# st.title("PostureSense AI")
# st.write("Real-time posture monitoring system")

# class PostureProcessor(VideoProcessorBase):

#     def recv(self, frame):

#         img = frame.to_ndarray(format="bgr24")

#         posture_text, color, angle, results = analyze_posture(img)

#         if results.pose_landmarks:

#             mp_drawing.draw_landmarks(
#                 img,
#                 results.pose_landmarks,
#                 mp_pose.POSE_CONNECTIONS,
#                 mp_drawing.DrawingSpec(color=color, thickness=3, circle_radius=4),
#                 mp_drawing.DrawingSpec(color=color, thickness=3)
#             )

#         cv2.putText(img,
#                     posture_text,
#                     (30,50),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     color,
#                     2)

#         cv2.putText(img,
#                     f"Angle: {int(angle)}",
#                     (30,90),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     1,
#                     (255,255,255),
#                     2)

#         return av.VideoFrame.from_ndarray(img, format="bgr24")


# webrtc_streamer(
#     key="posture",
#     video_processor_factory=PostureProcessor
# )


# import streamlit as st
# import av
# import numpy as np
# from streamlit_webrtc import webrtc_streamer
# from posture_engine import analyze_posture
# import mediapipe as mp

# st.title("PostureSense AI")
# st.write("Real-time posture monitoring")

# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose


# class PostureProcessor:

#     def recv(self, frame):

#         img = frame.to_ndarray(format="bgr24")

#         posture_text, color, angle, results = analyze_posture(img)

#         if results.pose_landmarks:
#             mp_drawing.draw_landmarks(
#                 img,
#                 results.pose_landmarks,
#                 mp_pose.POSE_CONNECTIONS
#             )

#         return av.VideoFrame.from_ndarray(img, format="bgr24")


# webrtc_streamer(
#     key="posture",
#     video_processor_factory=PostureProcessor,
#     media_stream_constraints={"video": True, "audio": False},
# )
