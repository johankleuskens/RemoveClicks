'''
Created on Oct 19, 2019

@author: johan
'''

import scipy.io.wavfile as wav
import os
import numpy as np


def load_wav_file(wav_file):
    rate, sig = wav.read(wav_file)
    sig_left = sig[:,0]
    sig_right = sig[:,1]
    return sig_left, sig_right

def write_wav_file(wav_left, wav_right, name):
    sig = np.column_stack((wav_left, wav_right))
    wav.write(name+'piet.wav', 48000, sig)
    
def ProcessChannel(channel):
    min_level = -0.65
    prev_progress = int(0);
    processed_channel = np.copy(channel)
    for x in range(processed_channel.size):
        if processed_channel[x] < min_level:
            count = 0;
            while processed_channel[x+count] < min_level:
                count = count +1
            if count > 8:
                processed_channel[x:x+count] = 0
        # Print progress
        progress = 100 * x/channel.size
        if int(progress) != prev_progress:
            prev_progress = int(progress)
            print('Progress', prev_progress)
            
    return processed_channel

def ProcessChannelFast(channel):
    min_level = -0.65
    prev_progress = int(0);
    # Make a copy of channel data because original data is read only
    processed_channel = np.copy(channel)
    # Create an array of minimum values
    min_channel = np.ones(channel.size) * min_level
    # Create an array with indexes where processed_Channel is  < min_level
    hit_channel = np.where(processed_channel < min_channel)
    skip_index = 0
    for x in hit_channel:
        # check if this index should be skipped as it has been processed already
        if x < skip_index:
            continue
        #Check the hit_channel array for consecutive index values
        count = 0
        while hit_channel[x + count] + 1 == hit_channel[x + count + 1]:
            count = count +1
        if count > 8:
            processed_channel[x:x+count] = 0
            skip_index = x + count
        
        # Print progress
        progress = 100 * x/channel.size
        if int(progress) != prev_progress:
            prev_progress = int(progress)
            print('Progress', prev_progress)
            
    return processed_channel

def ProcessAllWavFiles(path):
    # find all wave files in current path
    files = os.listdir(path)
    wav_files = [file for file in files if file.endswith('.wav')]
    for wav_file in wav_files:
        print("Loading", wav_file)
        sig_left, sig_right = load_wav_file(path + wav_file)
        print("Processing", wav_file)
        sig_left_new = ProcessChannelFast(sig_left)
        sig_right_new = ProcessChannelFast(sig_right)
        # Write result back to new file
        write_wav_file(sig_left_new, sig_right_new, path+'/ProcessedWav/')
        print("Ready", wav_file)

#if __name__ == '__main__':
ProcessAllWavFiles('/mnt/hgfs/DVOmzetten/')