import streamlit as st
import cv2
import time
from agent import run_anton_frame  

st.set_page_config(layout="wide")

st.title("🛰 ANTON Tactical Recon Interface")

col1, col2, col3 = st.columns([1, 2, 1])

threat_placeholder = col1.empty()
status_placeholder = col1.empty()

video_placeholder = col2.empty()

event_placeholder = col3.empty()

threat_level = 0
events = []

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Call Anton logic 
    processed_frame, threat_level, new_events = run_anton_frame(frame)

    events.extend(new_events)
    events = events[-10:]

    threat_placeholder.metric("Threat Level", f"{threat_level:.2f}")
    status_placeholder.success("System Operational")

    video_placeholder.image(processed_frame, channels="BGR")

    event_placeholder.write("### Recent Events")
    for e in reversed(events):
        event_placeholder.write(f"- {e}")

    time.sleep(0.03)