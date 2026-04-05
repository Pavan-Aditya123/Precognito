import multiprocessing
import subprocess
import time
import sys
import os
import signal

# Add the backend directory to sys.path
sys.path.append(os.path.join(os.getcwd(), "backend"))

def run_backend():
    """Runs the unified backend (API + MQTT Worker)."""
    print("🚀 Starting Backend (API + MQTT Worker)...")
    subprocess.run(["uv", "run", "python", "main.py"])

def run_frontend():
    """Runs the Next.js frontend."""
    print("🎨 Starting Frontend (dev:lite)...")
    os.chdir("frontend")
    subprocess.run(["bun", "run", "dev:lite"])

def run_simulator():
    """Runs the sensor telemetry simulator."""
    time.sleep(10) # Give the backend time to start up
    print("📡 Starting Sensor Simulator...")
    subprocess.run(["uv", "run", "python", "backend/precognito/ingestion/simulator.py"])

def signal_handler(sig, frame):
    print("\n🛑 Stopping all services...")
    # Processes will be terminated by the multiprocessing manager
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    # Ensure Docker infrastructure is up
    print("🏗️ Ensuring Docker infrastructure (Postgres, InfluxDB, Mosquitto) is running...")
    subprocess.run(["docker-compose", "up", "-d", "postgres", "influxdb", "mosquitto"])

    processes = []
    
    # Define processes
    p_backend = multiprocessing.Process(target=run_backend)
    p_frontend = multiprocessing.Process(target=run_frontend)
    p_simulator = multiprocessing.Process(target=run_simulator)
    
    processes.extend([p_backend, p_frontend, p_simulator])

    # Start all
    for p in processes:
        p.start()

    # Keep main alive
    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        for p in processes:
            p.terminate()
        print("👋 All services stopped.")
