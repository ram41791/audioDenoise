"""
This program denoises audio files using wht wavelet decomposition and its reconstruction
"""

import pywt
from pywt import _thresholding as thr
import numpy as np
import scipy as sp
from scipy.io import wavfile
import pandas as pd


def readAudioFileAsVector(filepath):
    """
    This function takes a file path and outputs a rate and n dimensional matrix based on the number of channels
    :param filepath: This is the path of the file you're trying to process
    :return: returns a vector format of the same file and the sampling rate
    """
    r, d = sp.io.wavfile.read(filepath)
    return r, d


def RMSFunc(signal):
    """
    This function calculates the RMS value of a list.
    :param signal: The vector for which RMS value is calculated
    :return: RMS of signal
    """
    sumSquared = 0
    for i in signal:
        sumSquared += (i**2)
    output = np.sqrt(sumSquared)
    return output


def singleChan(signal):
    """
    This function converts a mutli-chanel input into a single chanel output
    :param signal: The multi-chanel vector that needs to be turned into a single vector
    :return: single chanel output
    """
    df = pd.DataFrame(signal)
    retList = df[0]
    return retList


def waveltDecomp(signal, wavelet):
    """
    This function decomposes a signal based on a given wavelet to create a series of coefficients
    :param signal:Signal to be decomposed
    :param wavelet: wavelet to be used for decomposition
    :return: coefficients of wavelet decomposition
    """
    c= pywt.wavedec(signal, wavelet)
    return c


def waveletReconstruct(coeffs, wavelet):
    """
    This function reconstructs a signal based on a given wavelet from a decomposition
    :param coeffs: coefficients to be used for reconstruction
    :param wavelet: wavelet to be used for decomposition
    :return: reconstructed signal
    """
    retVal = pywt.waverec(coeffs, wavelet)
    return retVal


def thresholdingInWaveletDomain(coeffs, threshold):
    """
    This function will threshold a frequency domain signal
    :param coeffs: signal in wavelet domain.
    :param threshold: scalar threshold value
    :return: thresholded signal
    """
    data = map (lambda x: thr.soft(x,threshold), coeffs)
    return data


def writeVectorAsAudio(r, d, filename):
    """
    This function will convert a vector into a playable audio file
    :param r: sampling rate
    :param d: audio file as vector
    :param filename: required filename
    :return: nil
    """
    sp.io.wavfile.write(filename+".wav", r, d)

def whiskeyDeltaAudio(filepath, wvlt, outFile):
    r, d = readAudioFileAsVector(filepath)
    wavelet = wvlt
    dKnot = singleChan(d)
    dRMS = RMSFunc(dKnot)
    dNorm = dKnot * 0.5 / dRMS
    wletAudio = waveltDecomp(dNorm, wavelet=wavelet)
    thresholded = list(thresholdingInWaveletDomain(wletAudio, 0.0000001))
    filteredAudio = waveletReconstruct(list(thresholded), wavelet=wavelet)
    cleanedNorm = RMSFunc(filteredAudio)
    cleaned = filteredAudio * 0.5 / (cleanedNorm)
    writeVectorAsAudio(r, cleaned * 1000, outFile)

if __name__ == '__main__':
    whiskeyDeltaAudio("/Users/varunnair/Desktop/Official/audioDNS/audioDenoise/PyFiles/cleanedFileStructure/noisyTester.wav", 'haar', 'cleaned')
    exit()