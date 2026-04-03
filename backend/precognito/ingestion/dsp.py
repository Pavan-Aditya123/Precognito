"""
Digital Signal Processing (DSP) module for analyzing raw sensor waveforms.
"""
import numpy as np
from typing import Dict, List

def calculate_rms(samples: np.ndarray) -> float:
    """Calculates the Root Mean Square (RMS) of a signal.

    Args:
        samples (np.ndarray): An array of signal samples.

    Returns:
        float: The RMS value of the signal.
    """
    if len(samples) == 0:
        return 0.0
    return float(np.sqrt(np.mean(samples**2)))

def extract_fft_peaks(samples: np.ndarray, sampling_rate: int = 1000) -> Dict[str, float]:
    """Performs FFT and extracts dominant frequency amplitudes.

    Args:
        samples (np.ndarray): An array of signal samples.
        sampling_rate (int, optional): The sampling rate in Hz. Defaults to 1000.

    Returns:
        Dict[str, float]: A dictionary containing normalized amplitudes for 
                          1x and BPFO frequency spikes.
    """
    n = len(samples)
    if n == 0:
        return {"freq_1x": 0.0, "freq_bpfo": 0.0}
        
    # Perform FFT
    fft_values = np.fft.rfft(samples)
    amplitudes = np.abs(fft_values)
    freqs = np.fft.rfftfreq(n, d=1/sampling_rate)
    
    # In a real industrial scenario, we look for specific multiples of RPM (1x) 
    # or bearing specific frequencies (BPFO).
    # For simulation, we'll just find the max amplitude in expected bands.
    
    # 1x peak (e.g., 10-30Hz range)
    idx_1x = np.where((freqs >= 10) & (freqs <= 30))[0]
    amp_1x = np.max(amplitudes[idx_1x]) if len(idx_1x) > 0 else 0.0
    
    # BPFO peak (e.g., 80-120Hz range for bearing faults)
    idx_bpfo = np.where((freqs >= 80) & (freqs <= 120))[0]
    amp_bpfo = np.max(amplitudes[idx_bpfo]) if len(idx_bpfo) > 0 else 0.0
    
    return {
        "freq_spike_1x": float(amp_1x) / n, # Normalized
        "freq_spike_bpfo": float(amp_bpfo) / n
    }

def process_raw_edge_data(raw_values: List[float]) -> Dict[str, float]:
    """Processes raw edge data by calculating RMS and FFT peaks.

    Args:
        raw_values (List[float]): A list of raw signal values.

    Returns:
        Dict[str, float]: A dictionary containing processed metrics: 
                          'vibration_rms', 'freq_spike_1x', and 'freq_spike_bpfo'.
    """
    samples = np.array(raw_values)
    rms = calculate_rms(samples)
    peaks = extract_fft_peaks(samples)
    
    return {
        "vibration_rms": round(rms, 4),
        "freq_spike_1x": round(peaks["freq_spike_1x"], 4),
        "freq_spike_bpfo": round(peaks["freq_spike_bpfo"], 4)
    }
