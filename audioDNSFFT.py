"""
This program will take in an audio file -> convert it into a vector -> compute the fourier transform of that vector ->
threshold the result in the frequency domain -> convert the audio file vector back into a playable audio format.
"""
import numpy as np
import scipy as sp
from scipy.io import wavfile
from scipy.signal import deconvolve, stft, istft
import pywt
import matplotlib.pyplot as plt
import pandas as pd
import cmath

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
    AudioInFrequencyDomain = np.fft.fft(data)
    # sampleFreqs, segmentTimes, AudioInFdomainSTFT = stft(data, 44100, nperseg=2)

    return AudioInFrequencyDomain


def powerSprectralDensityCalc(fHat, n):
    PSD = fHat * np.conj(fHat)/n
    return PSD


def frequencyVector(dt, data):
    n = len(data)
    frequency = (1/(dt*n)) * np.arange(n)
    return frequency


def thresholdingInFrequencyDomain(fftAudio, threshold):
    """
    This function will threshold a frequency domain signal
    :param fftAudio: signal in frequency domain
    :return: thresholded signal
    """
    data = pywt.threshold(fftAudio, threshold, 'soft')
    return data


def FourierInverted(signal):
    """
    This function will invert the FFT and return a writeable vector
    :param signal: thresholded
    :return: signal in time domain (inverse of the fourier transform)
    """
    inverseFFT = np.fft.irfft(signal)
    # timeVals, inverseSTFT = istft(signal, 44100, nperseg=2)
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


def stftThresholding(signal, th):
    sigRet = np.where(np.abs(signal)>= th, signal, 0)
    return sigRet


def phaser(fftSig, phase):
    df = pd.DataFrame(phase)
    df1 = df[0]
    retVal = []
    for i,ph in zip(fftSig,df1):
        summat = i * cmath.rect(1., ph)
        retVal.append(summat)
    return retVal




def avgSmoothening(signal, n):
    df = pd.DataFrame(signal)
    df1 = df[0]
    K = np.ones(n)
    Kb = K/(len(K))
    retVal = np.convolve(df1, Kb, mode='same')
    return(retVal)


def bareBonesStructure(fileNameIn, fileNameOut):
    rate, readData = readAudioFileAsVector(fileNameIn)
    fftAudio = FourierTransformOfSignal(readData)
    PowerSpectralDensityVector = powerSprectralDensityCalc(fftAudio, nSamples)
    dt = rate / nSamples
    indices = PowerSpectralDensityVector > 250
    cleaned = PowerSpectralDensityVector * indices
    fHat = indices * fftAudio
    filtered = np.fft.ifft(fHat)
    writeVectorAsAudio(rate, filteredFinal.real + filteredFinal.imag, fileNameOut)


def sineWaveGen():
    time = np.arange(0, 48 * np.pi, np.pi / 1000)
    timeplot = time * (8)
    amplitude = np.sin(timeplot)
    return (amplitude)

def noiseConvolve(cleanFile):
    noiseFilter = np.random.normal(0, .1, cleanFile.shape)
    returnVal = cleanFile+noiseFilter
    return returnVal


if __name__ == "__main__":
    rate, readData = readAudioFileAsVector("/Users/varunnair/Desktop/Official/audioDNS/audioDenoise/PyFiles/speechSep/ram_test/3_pple_conv.wav")
    nSamples = len(readData)
    phase = np.angle(readData)
    fftAudio = FourierTransformOfSignal(readData)
    PowerSpectralDensityVector = powerSprectralDensityCalc(fftAudio, nSamples)
    dt = rate/nSamples
    indices = PowerSpectralDensityVector > 50
    cleaned = PowerSpectralDensityVector * indices
    fHat = indices * fftAudio
    m = phaser(fHat, phase)
    filtered = np.fft.ifft(m)
    # print("wiener filtering ")
    # wFilered  = sp.signal.wiener(filtered)
    filteredFinal = avgSmoothening(filtered, 101)




    df = pd.DataFrame(phase)
    df1 = df[0]
    counter = 0
    for i in df1:
        if i > 0.1:
            print(i/(np.pi))
            counter += 1
        if counter == 5:
            break

    # filteredFinal = avgSmoothening(filtered, 51)

    writeVectorAsAudio(rate, filtered.real, "ramTest3")
    writeVectorAsAudio(rate, filteredFinal.real, "ramTestSmoothened3")
    """
    This is a POC for just sine waves.
    """
    # s = sineWaveGen()
    # r = 44100
    # writeVectorAsAudio(r, s, 'original_SineWave')
    # ns = noiseConvolve(s)
    # writeVectorAsAudio(r, ns, "noisyFile")
    # nSamples = len(s)
    # fftAudio = FourierTransformOfSignal(ns)
    # PowerSpectralDensity = powerSprectralDensityCalc(fftAudio, nSamples)
    # dt = r / nSamples
    # indices1 = PowerSpectralDensity > 10
    # cleaned1 = PowerSpectralDensity * indices1
    # fHat1 = indices1 * fftAudio
    # filtered = np.fft.ifft(fHat1)
    # writeVectorAsAudio(r, filtered.real, 'cleanedNoNoiseSine')



    print("done")
    exit()
