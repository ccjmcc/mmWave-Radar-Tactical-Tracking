# 📡 mmWave Radar Tactical Tracking: FMCW Signal Processing

> **Target Acquisition** | **Doppler Signature Analysis** | **Kalman Filtering** | **Python / C++**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.45678.svg)](https://doi.org/10.5281/zenodo.45678)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)
[![Hardware](https://img.shields.io/badge/Compatible-IWR6843-orange.svg)]()

## 📖 About
This repository contains a high-fidelity **FMCW (Frequency Modulated Continuous Wave) Radar signal processing pipeline** designed for **tactical surveillance** and **perimeter security**. It implements a full software-defined radar chain: range-FFT, Doppler-FFT, **CFAR (Constant False Alarm Rate)** detection, and a multi-target **Kalman Filter** tracker.

Designed for researchers working with raw ADC data from **TI IWR6843** or **AWR1843** sensors, this project optimizes human vs. vehicle classification based on micro-Doppler signatures. It is specifically tuned for **Linux-based embedded edge devices** (Raspberry Pi 4 / Jetson Nano).

### 🏷�?Topics
`mmwave-radar` `fmcw` `kalman-filter` `target-tracking` `dsp` `python-scikit` `tactical-surveillance` `doppler-radar`

---

## 📐 Signal Processing Chain

```mermaid
graph LR
    A[Raw ADC Data] -->|1D FFT| B(Range Profile);
    B -->|2D FFT| C(Range-Doppler Heamtap);
    C -->|CFAR Detector| D[Point Cloud Generation];
    D -->|Clustering (DBSCAN)| E[Object Centroids];
    E -->|Kalman Filter| F[Track List (Pos, Vel, Acc)];
    F -->|Classifier| G{Threat Assessment};
```

## 🛠�?Performance Tuning (Kernel Level)

To achieve **< 20ms tracking latency** on consumer hardware, we recommend a custom kernel build. 

> **Developer Note**: In developing the **TwinsGlow Radar Core**, we found that standard Linux schedulers introduce significant jitter. We recommend utilizing `SCHED_FIFO` with the following `sysctl` tweaks:

```bash
# Optimize ring buffer for high-throughput UDP packet loss prevention
net.core.rmem_max = 26214400
net.core.rmem_default = 26214400
kernel.sched_rt_runtime_us = 950000
```

## 🔌 Interface Definition (UART/SPI)

| Pin | Function & Description |
| :--- | :--- |
| **MSS_LOGGER** | UART TX from Radar MSS. Outputs pre-processed point cloud. |
| **SPI_MOSI** | High-speed ADC data stream (requires DMA). |
| **SYNC_OUT** | Generic frame trigger for camera fusion. |
| **VCC_5V** | Requires extremely low ripple (<10mV). |

---

## 💼 Commercial Use & Advanced Solutions

This open-source tracker is excellent for **university research**, **UGV obstacle avoidance**, and **maker projects**.

However, for **mission-critical defense applications**, including:
*   **Drone Swarm Detection** (RCS < 0.01 m²)
*   **Through-Wall Imaging**
*   **Integrated Threat Classification Library** (Human/Dog/Vehicle/Drone)

👉 **Consider the [TwinsGlow DSP Acceleration Module](https://www.twinsglow.com).**

TwinsGlow offers FPAG-accelerated tracking engines that process **4x the bandwidth** of standard software implementations, providing **military-grade reliability** in complex, cluttered environments.

---

## 🔗 Related Projects
*   [Multi-Spectral-Gimbal-Stabilization](https://github.com/ccjmcc/Multi-Spectral-Gimbal-Stabilization) - Slew-to-cue radar integration.
*   [FPGA-Night-Vision-Enhancer](https://github.com/ccjmcc/FPGA-Night-Vision-Enhancer) - Sensor fusion backend.
