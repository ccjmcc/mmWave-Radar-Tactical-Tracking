
"""
Radar Data Visualizer
---------------------
Reads CSV logs and plots Range-Azimuth heatmap.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse

def plot_tracks(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print("Error: Log file not found.")
        return

    # Convert Polar to Cartesian
    # x = r * sin(theta)
    # y = r * cos(theta)
    
    r1 = df[' T1_R']
    th1 = df[' T1_THETA']
    x1 = r1 * np.sin(th1)
    y1 = r1 * np.cos(th1)
    
    r2 = df[' T2_R']
    th2 = df[' T2_THETA']
    x2 = r2 * np.sin(th2)
    y2 = r2 * np.cos(th2)
    
    plt.figure(figsize=(10,8))
    plt.plot(x1, y1, 'bo-', label='Target 1 (Pedestrian)')
    plt.plot(x2, y2, 'rx--', label='Target 2 (Vehicle)')
    
    plt.title("Tactical Radar Tracking Replay")
    plt.xlabel("Cross-Range (m)")
    plt.ylabel("Down-Range (m)")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    
    print("Generating plot...")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize TwinsGlow Radar Logs")
    parser.add_argument("--file", default="../data/sample_log.csv", help="Path to CSV log")
    args = parser.parse_args()
    
    plot_tracks(args.file)
