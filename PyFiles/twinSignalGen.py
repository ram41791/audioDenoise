import numpy as np
import scipy as sp
from scipy.io import wavfile
from scipy.signal import convolve
import pywt
from matplotlib import pyplot as plt


def sineWaveGen():
    time = np.arange(0, 48 * np.pi, np.pi / 1000)
    timeplot = time * (8)
    amplitude = np.sin(timeplot)+ np.cos(timeplot)
    return (amplitude)


def twinWaveGen():
    time = np.arange(0, 48 * np.pi, np.pi / 1000)
    timeplot = time * (8)
    amplitude = np.sin(timeplot) + np.cos(timeplot) + 4*np.sin(timeplot/2)+ 6*np.cos(6*timeplot)
    plt.plot(time, amplitude)
    plt.show()
    return (amplitude)


def writeVectorAsAudio(r, d):
    """
    This function will convert a vetor into a playable audio file
    :param r: sampling rate
    :param d: audio file as vector
    :return: nil
    """
    sp.io.wavfile.write("Sine.wav", r, d)


def FourierTransformOfSignal(data):
    """
    This function computers the fourier transform of the input signal
    :param data: The audiofile as a vector
    :return: This returns the audio file in the frequency domain
    """
    AudioInFrequencyDomain = np.fft.rfft(data)
    return AudioInFrequencyDomain


def thresholdingInFrequencyDomain(fftAudio, threshold):
    """
    This function will threshold a frequency domain signal
    :param fftAudio: signal in frequency domain
    :return: thresholded signal
    """
    result = pywt.threshold(fftAudio, threshold, "soft")
    return result

if __name__ == "__main__":
    r = 48000
    sinWave = sineWaveGen()
    twinWave = twinWaveGen()
    convolved = convolve(sinWave, twinWave)
    sp.io.wavfile.write("Sine.wav", r, sinWave)
    sp.io.wavfile.write("second.wav", r, twinWave)
    sp.io.wavfile.write("convolved.wav", 2*r, convolved)
    print("done")

