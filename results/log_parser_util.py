import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from tkFileDialog import askopenfilename

from IPython.display import HTML,display

from Tkinter import *

# this function to get avgs of each event to write in to database
def get_avg(files):
    avgs = np.zeros((0,6))
    for file in files:
        with open(file) as fp:
            lines = fp.readlines()

        event_one = np.zeros((1,0))
        event_two = np.zeros((1,0))
        event_three = np.zeros((1,0))
        event_four = np.zeros((1,0))
        event_five = np.zeros((1,0))
        event_six = np.zeros((1,0))

        for line in lines:
            if "Robot_id" in line:
                splitted_line = line.split(" ")
                if splitted_line[7] is '0':
                    event_one = np.hstack([event_one,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '1':
                    event_two = np.hstack([event_two,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '2':
                    event_three = np.hstack([event_three,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '3':
                    event_four = np.hstack([event_four,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '4':
                    event_five = np.hstack([event_five,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '5':
                    event_six = np.hstack([event_six,[[float(splitted_line[8])]]]) 
        avgs = np.vstack([avgs,[np.average(event_one),np.average(event_two),np.average(event_three),
                       np.average(event_four),np.average(event_five),np.average(event_six)]])
    return avgs
# use the below function only for parsing neo4j write logs
def get_avg_neo(files):
    avgs = np.zeros((0,6))
    for file in files:
        with open(file) as fp:
            lines = fp.readlines()

        event_one = np.zeros((1,0))
        event_two = np.zeros((1,0))
        event_three = np.zeros((1,0))
        event_four = np.zeros((1,0))
        event_five = np.zeros((1,0))
        event_six = np.zeros((1,0))

        for line in lines:
            if "Robot_id" in line:
                splitted_line = line.split(" ")
                if splitted_line[6] is '1':
                    event_one = np.hstack([event_one,[[float(splitted_line[7])]]])
                elif splitted_line[6] is '2':
                    event_two = np.hstack([event_two,[[float(splitted_line[7])]]])
                elif splitted_line[6] is '3':
                    event_three = np.hstack([event_three,[[float(splitted_line[7])]]])
                elif splitted_line[6] is '4':
                    event_four = np.hstack([event_four,[[float(splitted_line[7])]]])
                elif splitted_line[6] is '5':
                    event_five = np.hstack([event_five,[[float(splitted_line[7])]]])
                elif splitted_line[6] is '6':
                    event_six = np.hstack([event_six,[[float(splitted_line[7])]]]) 
        avgs = np.vstack([avgs,[np.average(event_one),np.average(event_two),np.average(event_three),
                       np.average(event_four),np.average(event_five),np.average(event_six)]])
    return avgs

def get_avg_read(files):
    avgs = np.zeros((0,4))
    for file in files:
        with open(file) as fp:
            lines = fp.readlines()
            
        query_one = np.zeros((1,0))
        query_two = np.zeros((1,0))
        query_three = np.zeros((1,0))
        query_four = np.zeros((1,0))

        for line in lines:
            if "Robot_id" in line:
                splitted_line = line.split(" ")
                if splitted_line[7] is '0':
                    query_one = np.hstack([query_one,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '1':
                    query_two = np.hstack([query_two,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '2':
                    query_three = np.hstack([query_three,[[float(splitted_line[8])]]])
                elif splitted_line[7] is '3':
                    query_four = np.hstack([query_four,[[float(splitted_line[8])]]])
        avgs = np.vstack([avgs,[np.average(query_one),np.average(query_two),np.average(query_three),
                               np.average(query_four)]])
    return avgs

def get_replica_results(files):
        result = []
        #get the write time stamp
        with open(files[0]) as fp:
            lines = fp.readlines()
        write_vals = {}
        for line in lines:
            if "replica_test_write" in line:
                splitted_line = line.split(" ")
                timestamp = splitted_line[9] + " " + splitted_line[10].split("\n")[0]
                write_vals[splitted_line[7]] = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        
        #get the read time stamp
        with open(files[1]) as fp:
            lines = fp.readlines()
        read_vals = {}
        for line in lines:
            if "replica_test_read" in line:
                splitted_line = line.split(" ")
                timestamp = splitted_line[9] + " " + splitted_line[10].split("\n")[0]
                read_vals[splitted_line[7]] = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')  
        
        for key,value in read_vals.iteritems():
            diff = value-write_vals[key]
            result.append(float(str(diff).split(".")[1])/1000000)
        return str(round(np.average(result),4)) + "seconds"
        

def open_files(n):
    files = []
    for i in range(n):
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        files.append(filename)
    return files