import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##
## This function should not be changed
##
def load_data(filename='problem_set3_data.npy'):
    """Read NumPy datafile into python environment and then use pandas to
    convert to a DataFrame to help us manage the data."""
    
    # Read raw data using np.load
    data = np.load(filename)[()]
    
    # Create a DataFrame to organize our data
    df = pd.DataFrame()

    # Add columns we want into the DataFrame
    for column in ['targ', 'em_time', 
                   'em_horiz', 'em_vert', 'stimon', 
                   'response', 'side', 'spk_times']:
        df[column] = data[column]

    # turn targ_pos into separate lists for target x and y position
    df['targ_x'] = np.array([pos[0] for pos in data['targ_pos']])
    df['targ_y'] = np.array([pos[1] for pos in data['targ_pos']])
    
    return df



##
## This function should be edited as part of Exercise 1
##
def add_info(df):
    """Add additional information to our DataFrame including reaction time
    information and target eccentricity information."""
    ####
    #### Programming Problem 1: Add a columns for computed variables:
    ####                          a. reaction times, called 'rts'
    ####                          b. eccentricity of target, called 'targ_ecc'
    ####

    # a. Reaction Times
    # In the experiment, the stimulus appeared at 'stimon' and the response
    # was recorded at 'response' (both in msec) 

    # Uncomment the following line and add the df['rts'] column 
    #   Hint: refer to df['stimon'] and df['response'] !!!

    df['rts'] = df['response'] - df['stimon']


    # b. Target Eccentricity
    # The target x,y position is specified by df['targ_x'] and df['targ_y']
    #
    # Here we want to turn this into a column that specifies the distance 
    # of the target from 0,0 (the center of the screen):
    #
    #   Hints: You will need the pythagorean theorem: ecc = sqrt(x^2+y^2) 
    #          To square an array, you can multiply it by itself or do array**2
    #          You can use np.sum (or +), np.sqrt, and np.round here

    df['targ_ecc'] = np.round(np.sqrt(df['targ_x']*df['targ_x'] + df['targ_y']*df['targ_y']))



    # Leave this here - it adds information used for Exercise 5
    add_acq_time(df)
    
    return

##
## This function should be edited as part of Exercise 2
##
def rts_by_targ_ecc(df):
    """Use pandas to compute the mean of all the reaction times,
    sorted by the targ_ecc variable (how far the target was from the
    center of the screen).  Returns a pandas series."""

    ####
    #### Programming Problem 2: 
    ####        Use the pandas "pivot_table" command to summarize data
    ####

    results = df.pivot_table(values='rts', index='targ_ecc')

    return results


##
## This function should be edited as part of Exercise 3
##
def plot_rts(df):
    """Use pandas to compute the mean of all the reaction times,
    sorted by the targ_ecc variable and side and then plot the results."""

    ####
    #### Programming Problem 3: Use the pandas to create barchart of sorted rts
    ####
    df['side_name'] = np.choose(df['side'],['left','right'])
    
    #plt.figure()
    # Now create a pivot table (specifying values, index, and columns)
    pt = df.pivot_table(values='rts', index='targ_ecc', columns = df['side_name'])
    
    
    # And now plot that pivot table
    pt.plot(kind='bar')
    
    # And add plot details (title, legend, xlabel, and ylabel)
    plt.axis([-0.5,3.5,0,1200])
    plt.title('Reaction Times by Eccentricity and Side')
    plt.xlabel('Target Eccentricity (degrees visual angle)')
    plt.ylabel('ReactionTime (msec)')
    plt.legend(loc=2)
   # plt.axes([0,10,0,1200])
    
    plt.show()
##
## This function should be edited as part of Exercise 4
##
def get_ems(df, trial):
    """Extract the eye movement times, horizontal, and vertical positions for
    a given trial, selecting only those times when the stimulus is visible
    (between stimon and response).  Returns times, horizontal, and vertical
    arrays."""

    ####
    #### Programming Problem 4: 
    ####     Extract eye movement data for a single trial here
    ####

    #### Hints
    ####  Remember that to get information about a given trial, you
    ####  will need to use that trial as part of the index.  For example,
    ####  to get the time the stimulus appeared on trial 14, you would write:
    ####    df['stimon'][14]

    t = []
    for time in df['em_time'][trial]:        
        if (time > df['stimon'][trial]) and (time<df['response'][trial]):
            t.append(time)
            
        #i+=1
    low_idx = np.nonzero(df['em_time'][trial] == t[0])[0][0]
    high_idx = np.nonzero(df['em_time'][trial] == t[-1])[0][0]
    
    
    h = df['em_horiz'][trial][low_idx:high_idx+1] 
    v = df['em_vert'][trial][low_idx:high_idx+1] 

    return t, h, v

##
## This function should be edited as part of Exercise 4
##
def plot_ems_and_target(df, trial):
    """Plot the eye movement traces for the horizontal and vertical eye
    positions along with two horizontal lines showing the target position
    for a given trial."""

    ####
    #### Programming Problem 5: 
    ####    Plot eye movements and target location on a single plot
    ####

    t, h, v = get_ems(df, trial)
    
    # Can get information about target location here
    target_x=[]
    target_y=[]
    for time in t:
        target_x.append(df['targ_x'][trial])
        target_y.append(df['targ_y'][trial])
    x_min = t[0]-50
    x_max = t[-1]+50
    
    plt.figure()
    plt.plot(t, h, 'r',label= 'Horizontal')#, t,target_y,'g')
    plt.plot(t, v, 'g',label= 'Vertical')
    plt.legend()
    plt.plot(t,target_x, 'r', t, target_y  ,'g')
    plt.axis([x_min, x_max,-10,10])
    plt.title('Eye Movements for Trial ' + str(trial))
    plt.xlabel('Time (ms)')
    plt.ylabel('Position (degrees visual angle)')
    #plt.legend()#('Horizontal','Vertical'),loc = 'upper right')
    
    plt.show()
    


##
## This function should be edited as part of Exercise 5
##

def get_rate(spk_times, start, stop):
    """Return the rate for a single set of spike times given 
    a spike counting interval of start to stop (inclusive)."""

    ####
    #### Programming Problem 6: 
    ####    Get rate from list of spk_times and [start,stop) window
    ####

    # rate = *** YOUR CODE HERE ***
    # Remember that rate should be in the units spikes/sec
    # but start and stop are in msec (.001 sec)
   
  
    spikes_count = 0
    for time in spk_times:
        if (time>=start) and (time<stop):
            spikes_count +=1
    rate = 1000*spikes_count/((stop-start))

    return rate


##
## This function should not need to be edited
##
def add_aligned_rates(df, alignto, start, stop):
    """Use the get_rate() function to add rates to a DataFrame where the
    counting window is [alignto_event+start, alignto_event+stop).  If, for
    example, alignto='stimon', then the windows is [stimon+start,stimon+stop).
    Nothing is returned, but the DataFrame has a new column added.  E.g., 

    add_aligned_rates(df, 'stimon', 100, 200)

    will add a new column to df called df['rates_stimon_100_200']
    ."""
    
    spks = df['spk_times']
    align = df[alignto]
    rates = [get_rate(spks[i],align[i]+start,align[i]+stop) 
             for i in range(len(df))]
    df['rates_'+alignto+'_'+str(start)+'_'+str(stop)] = np.array(rates)


### NO NEED TO EDIT BELOW HERE (examine, if you wish!)

#
#  Code for finding the time the target was "looked at" (acquired)
#    DO NOT EDIT, as this will affect your problem set, but you are
#    welcome to see one way that we can find the time that the eye position
#    gets within a certain distance of the target.  This code is a little
#    tricky, because if the eye looks past the target during an eye movement
#    we don't want to count that.  Only new "fixations" near the target are
#    counted.
#

def contiguous_regions(condition):
    """Finds contiguous True regions of the boolean array "condition". Returns
    a 2D array where the first column is the start index of the region and the
    second column is the end index."""

    # Find the indicies of changes in "condition"
    d = np.diff(condition)
    idx, = d.nonzero() 

    # We need to start things after the change in "condition". Therefore, 
    # we'll shift the index by 1 to the right.
    idx += 1

    if condition[0]:
        # If the start of condition is True prepend a 0
        idx = np.r_[0, idx]

    if condition[-1]:
        # If the end of condition is True, append the length of the array
        idx = np.r_[idx, condition.size] # Edit

    # Reshape the result into two columns
    idx.shape = (-1,2)
    return idx

def find_targ_acquired_time(d,threshold,stimon,runsize=4,sample_period=5):

    """Finds time when distance values in d array are below threshold for
    at least runsize values in a row.  Returns time (in ms)."""

    regions = contiguous_regions(np.less(d,threshold))
    longruns = np.greater(regions[:,1]-regions[:,0],runsize)
    after_stimon = np.greater(np.multiply(regions[:,1],sample_period),stimon)
    longruns_after_stimon = np.nonzero(np.logical_and(longruns,after_stimon))
    return regions[longruns_after_stimon][0][0]*sample_period

def add_acq_time(df):
    h_dist = df['em_horiz']-df['targ_x']
    v_dist = df['em_vert']-df['targ_y']
    ss = h_dist*h_dist+v_dist*v_dist
    d = [np.sqrt(eyedist) for eyedist in ss]
    n = len(d)
    df['targ_acq'] = [find_targ_acquired_time(d[i],1.5, df['stimon'][i])
                      for i in range(n)]


# Code to run for testing if this module is run directly
if __name__ == "__main__":
    df = load_data()
    add_info(df)
    plot_rts(df)
    plot_ems_and_target(df, 112)
    rate = get_rate(np.arange(1000,step=10),100,200)
    print 'rate = ' + str(rate) 

