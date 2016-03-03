#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os
from canvas import *

#
# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 360):
        self.sig = [0] * no_bins

    def print_signature(self):
        print self.sig

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];

        # Fills the filenames variable with names like loc_%%.dat
        # where %% are 2 digits (00, 01, 02...) indicating the location number.
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1

        if (n >= self.size):
            return -1;
        else:
            return n;

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])

    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)

        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close();
        else:
            print "WARNING: Signature does not exist."

        return ls

# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    for i in range(len(ls.sig)):
        angle = float(i) * 360.0/float(len(ls.sig))
        ls.sig[i] = int(particles.getFakeSensorMeasurement(walls,angle,canvas))


# FILL IN: compare two signatures
def compare_signatures(ls1, ls2):
    #histogram returns a tuple of histogram and spacing bins -only take the histogram
    h1 = np.histogram(ls1.sig,bins=20,range=(0,255),normed=True)[0]
    h2 = np.histogram(ls2.sig,bins=20,range=(0,255),normed=True)[0]
    histogram_difference = h1 - h2
    histogram_difference = histogram_difference**2
    dist = histogram_difference.sum()
    return dist

# This function characterizes the current location, and stores the obtained
# signature into the next available file.
def learn_location():
    ls = LocationSignature(noSonarReadings)
    characterize_location(ls)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return

    signatures.save(ls,idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."

# This function tries to recognize the current location.e
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location():
    ls_obs = LocationSignature(noSonarReadings);
    characterize_location(ls_obs);
    dist = []
    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        # print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx);
        dist.append(compare_signatures(ls_obs, ls_read))

    #find smallest distance
    smallest_d = dist[0]
    smallest_idx = 0
    for i in xrange(1,len(dist)):
        if dist[i] < smallest_d:
            smallest_d = dist[i]
            smallest_idx = i

    return (smallest_idx,dist[smallest_idx])

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files().
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.
noSonarReadings = 5
signatures = SignatureContainer(5)

signatures.delete_loc_files()
for w in waypoints:
    x,y = w
    print w
    particles = ps.Particles((x,y,0.0),1)
    learn_location()

for i in xrange(5):
    print 'loaded : ', i,
    signatures.read(i)

print ' RECOGNITION : '
for i in xrange(5):
    x, y = waypoints[i]
    particles = ps.Particles((x,y,0.0),1)
    res = recognize_location()
    print 'expected ', i, ' got ', res[0], 'with probability ', 1.0 - res[1]
