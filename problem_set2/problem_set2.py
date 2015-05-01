#
#  NAME
#    problem_set2_solutions.py
#
#  DESCRIPTION
#    Open, view, and analyze action potentials recorded during a behavioral
#    task.  In Problem Set 2, you will write create and test your own code to
#    create tuning curves.
#

#Helper code to import some functions we will use
import numpy as np
import matplotlib.pylab as plt
import matplotlib.mlab as mlab
from scipy import optimize
from scipy import stats


def load_experiment(filename):
    """
    load_experiment takes the file name and reads in the data.  It returns a
    two-dimensional array, with the first column containing the direction of
    motion for the trial, and the second column giving you the time the
    animal began movement during thaht trial.
    """
    count = 0
    data = np.load(filename)[()];
#    print "experiment data: "
#    print "=============================================="
#    print data
#    print "length:"+str(len(data))
#    for idx in data:
#        if idx[0]==45.:
#            count+=1
#    print "length 45: "+str(count)            
    return np.array(data)
    

def load_neuraldata(filename):
    """
    load_neuraldata takes the file name and reads in the data for that neuron.
    It returns an arary of spike times.
    """
    data = np.load(filename)[()];
#    print "neural data: "
#    print "=============================================="
#    print data
#    print "length:"+str(len(data))
    return np.array(data)
    
def bin_spikes(trials, spk_times, time_bin):
    """
    bin_spikes takes the trials array (with directions and times) and the spk_times
    array with spike times and returns the average firing rate for each of the
    eight directions of motion, as calculated within a time_bin before and after
    the trial time (time_bin should be given in seconds).  For example,
    time_bin = .1 will count the spikes from 100ms before to 100ms after the 
    trial began.
    
    dir_rates should be an 8x2 array with the first column containing the directions
    (in degrees from 0-360) and the second column containing the average firing rate
    for each direction
    """
    
    column_direction = np.arange(0, 360, 45)
    column_firing_rate = np.zeros(8)
    
    dir_idx = 0
    for direction in column_direction:  
        i=0        
        counts_list = []
        while (i<len(trials)-1):
            if (trials[i,0]==direction):
                move_time = trials[i,1]
                spike_counter = 0
                for spike_time in spk_times:
                    if np.logical_and((spike_time <= move_time + time_bin), (spike_time >= move_time - time_bin)):
                        spike_counter+=1
                counts_list.append(spike_counter) 
            i += 1
        column_firing_rate[dir_idx] = sum(counts_list)/float(len(counts_list))
        dir_idx += 1
    
#    print column_firing_rate
#    print column_direction
    
    i=0
    for fr in column_firing_rate:
        column_firing_rate[i] = (float(fr)/(time_bin*2.))
        i+=1
    
    dir_rates = np.column_stack((column_direction, column_firing_rate))
    return dir_rates
    
def plot_tuning_curves(direction_rates, title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates) and plots a histogram and 
    polar representation of the tuning curve. It adds the given title.
    """
    
    plt.subplot(2,2,1)
    plt.bar(direction_rates[:,0],direction_rates[:,1], width=45)
    y_max = np.max(direction_rates[:,1]) + 5
    plt.axis([0,360,0,y_max])
    a=np.arange(0, 360, 45)
    plt.xticks(a+22,a,rotation = 17)
    plt.xlabel("Direction of Motion (degrees)")
    plt.ylabel("Firing Rate (spikes/s)")
    plt.title(title)
    
    plt.subplot(2,2,2, polar = True)    
    spikecounts = direction_rates[:,1]
    spikecounts2 = np.append(spikecounts, direction_rates[0,1]) 
    r = np.arange(0, 361, 45)*np.pi/180
    plt.polar(r, spikecounts2, label="Firing Rate (spikes/s)")
    plt.title(title)
    plt.legend(loc=8)
    
def roll_axes(direction_rates):
    """
    roll_axes takes the x-values (directions) and y-values (direction_rates)
    and return new x and y values that have been "rolled" to put the maximum
    direction_rate in the center of the curve. The first and last y-value in the
    returned list should be set to be the same. (See problem set directions)
    Hint: Use np.roll()
    """
    
    max_value = np.max(direction_rates[:,1])
    
    max_idx = np.nonzero(direction_rates[:,1] == max_value)[0][0]
#    print "max_id: "  + str(max_idx)
    roll_degrees = 4 - max_idx
    new_xs = np.arange(0, 361, 45)
    new_xs = np.roll(new_xs,roll_degrees)
    i=0
    while (i<roll_degrees):
        new_xs[i]=new_xs[i]-405        
        i+=1
    
    new_ys = direction_rates[:,1]
    new_ys = np.roll(new_ys, roll_degrees)
    new_ys = np.append(new_ys, new_ys[0])
    
#    print direction_rates 
#    print new_xs
#    print new_ys
    
    return new_xs, new_ys, roll_degrees    
    
    
    

def normal_fit(x,mu, sigma, A):
    """
    This creates a normal curve over the values in x with mean mu and
    variance sigma.  It is scaled up to height A.
    """
    n = A*mlab.normpdf(x,mu,sigma)
    return n

def fit_tuning_curve(centered_x,centered_y):
    """
    This takes our rolled curve, generates the guesses for the fit function,
    and runs the fit.  It returns the parameters to generate the curve.
    """
    max_x = np.max(centered_x)
    max_y = np.max(centered_y)
    sigma = 90
    p, cov = optimize.curve_fit(normal_fit, centered_x, centered_y, p0=[max_x, sigma, max_y])
    
    return p
    


def plot_fits(direction_rates,fit_curve,title):
    """
    This function takes the x-values and the y-values  in units of spikes/s 
    (found in the two columns of direction_rates and fit_curve) and plots the 
    actual values with circles, and the curves as lines in both linear and 
    polar plots.
    """
    #print direction_rates
    
    
    
   # print fit_curve
   
    plt.subplots_adjust(hspace = 0.6)   
    y_max = np.max(direction_rates[:,1]) + 5
    plt.subplot(2,2,3)
    plt.axis([0,360,0,y_max])
    plt.plot(direction_rates[:,0], direction_rates[:,1],'o')
    plt.plot(fit_curve[:,0],fit_curve[:,1], '-')
    plt.xlabel("Direction of Motion (degrees)")
    plt.ylabel("Firing Rate (spikes/s)")
    plt.title(title)
    
    plt.subplot(2,2,4,  polar = True)    
    spikecounts = direction_rates[:,1]
    spikecounts2 = np.append(spikecounts, direction_rates[0,1]) 
    r = np.arange(0, 361, 45)*np.pi/180
    plt.polar(r, spikecounts2,'o')
    plt.polar(fit_curve[:,0]*np.pi/180,fit_curve[:,1],'-', label="Firing Rate (spikes/s)")
    plt.title(title)
    plt.legend(loc=8)
    

def von_mises_fitfunc(x, A, kappa, l, s):
    """
    This creates a scaled Von Mises distrubition.
    """
    return A*stats.vonmises.pdf(x, kappa, loc=l, scale=s)


    
def preferred_direction(fit_curve):
    """
    The function takes a 2-dimensional array with the x-values of the fit curve
    in the first column and the y-values of the fit curve in the second.  
    It returns the preferred direction of the neuron (in degrees).
    """
    y_max = np.max(fit_curve[:,1])
    y_idx = np.nonzero(fit_curve[:,1]==y_max)[0][0]
    pd = fit_curve[y_idx,0]
    
    return pd
    
def rfr(direction_rates):
    """
    Function that does rolling, fitting and rolling back
    """        
    #ROLL AXES
    new_x, new_y, roll_deg  = roll_axes(direction_rates)
    print new_x
    #FITTING
    p = fit_tuning_curve(new_x, new_y)
    curve_xs = np.arange(new_x[0],new_x[-1])
    #print curve_xs
    fit_ys = normal_fit(curve_xs,p[0],p[1],p[2])
    i=0
    
    zero_idx = np.nonzero(curve_xs == 0)[0][0]
    curve_xs = np.roll(curve_xs, -zero_idx)
    fit_ys = np.roll(fit_ys, -zero_idx)
    
    for item in curve_xs:
        if (item<0):
            curve_xs[i]=item+360
        i+=1    
    
   
    
    curve_fit = np.column_stack((curve_xs, fit_ys))
    print curve_fit
    return curve_fit
    
##########################
#You can put the code that calls the above functions down here    
if __name__ == "__main__":
    trials = load_experiment('trials.npy')  
    spk_times = load_neuraldata('neuron1.npy') 
    
    direction_rates = bin_spikes(trials, spk_times, 0.1)
    #print direction_rates
    plot_tuning_curves(direction_rates, "Example Neuron Tuning Curve")
    
    fit_curve = rfr(direction_rates)
    plot_fits(direction_rates, fit_curve,"Example Tuning Curve - VM Fit")
    
    print "prefered direction = " + str(preferred_direction(fit_curve))
