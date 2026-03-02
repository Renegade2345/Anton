ANTON — Real-Time Video Threat Intelligence

ANTON is a real-time surveillance intelligence system that detects objects, tracks behavioral events, and generates explainable threat scores from live video streams.

Built with YOLOv8 and a modular event-driven architecture, it converts raw webcam input into structured threat insights displayed through a tactical dashboard.

Features

Real-time object detection (YOLOv8)

Event-based object tracking (enter/exit)

Zone monitoring logic

Watchlist-based escalation

Dynamic threat scoring with decay

Severity-coded event logs

Live threat trend visualization

Lightweight, low-latency architecture

 Architecture

Camera
→ YOLO Detection
→ State Engine
→ Zone Engine
→ Watchlist Engine
→ Threat Engine
→ Tactical Dashboard

The system is modular, interpretable, and optimized for real-time performance.

Tech Stack

Python

YOLOv8 (Ultralytics)

OpenCV

Streamlit

Modular event-driven architecture

Run Locally:

streamlit run dashboard.py

Ensure webcam access is enabled.

Purpose

ANTON demonstrates how real-time video feeds can be transformed into structured, explainable threat intelligence using modular AI systems.


