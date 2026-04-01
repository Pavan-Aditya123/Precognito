"""
Test cases for batch anomaly detection API
"""

import requests
import json
import time
from typing import List, Dict

# API base URL
BASE_URL = "http://localhost:8000"

def test_batch_normal_data():
    """Test batch with normal sensor readings"""
    print("Test 1: Batch Normal Data")
    print("=" * 50)
    
    batch_data = {
        "data": [
            {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},
            {"machine_id": "M2", "temperature": 295.0, "vibration": 1.0, "torque": 40.0},
            {"machine_id": "M1", "temperature": 302.0, "vibration": 1.3, "torque": 46.0},
            {"machine_id": "M3", "temperature": 298.0, "vibration": 1.1, "torque": 42.0}
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Processed {len(results)} items")
            
            for i, result in enumerate(results):
                print(f"  Item {i+1}: Machine {result['machine_id']} - "
                      f"Anomaly: {result['anomaly_detected']} - "
                      f"Confidence: {result['confidence']:.2f}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on localhost:8000")
    
    print()

def test_batch_with_anomalies():
    """Test batch with mixed normal and anomalous readings"""
    print("Test 2: Batch With Anomalies")
    print("=" * 50)
    
    batch_data = {
        "data": [
            {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},  # Normal
            {"machine_id": "M1", "temperature": 350.0, "vibration": 1.2, "torque": 45.0},  # Temperature spike
            {"machine_id": "M2", "temperature": 295.0, "vibration": 2.5, "torque": 40.0},  # Vibration spike
            {"machine_id": "M3", "temperature": 298.0, "vibration": 1.1, "torque": 85.0},  # Torque critical
            {"machine_id": "M1", "temperature": 302.0, "vibration": 1.3, "torque": 46.0}   # Normal
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Processed {len(results)} items")
            
            anomaly_count = 0
            for i, result in enumerate(results):
                if result['anomaly_detected']:
                    anomaly_count += 1
                    print(f"  🚨 Item {i+1}: Machine {result['machine_id']} - "
                          f"Severity: {result['severity']} - "
                          f"Reason: {result['reason']}")
                else:
                    print(f"  ✅ Item {i+1}: Machine {result['machine_id']} - Normal")
            
            print(f"\nSummary: {anomaly_count}/{len(results)} anomalies detected")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on localhost:8000")
    
    print()

def test_batch_pattern_detection():
    """Test batch to verify pattern detection across multiple readings"""
    print("Test 3: Pattern Detection Across Batch")
    print("=" * 50)
    
    # Send multiple readings for same machine to build pattern, then spike
    batch_data = {
        "data": [
            {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},
            {"machine_id": "M1", "temperature": 301.0, "vibration": 1.3, "torque": 46.0},
            {"machine_id": "M1", "temperature": 299.0, "vibration": 1.1, "torque": 44.0},
            {"machine_id": "M1", "temperature": 302.0, "vibration": 1.4, "torque": 47.0},
            {"machine_id": "M1", "temperature": 340.0, "vibration": 1.2, "torque": 45.0},  # Spike after pattern
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Processed {len(results)} items")
            
            for i, result in enumerate(results):
                print(f"  Item {i+1}: Temp={result['metrics'].get('temperature', 'N/A')} - "
                      f"Anomaly: {result['anomaly_detected']} - "
                      f"Confidence: {result['confidence']:.2f}")
                
                if result['anomaly_detected']:
                    print(f"    Pattern: {result.get('pattern_analysis', {})}")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on localhost:8000")
    
    print()

def test_batch_different_machines():
    """Test batch with multiple machines having different patterns"""
    print("Test 4: Multiple Machines Different Patterns")
    print("=" * 50)
    
    batch_data = {
        "data": [
            {"machine_id": "M1", "temperature": 300.0, "vibration": 1.2, "torque": 45.0},
            {"machine_id": "M2", "temperature": 295.0, "vibration": 2.0, "torque": 40.0},
            {"machine_id": "M1", "temperature": 305.0, "vibration": 1.3, "torque": 46.0},
            {"machine_id": "M2", "temperature": 298.0, "vibration": 2.1, "torque": 41.0},
            {"machine_id": "M3", "temperature": 302.0, "vibration": 1.5, "torque": 50.0},
            {"machine_id": "M1", "temperature": 320.0, "vibration": 1.2, "torque": 45.0},  # Spike for M1
            {"machine_id": "M2", "temperature": 296.0, "vibration": 2.8, "torque": 40.0},  # Spike for M2
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"Processed {len(results)} items")
            
            machine_anomalies = {}
            for i, result in enumerate(results):
                machine_id = result['machine_id']
                if machine_id not in machine_anomalies:
                    machine_anomalies[machine_id] = 0
                
                if result['anomaly_detected']:
                    machine_anomalies[machine_id] += 1
                    print(f"  🚨 Item {i+1}: Machine {machine_id} - {result['severity']} - {result['reason']}")
                else:
                    print(f"  ✅ Item {i+1}: Machine {machine_id} - Normal")
            
            print(f"\nAnomalies by machine:")
            for machine, count in machine_anomalies.items():
                print(f"  {machine}: {count} anomalies")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on localhost:8000")
    
    print()

def test_batch_edge_cases():
    """Test batch edge cases and error handling"""
    print("Test 5: Edge Cases and Error Handling")
    print("=" * 50)
    
    # Test empty batch
    print("Subtest 5.1: Empty batch")
    try:
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json={"data": []})
        print(f"Empty batch status: {response.status_code}")
        if response.status_code == 200:
            print(f"Empty batch result: {response.json()}")
    except Exception as e:
        print(f"Empty batch error: {e}")
    
    # Test missing fields
    print("\nSubtest 5.2: Missing required fields")
    try:
        batch_data = {
            "data": [
                {"machine_id": "M1"},  # Missing sensor data
                {"temperature": 300.0},  # Missing machine_id
            ]
        }
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        print(f"Missing fields status: {response.status_code}")
        if response.status_code != 200:
            print(f"Expected error: {response.text}")
    except Exception as e:
        print(f"Missing fields error: {e}")
    
    # Test invalid data types
    print("\nSubtest 5.3: Invalid data types")
    try:
        batch_data = {
            "data": [
                {"machine_id": "M1", "temperature": "invalid", "vibration": 1.2, "torque": 45.0}
            ]
        }
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        print(f"Invalid types status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()[0]
            print(f"Handled gracefully: {result.get('error', 'No error field')}")
    except Exception as e:
        print(f"Invalid types error: {e}")
    
    print()

def test_batch_large_volume():
    """Test batch with larger volume of data"""
    print("Test 6: Large Volume Batch")
    print("=" * 50)
    
    # Generate 100 sensor readings
    batch_data = {"data": []}
    
    for i in range(100):
        machine_id = f"M{i % 5 + 1}"  # 5 machines
        # Mostly normal data with occasional anomalies
        if i % 20 == 0:  # Every 20th item is an anomaly
            temperature = 320.0 + (i % 10)
            vibration = 2.5 + (i % 5) * 0.1
        else:
            temperature = 295.0 + (i % 10)
            vibration = 1.0 + (i % 5) * 0.1
        
        batch_data["data"].append({
            "machine_id": machine_id,
            "temperature": temperature,
            "vibration": vibration,
            "torque": 40.0 + (i % 20)
        })
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/anomaly/detect/batch", json=batch_data)
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Processing time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            results = response.json()
            anomaly_count = sum(1 for r in results if r['anomaly_detected'])
            print(f"Processed {len(results)} items")
            print(f"Anomalies detected: {anomaly_count}")
            print(f"Anomaly rate: {anomaly_count/len(results)*100:.1f}%")
        else:
            print(f"Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on localhost:8000")
    
    print()

def run_all_tests():
    """Run all batch API tests"""
    print("Starting Batch API Tests")
    print("=" * 80)
    print("Make sure the FastAPI server is running on localhost:8000")
    print("Run: python main_simple.py")
    print("=" * 80)
    print()
    
    test_batch_normal_data()
    test_batch_with_anomalies()
    test_batch_pattern_detection()
    test_batch_different_machines()
    test_batch_edge_cases()
    test_batch_large_volume()
    
    print("All batch tests completed!")

if __name__ == "__main__":
    run_all_tests()
