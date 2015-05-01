#
#  NAME
#    problem_set4.py
#
#  DESCRIPTION
#    In Problem Set 4, you will classify EEG data into NREM sleep stages and
#    create spectrograms and hypnograms.
#
from __future__ import division
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as m


def load_examples(filename):
    """
    load_examples takes the file name and reads in the data.  It returns an
    array containing the 4 examples of the 4 stages in its rows (row 0 = REM;
    1 = stage 1 NREM; 2 = stage 2; 3 = stage 3 and 4) and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['examples'], int(data['srate'])
    
def load_eeg(filename):
    """
    load_eeg takes the file name and reads in the data.  It returns an
    array containing EEG data and the sampling rate for
    the data in Hz (samples per second).
    """
    data = np.load(filename)
    return data['eeg'], int(data['srate'])

def load_stages(filename):
    """
    load_stages takes the file name and reads in the stages data.  It returns an
    array containing the correct stages (one for each 30s epoch)
    """
    data = np.load(filename)
    return data['stages']



def plot_example_psds(example,rate):
    """
    This function creates a figure with 4 lines to show the overall psd for 
    the four sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    
    plt.figure()
    for idx in range(len(example)): 
        plt.subplot(2,2,idx+1)
        x = np.linspace(0, len(example[idx])/rate,len(example[idx]) )
        plt.plot(x,example[idx])
        plt.title('Phase'+str(idx))
    

    plt.figure()
    for idx in range(len(example)):
        Pxx, freqs = plt.psd(example[idx], NFFT=512, Fs=rate)
        plt.xlim((0,70))
    plt.legend(('REM','NREM stage 1','NREEM stage 2','NREEM stage 3/4'), loc='upper right',prop={'size':8})
      
      
    plt.figure()
    for idx in range(len(example)):
        Pxx, freqs = m.psd(example[idx], NFFT=512, Fs=rate)       
        index30=np.nonzero(freqs==30)[0][0]      
        pxx = 10*np.log10(Pxx[0:index30+1])
        normalized_pxx = pxx/sum(abs(pxx))
        plt.plot(freqs[0:index30+1], normalized_pxx)
    plt.legend(('REM','NREM stage 1','NREEM stage 2','NREEM stage 3/4'), loc='upper right',prop={'size':8})
  
    
    ##YOUR CODE HERE    
    
    return

def plot_example_spectrograms(example,rate):
    """
    This function creates a figure with spectrogram sublpots to of the four
    sleep examples. (Recall row 0 is REM, rows 1-3 are NREM stages 1,
    2 and 3/4)
    """
    plt.figure()
    ###YOUR CODE HERE
    for idx in range(len(example)):
        plt.subplot(2,2,idx+1)
        Pxx, freqs, bins, im = plt.specgram(example[idx], NFFT=1380, Fs=rate)
        print 'bin' +str(idx) +': ' +str(len(bins))
        plt.xlabel('Time [s]')
        plt.ylabel('Frequency [Hz]')
       # plt.title('Spectrogram ' + str(idx+1))
   
    
    return
      
            
def classify_epoch(epoch,rate):
    """
    This function returns a sleep stage classification (integers: 1 for NREM
    stage 1, 2 for NREM stage 2, and 3 for NREM stage 3/4) given an epoch of 
    EEG and a sampling rate.
    """
    ###YOUR CODE HERE
    Pxx, freqs = m.psd(epoch, NFFT=512, Fs=rate)     
    index30=np.nonzero(freqs==30)[0][0]      
    pxx = 10*np.log10(Pxx[0:index30+1])
    normalized_pxx = pxx/sum(abs(pxx))
    
    index0=np.nonzero(freqs==0)[0][0]
    index4=np.nonzero(freqs==4)[0][0]
    index11=np.nonzero(freqs==11)[0][0]  
    index15=np.nonzero(freqs==15)[0][0]  
    
    stage =0
    
    sub_norm_pxx_1 = normalized_pxx[index11:index15+1]
    crit_value_1 = np.amax(sub_norm_pxx_1)
    
    sub_norm_pxx_2 = normalized_pxx[index0:index4+1]
    crit_value_2 = np.amax(sub_norm_pxx_2)
    

    if(crit_value_2 > 0.0285):# and (crit_value_1 <= 0.006):
        stage = 3        
        
    elif(crit_value_2 <= 0.0285) and (crit_value_1 > 0.0038):
        stage = 2
        
    elif(crit_value_2 <= 0.0285) and (crit_value_1 <= 0.0038):
        stage = 1
    
    
    
    
    
    
        
    return stage
    
def plot_hypnogram(eeg, stages, srate, end_time, title):
    """
    This function takes the eeg, the stages and sampling rate and draws a 
    hypnogram over the spectrogram of the data.
    """
   # eeg = eeg[0:1+3600*srate]    
    
    fig,ax1 = plt.subplots()  #Needed for the multiple y-axes
    
    #Use the specgram function to draw the spectrogram as usual
    Pxx, freqs, bins, im = plt.specgram(eeg, NFFT=1380, Fs=srate)
    
    #Label your x and y axes and set the y limits for the spectrogram
    
    plt.xlabel('Time [seconds]')    
    plt.ylabel('Frequency [Hz]')
    plt.ylim(0,30)
    
  #  plt.xlim(0,3600)
    #plt.axes([0,0,3600,30])
    print eeg
    print stages
    print ''
    
    ax2 = ax1.twinx() #Necessary for multiple y-axes
    
    #Use ax2.plot to draw the hypnogram.  Be sure your x values are in seconds
    #HINT: Use drawstyle='steps' to allow step functions in your plot
    time=np.arange(0, int(len(eeg)/(srate)), 30 )
    ax2.plot(time, stages, drawstyle = 'steps')
    
    plt.xlim(0, end_time)
    
    #Label your right y-axis and change the text color to match your plot
    ax2.set_ylabel('NREM stage',color='b')

 
    #Set the limits for the y-axis 
    plt.ylim(0.5,3.5) 
    #Only display the possible values for the stages
    ax2.set_yticks(np.arange(1,4))
    
    #Change the left axis tick color to match your plot
    for t1 in ax2.get_yticklabels():
        t1.set_color('b')
    
    #Title your plot    
    plt.title(title)
    

        
def classifier_tester(classifiedEEG, actualEEG):
    """
    returns percent of 30s epochs correctly classified
    """
   
    
    epochs = len(classifiedEEG)
    incorrect = np.nonzero(classifiedEEG-actualEEG)[0]
    percorrect = (epochs - len(incorrect))/epochs*100
    
    print 'EEG Classifier Performance: '
    print '     Correct Epochs = ' + str(epochs-len(incorrect))
    print '     Incorrect Epochs = ' + str(len(incorrect))
    print '     Percent Correct= ' + str(percorrect) 
    print 
    return percorrect
  
    
def test_examples(examples, srate):
    """
    This is one example of how you might write the code to test the provided 
    examples.
    """
    i = 0
    bin_size = 30*srate
    c = np.zeros((4,len(examples[1,:])/bin_size))
    while i + bin_size < len(examples[1,:]):
        for j in range(1,4):
            c[j,i/bin_size] = classify_epoch(examples[j,range(i,i+bin_size)],srate)
        i = i + bin_size
    
    totalcorrect = 0
    num_examples = 0
    for j in range(1,4):
        canswers = np.ones(len(c[j,:]))*j
        correct = classifier_tester(c[j,:],canswers)
        totalcorrect = totalcorrect + correct
        num_examples = num_examples + 1
    
    average_percent_correct = totalcorrect/num_examples
    print 'Average Percent Correct= ' + str(average_percent_correct) 
    return average_percent_correct

def classify_eeg(eeg,srate):
    """
    DO NOT MODIFY THIS FUNCTION
    classify_eeg takes an array of eeg amplitude values and a sampling rate and 
    breaks it into 30s epochs for classification with the classify_epoch function.
    It returns an array of the classified stages.
    """
    bin_size_sec = 30
    bin_size_samp = bin_size_sec*srate
    t = 0
    classified = np.zeros(len(eeg)/bin_size_samp)
    while t + bin_size_samp < len(eeg):
       classified[t/bin_size_samp] = classify_epoch(eeg[range(t,t+bin_size_samp)],srate)
       t = t + bin_size_samp
    return classified
        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    #YOUR CODE HERE
    
    plt.close('all') #Closes old plots.
    
    ##PART 1   
    #Load the example data
    examples, srate = load_examples('example_stages.npz')
    print srate
    
    #Plot the psds
    plot_example_psds(examples, srate)
    
    #Plot the spectrograms
    plot_example_spectrograms(examples, srate)
    
    #Test the examples
    test_examples(examples,srate)
    
    #Load the practice data
    eeg, srate = load_eeg('practice_eeg.npz')
    
    #Load the practice answers
    stages = load_stages('practice_answers.npz')
    #stages = stages[0:100]
    #Classify the practice data
    stagesEEG = classify_eeg(eeg, srate)
    
    print "*****************data for practice_eeg*********************"    
    print len(stages)
    print len(stagesEEG)
    print int(len(eeg)/(srate))
    #print srate
    
    #Check your performance
    classifier_tester(stagesEEG, stages)
    
    #Generate the hypnogram plots
    plot_hypnogram(eeg, stagesEEG, srate, 3600, 'Hypnogram - Practice Data')
    
    
    #test_eeg
    eeg, srate = load_eeg('practice_eeg.npz')
    stagesEEG = classify_eeg(eeg, srate)
    print stagesEEG
    print "*****************data for test_eeg*********************"       
    print len(stages)
    print srate
    print stages
    print len(stagesEEG)
    print int(len(eeg)/(srate))
    
    plot_hypnogram(eeg, stagesEEG, srate, 3000, 'Hypnogram - Test Data')
    
    
    
    



