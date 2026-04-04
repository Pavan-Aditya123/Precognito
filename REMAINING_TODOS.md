# Remaining Tasks for Precognito

This document tracks the technical and functional polish required to transition from a prototype to a full production system.

## 1. Communications (Module 6)
- [ ] **Enterprise Notification Providers**: Integrate with formal **Twilio** (SMS) and **SendGrid** (Email) services for redundant critical alerting (TC_M6_02).
- [ ] **User Notification Preferences**: Allow users to toggle between In-App, SMS, and Email channels in the Settings page.

## 2. Hardware/Edge (Module 1)
- [ ] **ESP32 Firmware Finalization**: Port the `dsp.py` logic to C++ for native execution on edge hardware.
- [ ] **OTA Updates**: Secure Over-the-Air (OTA) firmware updates for edge sensor nodes.

## 3. Financials (Module 5)
- [ ] **Teammate Integration**: Verify and merge final UI components from teammate's financial module.
