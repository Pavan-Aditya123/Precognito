# Remaining Tasks for Precognito

This document tracks the final technical and functional polish required to transition from a prototype to a full production system.

## 1. Financial & Reporting (Module 5)
- [ ] **High-Integrity Reporting**: Add "Authorized Signature" blocks and official company headers to generated PDF reports (FR 17.6).
- [ ] **Automated Maintenance Cost Tracking**: Calculate actual cost per work order by summing part costs + technician labor hours.
- [ ] **ROI Monthly Summary**: Automatic generation of monthly "Downtime Avoided" dollar-value reports.

## 2. Communications (Module 6)
- [ ] **Enterprise Notification Providers**: Integrate with **Twilio** (SMS) and **SendGrid** (Email) for redundant critical alerting (TC_M6_02).
- [ ] **User Notification Preferences**: Allow users to toggle between In-App, SMS, and Email channels in the Settings page.

## 3. PWA & Frontend Polish
- [ ] **QR Code Error Recovery**: Add manual ID entry fallback if the mobile camera cannot read a damaged physical QR tag.
- [ ] **Dark Mode Toggle**: Persistent theme switching for varied factory lighting conditions.

## 4. Hardware/Edge (Module 1)
- [ ] **ESP32 Firmware Finalization**: Port the `dsp.py` logic to C++ for native execution on edge hardware.
- [ ] **OTA Updates**: Secure Over-the-Air (OTA) firmware updates for edge sensor nodes.
