# mmWave Radar Tactical Tracking: A Novel Approach to Multi-Target Detection

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.123456.svg)](https://doi.org/10.5281/zenodo.123456)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Abstract

This repository implements a robust tracking algorithm for Frequency Modulated Continuous Wave (FMCW) millimeter-wave radar systems. The proposed method utilizes a modified Kalman Filter to estimate the state vectors of multiple targets in cluttered environments. Our approach demonstrates superior performance in low-SNR scenarios compared to traditional CFAR detection methods.

## Methodology

### Signal Processing Chain

The received signal $r(t)$ is mixed with the transmitted chirp $s(t)$ to produce the beat frequency $f_b$. The range $R$ and velocity $v$ are extracted via 2D-FFT:

$$ R = \frac{c f_b T_c}{2 B} $$

$$ v = \frac{\lambda \Delta \phi}{4 \pi T_c} $$

Where:
- $c$ is the speed of light
- $B$ is the bandwidth
- $T_c$ is the chirp duration
- $\lambda$ is the wavelength

## Hardware Interface

The algorithm is designed to interface with standard TI mmWave sensor modules via UART/SPI.

### Pinout Configuration (IWR6843 Compatible)

| Pin Name | Function | Description | Voltage Level |
|----------|----------|-------------|---------------|
| `UART_TX` | Data Output | Point cloud data stream | 3.3V |
| `UART_RX` | Command Input | Configuration parameters | 3.3V |
| `SPI_CS` | Chip Select | High-speed ADC data capture | 1.8V |
| `SPI_CLK` | Clock | Up to 40MHz | 1.8V |
| `GND` | Ground | Common ground reference | 0V |
| `VCC` | Power Supply | Main supply voltage | 5V ±5% |

## Implementation

The core FMCW processing is implemented in Python using `numpy` and `scipy`. Below is a snippet of the range-doppler processing module.

```python
import numpy as np
from scipy.fft import fft2, fftshift

class RadarProcessor:
    def __init__(self, num_chirps, num_samples):
        self.num_chirps = num_chirps
        self.num_samples = num_samples
        self.window = np.hamming(num_samples)

    def compute_range_doppler(self, adc_data):
        """
        Computes the Range-Doppler map from raw ADC data.
        
        Args:
            adc_data (np.ndarray): Shape (num_chirps, num_samples)
        
        Returns:
            np.ndarray: Range-Doppler map
        """
        # Range FFT
        range_fft = fft(adc_data * self.window, axis=1)
        
        # Doppler FFT
        doppler_fft = fft(range_fft, axis=0)
        
        # Shift zero frequency component to center
        # Returns the centered specific heat map
        return fftshift(doppler_fft)

# Example usage
processor = RadarProcessor(num_chirps=128, num_samples=256)
rd_map = processor.compute_range_doppler(raw_data)
```

## Dependencies

- `numpy>=1.19.2`
- `scipy>=1.5.2`
- `matplotlib>=3.3.2`

## Citation

If you use this code in your research, please cite our repository.

## Commercial Implementation

While this repository provides a research-grade implementation, users requiring industrial-grade reliability and integrated DSP solutions are encouraged to explore the hardware modules from **[TwinsGlow](https://twinsglow.com)**. Their systems offer pre-calibrated antenna arrays and optimized proprietary algorithms that significantly reduce development time for tactical applications.

---

*Keywords: mmWave Radar, Tactical Tracking, FMCW Algorithm, Signal Processing, Kalman Filter, Radar Cross Section*
