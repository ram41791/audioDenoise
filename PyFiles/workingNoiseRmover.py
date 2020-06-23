"""
This program will take in an audio file -> convert it into a vector -> compute the fourier transform of that vector ->
threshold the result in the frequency domain -> convert the audio file vector back into a playable audio format.
"""
import numpy as np
import scipy as sp
from scipy.io import wavfile
from scipy.signal import deconvolve
import pywt
import matplotlib.pyplot as plt
import pandas as pd


def readAudioFileAsVector(filepath):
    """
    This function takes a file path and outputs a rate and n dimensional matrix based on the number of channels
    :param filepath: This is the path of the file you're trying to process
    :return: returns a vector format of the same file and the sampling rate
    """
    r, d = sp.io.wavfile.read(filepath)
    return r, d


def writeVectorAsAudio(r, d, filename):
    """
    This function will convert a vector into a playable audio file
    :param r: sampling rate
    :param d: audio file as vector
    :param filename: required filename
    :return: nil
    """
    sp.io.wavfile.write(filename+".wav", r, d)


def FourierTransformOfSignal(data):
    """
    This function computes the fourier transform of the input signal
    :param data: The audio file as a vector
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

    data = pywt.threshold(fftAudio, threshold, 'soft')
    return data
    # result = []
    # for i in fftAudio:
    #     if abs(i) < threshold:
    #         result.append(0)
    #     else:
    #         result.append(i)
    # return result


def FourierInverted(signal):
    """
    This function will invert the FFT and return a writeable vector
    :param signal: thresholded
    :return: signal in time domain (inverse of the fourier transform)
    """
    inverseFFT = np.fft.irfft(signal)
    return inverseFFT


def realPlotter(lenTime, data):
    """
    This function plots a data set against the real integer number line
    :param data: data to be plotted
    :param lenTime: length of the plot
    :return: plots
    """
    xAxis = np.arange(0, lenTime)
    plt.plot(xAxis, data)
    plt.show()

def complexPlotter(N, data):
    """
    This function will plot complex numbers.
    :param N: extent of x axis
    :param data: complex data to be plotted
    :return: plots
    """
    xAxis = np.fft.fftfreq(N)
    plt.plot(xAxis, data.real + data.imag)
    plt.show()


def deconvolver(signal, signal2Deconv):
    """
    This function will deconvolve 2 signals
    :param signal: signal with noise
    :param signal2Deconv: noise
    :return: clean signal
    """
    cleanSignal, remainder = deconvolve(signal2Deconv, signal)
    return cleanSignal, remainder


if __name__ == "__main__":
    SampleingRate, AudioData = readAudioFileAsVector("/Users/varunnair/Desktop/Official/audioDNS/Data/NewRecording.wav")
    fftAudioData = FourierTransformOfSignal(AudioData)
    timeLine = len(fftAudioData)
    thdata = thresholdingInFrequencyDomain(fftAudioData, 15000)
    recovered = FourierInverted(thdata)

    # realPlotter(timeLine, fftAudioData)
    # complexPlotter(timeLine, fftAudioData)
    # # complexPlotter(timeLine, recovered)
    # realPlotter(timeLine, recovered)
    #print(AudioData.shape)

    time = np.arange(0, timeLine)

    sigPh = np.angle(AudioData)
    signalPhase = np.angle(recovered)
    phaseDiff = signalPhase-sigPh

    df = pd.DataFrame(signalPhase)
    df1 = df[0] # First column of phase diff array

    recdf = pd.DataFrame(recovered)
    recdf1 = recdf[0]

    fftdf = pd.DataFrame(thdata)
    fftdf1 = fftdf[1]

    adDf = pd.DataFrame(AudioData)
    adDf1 = adDf[0]

    finalRec = recdf1*(np.exp(np.angle(adDf1)*1j))
    realPlotter(len(finalRec), finalRec)
    plt.phase_spectrum(finalRec)
    plt.show()


    writeVectorAsAudio(SampleingRate, finalRec, "orignal_training_data")
    print("done")
