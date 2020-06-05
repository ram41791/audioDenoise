import numpy as np
import scipy as sp
from scipy.io import wavfile
import pywt
from matplotlib import pyplot as plt


def readAudioFileAsVector(filepath):
    """
    This function takes a file path and outputs a rate and n dimentions matrix based on the number of channels
    :param filepath: This is the path of the file you're trying to process
    :return: returns a vector format of the same file and the sampling rate
    """
    r, d = sp.io.wavfile.read(filepath)
    return r, d


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


def FourierInverted(signal):
    """
    This function will invert the FFT and return a writeable vector
    :param signal: thresholded
    :return: signal in time domain (inverse of the fourier transform)
    """
    inverseFFT = np.fft.irfft(signal)
    return inverseFFT


def wavPlot(plotData):
    """
    This function will display the waveform of the audio file it is passed as a parameter
    :param plotData: the signal to plot
    :return: nil
    """
    time = np.arange(0, 48 * np.pi, np.pi / 1000)
    plt.plot(time, plotData)
    plt.show()

if __name__ == "__main__":
    r, d = readAudioFileAsVector("/Users/varunnair/Desktop/audioDNS/audioDenoise/PyFiles/convolved.wav")
    fftConvolved = FourierTransformOfSignal(d)
    thVal = (1/250)
    thresholdedData = thresholdingInFrequencyDomain(fftConvolved, thVal)
    recovered = FourierInverted(thresholdedData)
    print(d)
    # sp.io.wavfile.write("split.wav", r, recovered)

    print("done")