import mediapipe as mp

print("MediaPipe module file:")
print(mp.__file__)

print("Has solutions?")
print(hasattr(mp, "solutions"))

print("Module contents (first 20):")
print(dir(mp)[:20])
