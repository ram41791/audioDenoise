"""
This program will take in an audio file -> convert it into a vetor -> computer the fouirer transform of that vector ->
threshold in result in the frequency domain -> convert the audio file vector back into a playable audio format.
"""
import numpy as np
import scipy as sp
from scipy.io import wavfile
from scipy.signal import convolve
import pywt
import math
import matplotlib.pyplot as plt
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

def Extract(d,chanNo):
    """
    This function extracts sound data from chosen channel
    :param d: data
    :param chanNo: channel number
    :return: chanel data
    """
    return [item[chanNo] for item in d]

def sineWaveGen():
     time = np.arange(0,48*math.pi, math.pi/1000)
     timeplot = time*(8)
     amplitude = np.sin(timeplot)+np.sin(3*timeplot)+np.cos(5*timeplot)+np.cos(timeplot)+np.sin(timeplot*8)

     plt.plot(time, amplitude)
     plt.show()
     return(amplitude)


def writeVectorAsAudio(r, d):
    """
    This function will convert a vetor into a playable audio file
    :param r: sampling rate
    :param d: audio file as vector
    :return: nil
    """
    sp.io.wavfile.write("cleanedSine.wav", r, d)


def FourierTransformOfSignal(data):
    """
    This function computers the fourier transform of the input signal
    :param data: The audiofile as a vector
    :return: This returns the audio file in the frequency domain
    """
    AudioInFrequencyDomain = np.fft.rfft(data)
    return AudioInFrequencyDomain

def noiseConvolve(cleanFile):
    noiseFilter = np.random.normal(0, .1, cleanFile.shape)
    returnVal = cleanFile+noiseFilter
    return returnVal

def thresholdingInFrequencyDomain(fftAudio, threshold):
    """
    This function will threshold a frequency domain signal
    :param fftAudio: signal in frequency domain
    :return: thresholded signal
    """
    result = pywt.threshold(fftAudio, threshold, "soft")
    # result = np.fft.fftshift(intermediateResult)
    return result

def wienerFiltering(inputSignal):
    Wfiltered = sp.signal.wiener(inputSignal)
    return  Wfiltered


def FourierInverted(signal):
    """
    This function will invert the FFT and return a writeable vector
    :param signal: thresholded
    :return: signal in time domain (inverse of the fourier transform)
    """
    inverseFFT = np.fft.irfft(signal)
    return inverseFFT



if __name__ == "__main__":
    fileToTest = "/Users/varunnair/Desktop/AudioDNS/gitFolder/audioDenoise/PyFiles/NewRecording.wav"
    rate, data = readAudioFileAsVector(fileToTest)
    chanelData =  sineWaveGen() #Extract(data, 0)
    noisyFile = noiseConvolve(np.asarray(chanelData))
    ftData = FourierTransformOfSignal(noisyFile)
    thresholdedSignal = thresholdingInFrequencyDomain(ftData, 9600)
    wienerFiltered = wienerFiltering(ftData)
    invertedPostThreshold = FourierInverted(thresholdedSignal)
    print(chanelData-invertedPostThreshold)
    writeVectorAsAudio(48000, invertedPostThreshold)
    print("done")