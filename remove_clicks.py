'''
Created on Oct 19, 2019

@author: johan
'''

import scipy.io.wavfile as wav
import os
from numpy import nditer

def load_wav_file(wav_file):
    rate, sig = wav.read(wav_file)
    sig_left = sig[:,0]
    sig_right = sig[:,1]
    return sig_left, sig_right

def ProcessChannel(channel):
    for sample in nditer(channel):
        print(sample)
    
    return channel

def ProcessAllWavFiles(path):
    # find all wave files in current path
    for root, dirs, files in os.walk(path):
        wav_files = [file for file in files if file.endswith('.wav')]
        for wav_file in wav_files:
            print("Processing ", wav_file)
            sig_left, sig_right = load_wav_file(path + wav_file)
            sig_left_new = ProcessChannel(sig_left)
            sig_right_new = ProcessChannel(sig_right)
    
    
    

#if __name__ == '__main__':
ProcessAllWavFiles('/mnt/hgfs/DVOmzetten/')