#This script creates plots from the output of the benchmarks

from matplotlib import pyplot as plt
import sys
import numpy as np
from os.path import exists

#This function creates plots from the running-time measurements.
#The format of the files is:
# Number of clients;Total time spend for encryption in ns;Total time spend for decryption in ns; Total time spend for setup in ns
def plot():
    #This is the number of test-runs that are contained in the input file.
    runs_per_file = 1
    #This is the number of lines per run, i.e.
    lines_per_run = 10
    if len(sys.argv) == 3:
        runs_per_file = int(sys.argv[1])
        lines_per_run = int(sys.argv[2])
        
    if len(sys.argv) == 2:
        runs_per_file = int(sys.argv[1])
        
        
    file1 = open('runtime.txt', 'r')
    Lines1 = file1.readlines()
    if len(sys.argv) == 1:
        runs_per_file = len(Lines1) // lines_per_run
    
    lass_file_exists = exists('runtime_lass.txt')
    if lass_file_exists:
        file2 = open('runtime_lass.txt', 'r')
        Lines2 = file2.readlines()
    else:   #fill Lines2 with one-entries (reduces case distinctions) (we will not print a plot in this case)
        Lines2 = ['1;1;1;1\n'] * lines_per_run * runs_per_file
        
    assert(len(Lines1) == lines_per_run * runs_per_file)
    assert(len(Lines2) == lines_per_run * runs_per_file)
        
    # these are the arrays for our scheme
    num_clients1 = [0] * lines_per_run
    runtime_enc1 = [0] * lines_per_run
    runtime_dec1 = [0] * lines_per_run
    runtime_setup1 = [0] * lines_per_run
    
    # these are the arrays for the LaSS scheme
    num_clients2 = [0] * lines_per_run
    runtime_enc2 = [0] * lines_per_run
    runtime_dec2 = [0] * lines_per_run
    runtime_setup2 = [0] * lines_per_run

    #numpy part for computing the errors
    array1 = [[[0 for columns in range(4)] for rows in range(lines_per_run)] for stuff in range(runs_per_file)]
    array2 = [[[0 for columns in range(4)] for rows in range(lines_per_run)] for stuff in range(runs_per_file)]
    
    for run_idx in range(0,runs_per_file):
        for line_idx in range(0, lines_per_run):
            line1 = Lines1[run_idx * lines_per_run + line_idx].strip()
            line2 = Lines2[run_idx * lines_per_run + line_idx].strip()
            split_strings1 = line1.split(';')
            split_strings2 = line2.split(';')
            
            array1[run_idx][line_idx][0] = (int(split_strings1[0]))
            array1[run_idx][line_idx][1] = (int(split_strings1[1]))
            array1[run_idx][line_idx][2] = (int(split_strings1[2]))
            array1[run_idx][line_idx][3] = (int(split_strings1[3]))
            
            array2[run_idx][line_idx][0] = (int(split_strings2[0]))
            array2[run_idx][line_idx][1] = (int(split_strings2[1]))
            array2[run_idx][line_idx][2] = (int(split_strings2[2]))
            array2[run_idx][line_idx][3] = (int(split_strings2[3]))
                   
    np_array1 = np.array(array1)
    np_array2 = np.array(array2)
    
    #weird hack to convince numpy to use floats
    np_array1 = np_array1 / 1
    np_array2 = np_array2 / 1
    
    #divide enc-time by number of clients
    np_array1[:,:,1] = np_array1[:,:,1] / np_array1[:,:,0]
    np_array2[:,:,1] = np_array2[:,:,1] / np_array2[:,:,0]
    
    #divide dec-time by 1000
    np_array1[:,:,2] = np_array1[:,:,2] / 1000.0
    np_array2[:,:,2] = np_array2[:,:,2] / 1000.0
    
    #transform from nanoseconds to milliseconds/seconds
    #enc
    np_array1[:,:,1] = np_array1[:,:,1] / 1000000.0
    np_array2[:,:,1] = np_array2[:,:,1] / 1000000.0
    #dec
    np_array1[:,:,2] = np_array1[:,:,2] / 1000000.0
    np_array2[:,:,2] = np_array2[:,:,2] / 1000000.0
    #setup
    np_array1[:,:,3] = np_array1[:,:,3] / 1000000000.0
    np_array2[:,:,3] = np_array2[:,:,3] / 1000000000.0
    
    #compute standard deviation of results
    np_error_enc_1 = np.std(np_array1[:,:,1], axis=0)
    np_error_dec_1 = np.std(np_array1[:,:,2], axis=0)
    np_error_setup_1 = np.std(np_array1[:,:,3], axis=0)
    
    np_error_enc_2 = np.std(np_array2[:,:,1], axis=0)
    np_error_dec_2 = np.std(np_array2[:,:,2], axis=0)
    np_error_setup_2 = np.std(np_array2[:,:,3], axis=0)
    
    #print("Standard deviation enc (our scheme): " + str(np_error_enc_1))
    #print("Standard deviation dec (our scheme): " + str(np_error_dec_1))
    #print("Standard deviation setup (our scheme): " + str(np_error_setup_1))
    #print("Standard deviation enc (LaSS): " + str(np_error_enc_2))
    #print("Standard deviation dec (LaSS): " + str(np_error_dec_2))
    #print("Standard deviation setup (LaSS): " + str(np_error_setup_2))

    #end numpy part
    
    for run_idx in range(0,runs_per_file):
        for line_idx in range(0, lines_per_run):
            line1 = Lines1[run_idx * lines_per_run + line_idx].strip()
            line2 = Lines2[run_idx * lines_per_run + line_idx].strip()

            #process lines of our scheme
            split_strings1 = line1.split(';')
            num_clients1[line_idx] += (int(split_strings1[0]))
            runtime_enc1[line_idx] += (int(split_strings1[1]))
            runtime_dec1[line_idx] += (int(split_strings1[2]))
            runtime_setup1[line_idx] += (int(split_strings1[3]))
            
            #process lines of lass scheme
            split_strings2 = line2.split(';')
            num_clients2[line_idx] += (int(split_strings2[0]))
            runtime_enc2[line_idx] += (int(split_strings2[1]))
            runtime_dec2[line_idx] += (int(split_strings2[2]))
            runtime_setup2[line_idx] += (int(split_strings2[3]))  
            
    for i in range(0, lines_per_run):
        num_clients1[i] = int(num_clients1[i] / runs_per_file)
        runtime_enc1[i] /= runs_per_file
        runtime_dec1[i] /= runs_per_file
        runtime_setup1[i] /= runs_per_file
        
        num_clients2[i] = int(num_clients2[i] / runs_per_file)
        runtime_enc2[i] /= runs_per_file
        runtime_dec2[i] /= runs_per_file
        runtime_setup2[i] /= runs_per_file
    
    #compute running time per client
    for i in range(0,len(runtime_enc1)):
        runtime_enc1[i] /= num_clients1[i]
        runtime_enc2[i] /= num_clients2[i]

    #transform runtime from nanoseconds to milliseconds/seconds
    for i in range(0,len(runtime_enc1)):
        runtime_enc1[i] /= 1000000  #nanoseconds to milliseconds
        runtime_dec1[i] /= 1000000000   #divide by 10^6 for conversion to milliseconds and by 10^3 because of 1000 runs per decryption
        runtime_setup1[i] /= 1000000000 #nanoseconds to seconds
        
        runtime_enc2[i] /= 1000000  #nanoseconds to milliseconds
        runtime_dec2[i] /= 1000000000   #also divide by 1000, because of the 1000 runs for each decrypt
        runtime_setup2[i] /= 1000000000 #nanoseconds to seconds
        
    
    #print("Num clients: " + str(num_clients1))
    #print("Running time enc ours: " + str(runtime_enc1))
    #print("Running time dec ours: " + str(runtime_dec1))
    #print("Running time setup ours: " + str(runtime_setup1))
    
    #print("Running time enc lass " + str(runtime_enc2))
    #print("Running time dec lass " + str(runtime_dec2))
    #print("Running time setup lass: " + str(runtime_setup2))
    
    max_list = [max(runtime_enc1), max(runtime_dec1), max(runtime_enc2), max(runtime_dec2)]
    max_value = max(max_list)
    
    plt.ylim(0,max_value*1.1)
    plt.plot(num_clients1, runtime_enc1, 'r-')
    plt.plot(num_clients1, runtime_enc1, 'ro', label='Encryption (Our scheme)')
    plt.errorbar(num_clients1, runtime_enc1, yerr = np_error_enc_1, fmt='ro')
    plt.plot(num_clients1, runtime_dec1, 'g-')
    plt.plot(num_clients1, runtime_dec1, 'gs', label='Decryption (Our scheme)')
    plt.errorbar(num_clients1, runtime_dec1, yerr = np_error_dec_1, fmt='gs')
    plt.plot(num_clients1, runtime_enc2, 'b-')
    if lass_file_exists:
        plt.plot(num_clients1, runtime_enc2, 'bd', label='Encryption (LaSS)')
        plt.errorbar(num_clients1, runtime_enc2, yerr = np_error_enc_2, fmt='bd')
        plt.plot(num_clients1, runtime_dec2, 'c-')
        plt.plot(num_clients1, runtime_dec2, 'c^', label='Decryption (LaSS)')
        plt.errorbar(num_clients1, runtime_dec2, yerr = np_error_dec_2, fmt='c^')
    
    plt.legend(loc=0)
    plt.xlabel("Number of clients")
    plt.ylabel("Running time in milliseconds")
    plt.savefig("enc-dec.svg")
    plt.clf()
    
    #plt.ylim(0,max_value*1.1)
    plt.plot(num_clients1, runtime_setup1, 'g-')
    plt.plot(num_clients1, runtime_setup1, 'go', label='Setup (Our scheme)')
    plt.errorbar(num_clients1, runtime_setup1, yerr = np_error_setup_1, fmt='go')
    if lass_file_exists:
        plt.plot(num_clients1, runtime_setup2, 'b-')
        plt.plot(num_clients1, runtime_setup2, 'bd', label='Setup (LaSS)')
        plt.errorbar(num_clients1, runtime_setup2, yerr = np_error_setup_2, fmt='bd')
    
    plt.legend(loc=0)
    plt.xlabel("Number of clients")
    plt.ylabel("Running time in seconds")
    plt.savefig("setup.svg")
    plt.clf()
    
    #output values for the table in the paper
    print("Running time encryption 1000 users (our scheme):  " + str(runtime_enc1[0]) + " standard deviation: " + str(np_error_enc_1[0]))
    print("Running time encryption 5000 users (our scheme):  " + str(runtime_enc1[4]) + " standard deviation: " + str(np_error_enc_1[4]))
    print("Running time encryption 10000 users (our scheme): " + str(runtime_enc1[9]) + " standard deviation: " + str(np_error_enc_1[9]))
    print("Running time decryption 1000 users (our scheme):  " + str(runtime_dec1[0]) + " standard deviation: " + str(np_error_dec_1[0]))
    print("Running time decryption 5000 users (our scheme):  " + str(runtime_dec1[4]) + " standard deviation: " + str(np_error_dec_1[4]))
    print("Running time decryption 10000 users (our scheme): " + str(runtime_dec1[9]) + " standard deviation: " + str(np_error_dec_1[9]))
    if lass_file_exists:
        print("Running time encryption 1000 users (LaSS):  " + str(runtime_enc2[0]) + " standard deviation: " + str(np_error_enc_2[0]))
        print("Running time encryption 5000 users (LaSS):  " + str(runtime_enc2[4]) + " standard deviation: " + str(np_error_enc_2[4]))
        print("Running time encryption 10000 users (LaSS): " + str(runtime_enc2[9]) + " standard deviation: " + str(np_error_enc_2[9]))
        print("Running time decryption 1000 users (LaSS):  " + str(runtime_dec2[0]) + " standard deviation: " + str(np_error_dec_2[0]))
        print("Running time decryption 5000 users (LaSS):  " + str(runtime_dec2[4]) + " standard deviation: " + str(np_error_dec_2[4]))
        print("Running time decryption 10000 users (LaSS): " + str(runtime_dec2[9]) + " standard deviation: " + str(np_error_dec_2[9]))
    
    
    
    
plot()
