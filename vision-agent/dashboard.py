import streamlit as st
import cv2
import time
from agent import run_anton_frame



st.set_page_config(layout="wide")



st.markdown("""
<style>
body {
    background-color: #0b0f14;
    color: #e6edf3;
}
.stMetric {
    background-color: #111821;
    padding: 10px;
    border-radius: 8px;
}
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🛰 ANTON Tactical Recon Interface")

col1, col2, col3 = st.columns([1, 2, 1])

threat_placeholder = col1.empty()
status_placeholder = col1.empty()
progress_placeholder = col1.empty()
trend_placeholder = col1.empty()

video_placeholder = col2.empty()

event_placeholder = col3.empty()
analysis_placeholder = col3.empty()



threat_level = 0.0
events = []
threat_history = []

cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not accessible.")
        break

    processed_frame, threat_level, new_events = run_anton_frame(frame)

    # Maintain last 15 events
    events.extend(new_events)
    events = events[-15:]

    # Maintain last 50 threat values
    threat_history.append(threat_level)
    threat_history = threat_history[-50:]



    threat_placeholder.metric("Threat Level", f"{threat_level:.2f}")

    if threat_level < 0.3:
        status_placeholder.success("Status: Stable")
    elif threat_level < 0.7:
        status_placeholder.warning("Status: Elevated")
    else:
        status_placeholder.error("Status: Critical")

    progress_placeholder.progress(threat_level)

    trend_placeholder.markdown("### Threat Trend")
    trend_placeholder.line_chart(threat_history)


    video_placeholder.image(processed_frame, channels="BGR")



    event_placeholder.markdown("### Recent Events")

    for e in reversed(events):

        if "WATCHLIST" in e:
            event_placeholder.markdown(
                f"<span style='color:red'>🔴 {e}</span>",
                unsafe_allow_html=True
            )

        elif "ZONE" in e:
            event_placeholder.markdown(
                f"<span style='color:orange'>🟠 {e}</span>",
                unsafe_allow_html=True
            )

        else:
            event_placeholder.markdown(
                f"<span style='color:lightgreen'>🟢 {e}</span>",
                unsafe_allow_html=True
            )



    analysis_placeholder.markdown("### Threat Analysis")

    if events:
        analysis_placeholder.write("Escalation Drivers:")
        for e in events[-3:]:
            analysis_placeholder.write(f"- {e}")
    else:
        analysis_placeholder.write("No active escalation drivers.")

    time.sleep(0.03)