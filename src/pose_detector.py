import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def analyze_posture(frame):

    image = frame.copy()
    h, w, _ = image.shape

    results = pose.process(image)

    posture_text = "Detecting..."
    color = (255,255,255)
    angle = 0

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        nose = landmarks[0]

        left_shoulder_x = int(left_shoulder.x * w)
        left_shoulder_y = int(left_shoulder.y * h)

        right_shoulder_x = int(right_shoulder.x * w)
        right_shoulder_y = int(right_shoulder.y * h)

        left_hip_x = int(left_hip.x * w)
        left_hip_y = int(left_hip.y * h)

        right_hip_x = int(right_hip.x * w)
        right_hip_y = int(right_hip.y * h)

        nose_y = int(nose.y * h)

        shoulder_mid_x = int((left_shoulder_x + right_shoulder_x) / 2)
        shoulder_mid_y = int((left_shoulder_y + right_shoulder_y) / 2)

        hip_mid_x = int((left_hip_x + right_hip_x) / 2)
        hip_mid_y = int((left_hip_y + right_hip_y) / 2)

        spine_vector = np.array([
            shoulder_mid_x - hip_mid_x,
            shoulder_mid_y - hip_mid_y
        ])

        vertical_vector = np.array([0, -1])

        cos_theta = np.dot(spine_vector, vertical_vector) / (
            np.linalg.norm(spine_vector) * np.linalg.norm(vertical_vector)
        )

        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        angle = np.degrees(np.arccos(cos_theta))

        vertical_diff = abs(shoulder_mid_x - hip_mid_x)

        if angle < 10 and vertical_diff < 20:
            posture_text = "Good Posture"
            color = (0,255,0)

        elif angle < 20:
            posture_text = "Slight Bend"
            color = (0,255,255)

        else:
            posture_text = "Bad Posture"
            color = (0,0,255)

    return posture_text, color, angle, results










































































# import cv2
# import mediapipe as mp

# mp_pose = mp.solutions.pose
# mp_draw = mp.solutions.drawing_utils

# pose = mp_pose.Pose()

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     result = pose.process(rgb)

#     if result.pose_landmarks:
#         mp_draw.draw_landmarks(
#             frame,
#             result.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS
#         )

#     cv2.imshow("Pose Detection", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# import mediapipe as mp
# import numpy as np

# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()

# def analyze_posture(frame):

#     image = frame.copy()
#     h, w, _ = image.shape

#     results = pose.process(image)

#     posture_text = "Detecting..."
#     color = (255,255,255)
#     angle = 0

#     if results.pose_landmarks:

#         landmarks = results.pose_landmarks.landmark

#         left_shoulder = landmarks[11]
#         right_shoulder = landmarks[12]
#         left_hip = landmarks[23]
#         right_hip = landmarks[24]
#         nose = landmarks[0]

#         left_shoulder_x = int(left_shoulder.x * w)
#         left_shoulder_y = int(left_shoulder.y * h)

#         right_shoulder_x = int(right_shoulder.x * w)
#         right_shoulder_y = int(right_shoulder.y * h)

#         left_hip_x = int(left_hip.x * w)
#         left_hip_y = int(left_hip.y * h)

#         right_hip_x = int(right_hip.x * w)
#         right_hip_y = int(right_hip.y * h)

#         nose_y = int(nose.y * h)

#         shoulder_mid_x = int((left_shoulder_x + right_shoulder_x) / 2)
#         shoulder_mid_y = int((left_shoulder_y + right_shoulder_y) / 2)

#         hip_mid_x = int((left_hip_x + right_hip_x) / 2)
#         hip_mid_y = int((left_hip_y + right_hip_y) / 2)

#         spine_vector = np.array([
#             shoulder_mid_x - hip_mid_x,
#             shoulder_mid_y - hip_mid_y
#         ])

#         vertical_vector = np.array([0, -1])

#         cos_theta = np.dot(spine_vector, vertical_vector) / (
#             np.linalg.norm(spine_vector) * np.linalg.norm(vertical_vector)
#         )

#         cos_theta = np.clip(cos_theta, -1.0, 1.0)
#         angle = np.degrees(np.arccos(cos_theta))

#         vertical_diff = abs(shoulder_mid_x - hip_mid_x)

#         if angle < 10 and vertical_diff < 20:
#             posture_text = "Good Posture"
#             color = (0,255,0)

#         elif angle < 20:
#             posture_text = "Slight Bend"
#             color = (0,255,255)

#         else:
#             posture_text = "Bad Posture"
#             color = (0,0,255)

#     return posture_text, color, angle, results
