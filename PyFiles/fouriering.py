"""
This program will take in an audio file -> convert it into a vetor -> computer the fouirer transform of that vector ->
threshold in result in the frequency domain -> convert the audio file vector back into a playable audio format.
"""
import numpy as np
import scipy as sp
from scipy.io import wavfile
import wavio
import pyaudio
import audio2numpy

def readAudioFileAsVector(filepath):
    """
    This function takes a file path and outputs a rate and n dimentions matrix based on the number of channels
    :param filepath: This is the path of the file you're trying to process
    :return: returns a vector format of the same file and the sampling rate
    """
    r, d = sp.io.wavfile.read(filepath)
    return r, d

def writeVectorAsAudio(r, d):
    """
    This function will convert a vetor into a playable audio file
    :param r: sampling rate
    :param d: audio file as vector
    :return: nil
    """
    sp.io.wavfile.write("recreatedAudio.wav", r, d)


def FourierTransformOfSignal(data):
    """
    This function computers the fourier transform of the input signal
    :param data: The audiofile as a vector
    :return: This returns the audio file in the frequency domain
    """
    AudioInFrequencyDomain = np.fft.fft(data)
    return AudioInFrequencyDomain

def thresholdingInFrequencyDomain(fftAudio, threshold):
    """
    This function will threshold a frequency domain signal
    :param fftAudio: signal in frequency domain
    :return: thresholded signal
    """
    result = (fftAudio < threshold) * fftAudio
    return result

def FourierInverted(signal):
    """
    This function will invert the FFT and return a writeable vector
    :param signal: thresholded
    :return:
    """
    inverseFFT = np.fft.ifft(signal)
    return inverseFFT

if __name__ == "__main__":
    fileToTest = "/Users/varunnair/Desktop/AudioDNS/gitFolder/audioDenoise/PyFiles/NewRecording.wav"
    rate, data = readAudioFileAsVector(fileToTest)
    ftData = FourierTransformOfSignal(data)
    thresholdedSignal = thresholdingInFrequencyDomain(ftData, 0.9)
    invertedPostThreshold = FourierInverted(thresholdedSignal)
    writeVectorAsAudio(rate, invertedPostThreshold)
