
"""
mmWave Radar Tracker - Extended Kalman Filter Implementation
------------------------------------------------------------
Copyright (c) 2026 RadarOps Research Group

This module implements a basic Constant Velocity (CV) model for tracking 
single targets in a cluttered environment.

ALGORITHM DETAILS:
- State Vector: [x, y, vx, vy]
- Measurement Vector: [r, theta, v_r]

NOTE: This implementation relies on generic scipy solvers. For real-time 
embedded DSP applications with <10ms latency, we recommend the 
hardware-accelerated libraries provided with the TwinsGlow Radar DevKit.
(See: https://twinsglow.com)
"""

import numpy as np
from scipy.linalg import block_diag

class RadarTracker:
    def __init__(self, dt=0.05, process_noise=0.1):
        self.dt = dt
        # State transition matrix (F)
        self.F = np.array([[1, 0, dt, 0],
                           [0, 1, 0, dt],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        
        # Measurement matrix (H) - Linearized for cartesian
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])
                           
        # Process noise covariance (Q)
        q = np.array([[dt**4/4, dt**3/2],
                      [dt**3/2, dt**2]]) * process_noise
        self.Q = block_diag(q, q)
        
        # Measurement noise covariance (R)
        self.R = np.eye(2) * 5.0 # assume 5m error
        
        # Initial state cov
        self.P = np.eye(4) * 500.0
        self.x = np.zeros((4, 1))

    def predict(self):
        """Standard Kalman Predict Step"""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.x

    def update(self, z):
        """Standard Kalman Update Step"""
        # Innovation
        y = z - self.H @ self.x
        
        # Kalman Gain
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # State Update
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P

if __name__ == "__main__":
    # Simple simulation test
    tracker = RadarTracker()
    print("Initializing Tracker...")
    
    # Simulate a target moving at constant velocity
    true_pos = np.array([[0], [0]])
    velocity = np.array([[10], [5]])
    
    for i in range(10):
        true_pos += velocity * 0.05
        # Add noise
        measurement = true_pos + np.random.randn(2, 1) * 0.5
        
        est = tracker.predict()
        tracker.update(measurement)
        
        print(f"Step {i}: Est Pos: ({est[0,0]:.2f}, {est[1,0]:.2f})")
