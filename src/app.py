import streamlit as st
import cv2
import av
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from pose_detector import analyze_posture
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

st.title("PostureSense AI")
st.write("Real-time posture monitoring system")

class PostureProcessor(VideoProcessorBase):

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        posture_text, color, angle, results = analyze_posture(img)

        if results.pose_landmarks:

            mp_drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=3, circle_radius=4),
                mp_drawing.DrawingSpec(color=color, thickness=3)
            )

        cv2.putText(img,
                    posture_text,
                    (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2)

        cv2.putText(img,
                    f"Angle: {int(angle)}",
                    (30,90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="posture",
    video_processor_factory=PostureProcessor
)


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
