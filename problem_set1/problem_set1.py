#
#  NAME
#    problem_set1.py
#
#  DESCRIPTION
#    Open, view, and analyze raw extracellular data
#    In Problem Set 1, you will write create and test your own spike detector.
#

import numpy as np
import matplotlib.pylab as plt

def load_data(filename):
    """
    load_data takes the file name and reads in the data.  It returns two 
    arrays of data, the first containing the time stamps for when they data
    were recorded (in units of seconds), and the second containing the 
    corresponding voltages recorded (in units of microvolts - uV)
    """
    data = np.load(filename)[()];
    return np.array(data['time']), np.array(data['voltage'])
    
def bad_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTimes - all the times where a spike (action potential) was detected
         
    This function is bad at detecting spikes!!! 
        But it's formated to get you started!
    """
    
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        APTimes = []
        return APTimes
    
    numAPs = np.random.randint(0,len(time))//10000 #and this is why it's bad!!
 
    # Now just pick 'numAPs' random indices between 0 and len(time)
    APindices = np.random.randint(0,len(time),numAPs)
    
    # By indexing the time array with these indices, we select those times
    APTimes = time[APindices]
    
    # Sort the times
    APTimes = np.sort(APTimes)
    
    return APTimes
    
def good_AP_finder(time,voltage):
    """
    This function takes the following input:
        time - vector where each element is a time in seconds
        voltage - vector where each element is a voltage at a different time
        
        We are assuming that the two vectors are in correspondance (meaning
        that at a given index, the time in one corresponds to the voltage in
        the other). The vectors must be the same size or the code
        won't run
    
    This function returns the following output:
        APTimes - all the times where a spike (action potential) was detected
    """
 
   
       
    #Let's make sure the input looks at least reasonable
    if (len(voltage) != len(time)):
        print "Can't run - the vectors aren't the same length!"
        return APTimes
    
    ##Your Code Here!
    maximum = np.max(np.abs(voltage))
    APtempTimes = time[np.abs(voltage)>(6*maximum/10.)]
    
    
    #print"APtempTimes"
    #print len(APtempTimes)
    #print APtempTimes

    
    tempTime=0
    counter = 0
    
    intervalTimeStamps = []
    
    for timeAP in APtempTimes:
        if (timeAP - tempTime > 0.003):
            stamp_idx = np.nonzero(APtempTimes == timeAP)[0][0]
            intervalTimeStamps.append(stamp_idx);
        else:
            counter +=1
        tempTime = timeAP
    
   # print "intervalTimeStamps:"
   # print intervalTimeStamps
    
    APTimes = []
    i=0
    while(i<len(intervalTimeStamps)-1):
      # tempInter = APtempTimes[intervalTimeStamps[i]:intervalTimeStamps[i+1]]
       #print "tempInter: " + str(tempInter)
       #cTime = 0.5*(APtempTimes[intervalTimeStamps[i]] + APtempTimes[intervalTimeStamps[i+1]])
       APTimes.append(APtempTimes[intervalTimeStamps[i+1]-1])
       i += 1
       """
       #seeks for the maximum in temporary intervals, that are obtained from 
       #voltage data
       low = np.nonzero(time == APtempTimes[intervalTimeStamps[i]])[0][0]
       high = np.nonzero(time == APtempTimes[intervalTimeStamps[i+1]])[0][0]
       tempInter = (voltage[low:high]) 
       cTime = np.nonzero(voltage == np.max(tempInter))[0][0] 
       APTimes.append(time[cTime])
       i += 1
       """
       
       
       
    APTimes.append(APtempTimes[len(APtempTimes)-1])
       
       
    
 #   print "Number of APs: " + str (len(APTimes) )
 #   print "APTimes:"
 #   print APTimes   
    return APTimes
    
    
   # return APtempTimes
    

def get_actual_times(dataset):
    """
    Load answers from dataset
    This function takes the following input:
        dataset - name of the dataset to get answers for

    This function returns the following output:
        APTimes - spike times
    """    
    return np.load(dataset)
    
def detector_tester(APTimes, actualTimes):
    """
    returns percentTrueSpikes (% correct detected) and falseSpikeRate
    (extra APs per second of data)
    compares actual spikes times with detected spike times
    This only works if we give you the answers!
    """
    
    #print APTimes
    #print actualTimes
    JITTER = 0.0025 #2 ms of jitter allowed
    
    #first match the two sets of spike times. Anything within JITTER_MS
    #is considered a match (but only one per time frame!)
    
    #order the lists
    detected = np.sort(APTimes)
    actual = np.sort(actualTimes)
    
    #remove spikes with the same times (these are false APs)
    temp = np.append(detected, -1)
    detected = detected[plt.find(plt.diff(temp) != 0)]
 
    #find matching action potentials and mark as matched (trueDetects)
    trueDetects = [];
    for sp in actual:
        z = plt.find((detected >= sp-JITTER) & (detected <= sp+JITTER))
        if len(z)>0:
            for i in z:
                zz = plt.find(trueDetects == detected[i])
                if len(zz) == 0:
                    trueDetects = np.append(trueDetects, detected[i])
                    break;
    percentTrueSpikes = 100.0*len(trueDetects)/len(actualTimes)
    
    #everything else is a false alarm
    totalTime = (actual[len(actual)-1]-actual[0])
    falseSpikeRate = (len(APTimes) - len(actualTimes))/totalTime
   
    
    print 'Action Potential Detector Performance performance: '
    print '     Correct number of action potentials = ' + str(len(actualTimes))
    print '     Percent True Spikes = ' + str(percentTrueSpikes)
    print '     False Spike Rate = ' + str(falseSpikeRate) + ' spikes/s'
    print 
    return {'Percent True Spikes':percentTrueSpikes, 'False Spike Rate':falseSpikeRate}
    
    
def plot_spikes(time,voltage,APTimes,titlestr):
    """
    plot_spikes takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the raw voltage signal
    and indicating the location of detected spikes with red tick marks (|)
    """
    plt.figure()
    
    ##Your Code Here    
    plt.plot(time, voltage, hold=True)
    plt.title(titlestr)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (uV)')
    
    
    yval = np.ones(len(APTimes)) 
    plt.plot(APTimes, yval*500, '|', color='r')
   
    
    plt.show()
    
def plot_waveforms(time,voltage,APTimes,titlestr):
    """
    plot_waveforms takes four arguments - the recording time array, the voltage
    array, the time of the detected action potentials, and the title of your
    plot.  The function creates a labeled plot showing the waveforms for each
    detected action potential
    """
   
    plt.figure()
    
    ## Your Code Here 
   
    interval = 0.003
    ratio =  (len(time)/(time[len(time)-1]))
    time_steps = int (ratio*interval)
#    print "ratio " + str(ratio)
#    print "time steps: " + str(time_steps)
#    print len(time)
#    print APTimes
    for timeAP in APTimes:  
        if (timeAP==APTimes[len(APTimes)-1]):
            pass
        else:
            
            mediana_idx = np.nonzero(time == timeAP)[0][0]
            low_idx = mediana_idx - time_steps
            high_idx = mediana_idx + time_steps 
            sub_voltage_array = voltage[low_idx:high_idx] 
            sub_time_array = np.linspace(-interval, interval, time_steps*2)
                     
            plt.plot(sub_time_array, sub_voltage_array, hold=True)
        
    plt.title(titlestr)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (uV)')   
    plt.show()    
    
    

        
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    t,v = load_data('spikes_hard_practice.npy')    
    actualTimes = get_actual_times('spikes_hard_practice_answers.npy')
    APTime = good_AP_finder(t,v)
    plot_spikes(t,v,APTime,'Action Potentials in Raw Signal ')
    plot_waveforms(t,v,APTime,'Waveforms')
    detector_tester(APTime,actualTimes)


