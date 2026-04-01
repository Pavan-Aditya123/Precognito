#!/bin/bash

# Batch API Test Script using curl
# Make sure the FastAPI server is running on localhost:8000

BASE_URL="http://localhost:8000"

echo "Batch API Tests using curl"
echo "=========================="
echo

# Test 1: Normal batch data
echo "Test 1: Normal batch data"
curl -X POST "$BASE_URL/anomaly/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},
      {"machine_id": "M2", "temperature": 295.0, "vibration": 1.0, "torque": 40.0},
      {"machine_id": "M1", "temperature": 302.0, "vibration": 1.3, "torque": 46.0}
    ]
  }' | jq '.'
echo
echo

# Test 2: Batch with anomalies
echo "Test 2: Batch with anomalies"
curl -X POST "$BASE_URL/anomaly/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},
      {"machine_id": "M1", "temperature": 350.0, "vibration": 1.2, "torque": 45.0},
      {"machine_id": "M2", "temperature": 295.0, "vibration": 2.5, "torque": 40.0},
      {"machine_id": "M3", "temperature": 298.0, "vibration": 1.1, "torque": 85.0}
    ]
  }' | jq '.'
echo
echo

# Test 3: Pattern detection (same machine multiple readings)
echo "Test 3: Pattern detection"
curl -X POST "$BASE_URL/anomaly/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},
      {"machine_id": "M1", "temperature": 301.0, "vibration": 1.3, "torque": 46.0},
      {"machine_id": "M1", "temperature": 299.0, "vibration": 1.1, "torque": 44.0},
      {"machine_id": "M1", "temperature": 302.0, "vibration": 1.4, "torque": 47.0},
      {"machine_id": "M1", "temperature": 340.0, "vibration": 1.2, "torque": 45.0}
    ]
  }' | jq '.'
echo
echo

# Test 4: Empty batch
echo "Test 4: Empty batch"
curl -X POST "$BASE_URL/anomaly/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{"data": []}' | jq '.'
echo
echo

# Test 5: Invalid data
echo "Test 5: Invalid data"
curl -X POST "$BASE_URL/anomaly/detect/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"machine_id": "M1"},
      {"temperature": 300.0}
    ]
  }' | jq '.'
echo
echo

echo "All curl tests completed!"
