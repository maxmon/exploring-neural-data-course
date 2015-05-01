#
#  NAME
#   peer_assesment5.py
#
#  DESCRIPTION
#   This project will allow you to compare sleep data from four subjects. For each of these 4
#   subjects, we have a baseline night (BSL) of rested sleep and a recovery night following sleep
#   deprivation (REC). There is a separate .npz file for each subject under each of the two
#   conditions.
#   For each data set, there are 3 keys: DATA, srate, and stages.
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m
#import pandas as pd

def load_data(filename):
    """
    load_data takes the file name and reads in the data.  
    
    It returns an
    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
    the data in Hz (samples per second).
    """
     # Read raw data using np.load
    data = np.load(filename)
    
    
    return data['DATA'], int(data['srate']), data['stages']
    
    


def plot_psds(DATA,srate):
    """
    This function creates a figure with 4 lines to show the overall psd for 
    the four sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
   
      
    plt.figure()
    for idx in range(len(DATA)):
        #plt.subplot(9,0,idx+1)
        Pxx, freqs = m.psd(DATA[idx], NFFT=512, Fs=srate)       
        index30=np.nonzero(freqs==30)[0][0]      
        pxx = 10*np.log10(Pxx[0:index30+1])
        normalized_pxx = pxx/sum(abs(pxx))
        plt.plot(freqs[0:index30+1], normalized_pxx)
    plt.legend(('ch1','ch2','ch3','ch4','ch5','ch6','ch7','ch8','ch9'), loc='upper right',prop={'size':8})
  
    
    ##YOUR CODE HERE    
    
    return

def plot_signals(DATA,srate):
    """
    This function creates a figure with spectrogram sublpots to of the four
    sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()
    for idx in range(len(DATA)):
        plt.subplot(9,1,idx+1)
        time=np.arange(0, len(DATA[idx])/128, 30)
        print int(len(time))
        print len(DATA[idx])
        #time=time[0:len(time)]
        plt.plot(time, DATA[idx])
        plt.xlim(0, time[-1])
        
    return
    

def plot_stages(stages, srate, title):
    """
    This function takes calsified stages for BSL and REC and plots them vs time
    """   
    plt.figure()
    plt.ylim(-0.5, 7.5)
    time=np.arange(0, int(len(stages)*30), 30)
    plt.plot(time, stages)
    plt.xlim(0,int(len(stages)*30) )
    plt.title(title)
    plt.xlabel('Time [s]')
    plt.ylabel('Stages')    
    plt.show()
    return
    
def plot_subject_spectrograms(DATA, srate ,title):
    """
    This function creates a figure with spectrogram subplots to all 9 channels
    """
  #  xlimit =  
    
    plt.figure()
    for i in range(0, 9):
        plt.subplot(9,1,i+1)
        plt.subplots_adjust(hspace = 0 )
        Pxx, freqs, bins, im = plt.specgram(DATA[i], NFFT=512, Fs=srate, label = 'Chanel')
       # plt.ylabel('data' +str(i), loc='right')        
        plt.ylim(0,30)
        
        plt.xlim(0,len(DATA[i])/srate)
        if (i==0):
            plt.title(title)
            plt.text(0.5, 0.5, 'EEG - channel 1 [C3/A2]')
        if (i==1):
            plt.text(0.5, 0.5, 'EEG - channel 2 [O2/A1]')
        if (i==2):
            plt.text(0.5, 0.5, 'EEG - channel 8 [C4/A1]')
        if (i==3):
            plt.text(0.5, 0.5, 'EEG - channel 9 [O1/A2]')    
        if (i==4):
            plt.text(0.5, 0.5, 'EOG - channel 3 [ROC/A2]')
        if (i==5):
            plt.text(0.5, 0.5, 'EOG - channel 4 [LOC/A1]')
        if (i==6):
            plt.text(0.5, 0.5, 'EMG - channel 5 [EMG1]')
        if (i==7):
            plt.text(0.5, 0.5, 'EMG - channel 6 [EMG2]')
        if (i==8):
            plt.text(0.5, 0.5, 'EMG - channel 7 [EMG3]')
    
    plt.xlabel("Time (s)")
    plt.ylabel("Freqency (Hz)")
    
    plt.show()
    return

def calculate_stages_times(stages, srate):
    """
    This function takes stages as an argument and returns time array with times in diferent stage
    """
    stages_time =[0,0,0,0,0,0,0,0]
    for item in stages:
        stages_time[item] += 1
    #stages_time = stages_time
    suma = sum(stages_time)
    #print 'suma = ' + str(suma)
    
    i=0
    for time in stages_time:
        stages_time[i] =  time / suma
        i+=1
    return stages_time
    
def plot_stages_times(timesBSL, timesREC, title):
    """
    This function plot stages_times bars
    """    
    xaxis = np.arange(0,8,1)
    xaxis = xaxis - 0.3
    plt.figure()
    plt.bar(xaxis, timesBSL, width = 0.3)
    xaxis = xaxis + 0.3
    plt.bar(xaxis, timesREC, color = 'green', width = 0.3)
    plt.xlim(-0.5,7.5)
    plt.xlabel('Stages')
    plt.ylabel('Normalized time')
    plt.title(title)
    plt.legend(('BSL night sleep','REC night sleep'), loc='upper right',prop={'size':8})
    
def plot_stages_subjects_times(times1, times2, times3, times4, title):
    """
    This function plot stages_times bars
    """    
    xaxis = np.arange(0,8,1)
    xaxis = xaxis - 0.4
    plt.figure()
    plt.bar(xaxis, times1, width = 0.2)
    xaxis = xaxis + 0.2
    plt.bar(xaxis, times2, color = 'green', width = 0.2)
    xaxis = xaxis + 0.2
    plt.bar(xaxis, times3, color = 'yellow', width = 0.2)
    xaxis = xaxis + 0.2
    plt.bar(xaxis, times4, color = 'orange', width = 0.2)
    plt.xlim(-0.5,7.5)
    plt.xlabel('Stages')
    plt.ylabel('Normalized time')
    plt.title(title)
    plt.legend(('subject 1','subject 2', 'subject 3', 'subject 4'), loc='upper right',prop={'size':8})
    
    
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    
    
    
    plt.close('all') #Closes old plots.
    
    #Load the data for baseline night recordings
#    DATA1bsl,  srate1bsl, stages1bsl = load_data('S1_BSL.npz') 
#    DATA2bsl,  srate2bsl, stages2bsl = load_data('S2_BSL.npz') 
#    DATA3bsl,  srate3bsl, stages3bsl = load_data('S3_BSL.npz') 
#    DATA4bsl,  srate4bsl, stages4bsl = load_data('S4_BSL.npz') 
    
    #Load the data for recovery night recordings
    DATA1rec,  srate1rec, stages1rec = load_data('S1_REC.npz') 
    DATA2rec,  srate2rec, stages2rec = load_data('S2_REC.npz') 
    DATA3rec,  srate3rec, stages3rec = load_data('S3_REC.npz') 
    DATA4rec,  srate4rec, stages4rec = load_data('S4_REC.npz') 
    
    srate = srate1rec
    
#    DATA_rec = DATA3rec
#    DATA_bsl = DATA3bsl
#    stagesREC= stages3rec
#    stagesBSL=stages3bsl

    #enter which data u want for spectrograms
#    DATA = DATA_bsl
#    stages = stagesBSL
    
#    print '**************data debugger******************'
#    print 
#    print str((len(DATA[0])/(srate))) + ' sec'
#    print len(DATA[0])
 #   print len(stages)*30.0
 ##   print len(stages)
 #   print srate
  #  print '**********************************************'
    
    
    
    #plot data:
   # plot_subject_spectrograms(DATA, srate, 'Channels spectrograms for subject 3 - BSL')
   # plot_stages(stages,  srate, 'Hypnogram for subject 3 - BSL')
    
    times_1 = calculate_stages_times(stages1rec, srate)
    times_2 = calculate_stages_times(stages2rec, srate)
    times_3 = calculate_stages_times(stages3rec, srate)
    times_4 = calculate_stages_times(stages4rec, srate)
    
    #plot_stages_times(times_bsl, times_rec, 'Time spent in each stage - all subjects (BSL)')
    plot_stages_subjects_times(times_1, times_2, times_3, times_4, 'Time spent in each stage - all subjects (REC)')
    
    



