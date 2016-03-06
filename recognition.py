#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

import random
import os
from canvas import *

# Sorts a list, but returns a list of indicies
def sort_by_index(list):
    return [i[0] for i in sorted(enumerate(list), key=lambda x:x[1])]

# Gets the index of the smallest element of a list
def get_smallest_index(list):
    return sort_by_index(list)[0]

# Gets the sum of the squared differences of two vectors
def mean_squared_distance(v1,v2):
    res = np.array(v1) - np.array(v2)
    res = res**2
    return res.sum()

#
# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 360):
        self.sig = [0] * no_bins

    def print_signature(self):
        print self.sig

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self,noSonarReadings, size = 5):
        self.noSonarReadings = noSonarReadings
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
        ls = LocationSignature(self.noSonarReadings)
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

class Recognition:
  def __init__(self,useRobot,waypoints,walls,noSonarReadings):
    self.useRobot = useRobot
    self.walls = walls
    self.waypoints = waypoints
    self.noWaypoints = len(waypoints)
    self.noSonarReadings = noSonarReadings
    self.signatures = SignatureContainer(self.noSonarReadings,self.noWaypoints)

  def loadExisitingData(self):
    for i in xrange(5):
      print 'loaded : ', i,
      self.signatures.read(i)

  def sim_learn(self):
    # Delete old data
    self.signatures.delete_loc_files()
    # Do learning
    for w in self.waypoints:
        x,y = w
        print w
        self.particles = ps.Particles((x,y,0),1)
        self.learn_location()

  def sim_testRecognition(self,starting_angle=0):
    for i in xrange(5):
        x, y = self.waypoints[i]
        self.particles = ps.Particles((x,y,0),1)
        res = self.recognize_location()
        print 'expected ', i, ' got ', res[0], ' angle is between ', res[1]

  def sim_recognise(self,x,y,angle):
    self.particles = ps.Particles((x,y,angle),1)
    return self.recognize_location()


  # FILL IN: spin robot or sonar to capture a signature and store it in ls
  def characterize_location(self,ls):
      for i in range(len(ls.sig)):
          angle = float(i) * 360.0/float(len(ls.sig))
          ls.sig[i] = int(self.particles.getFakeSensorMeasurement(self.walls,angle,canvas))


  # FILL IN: compare two signatures
  def compare_signatures(self,ls1, ls2):
      #histogram returns a tuple of histogram and spacing bins -only take the histogram
      h1 = np.histogram(ls1.sig,bins=20,range=(0,255),normed=True)[0]
      h2 = np.histogram(ls2.sig,bins=20,range=(0,255),normed=True)[0]
      return mean_squared_distance(h1,h2)

  # This function characterizes the current location, and stores the obtained
  # signature into the next available file.
  def learn_location(self):
      ls = LocationSignature(self.noSonarReadings)
      self.characterize_location(ls)
      idx = self.signatures.get_free_index();
      if (idx == -1): # run out of signature files
          print "\nWARNING:"
          print "No signature file is available. NOTHING NEW will be learned and stored."
          print "Please remove some loc_%%.dat files.\n"
          return

      self.signatures.save(ls,idx)
      print "STATUS:  Location " + str(idx) + " learned and saved."

  # This function tries to recognize the current location.e
  # 1.   Characterize current location
  # 2.   For every learned locations
  # 2.1. Read signature of learned location from file
  # 2.2. Compare signature to signature coming from actual characterization
  # 3.   Retain the learned location whose minimum distance with
  #      actual characterization is the smallest.
  # 4.   Display the index of the recognized location on the screen
  def recognize_location(self):
      ls_obs = LocationSignature(self.noSonarReadings)
      self.characterize_location(ls_obs)
      dist = []
      # FILL IN: COMPARE ls_read with ls_obs and find the best match
      for idx in range(self.signatures.size):
          # print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
          ls_read = self.signatures.read(idx)
          dist.append(self.compare_signatures(ls_obs, ls_read))

      #find smallest distance
      smallest_idx = get_smallest_index(dist)

      # Reload the chosen signature and try and calculate starting angle
      chosen_sig = self.signatures.read(smallest_idx)
      angle = self.estimate_angle(chosen_sig.sig, ls_obs.sig)

      return (smallest_idx,angle)

  # Try to recover the starting angle by comparing two signatures
  def estimate_angle(self,chosen,observed):
      meansq = []
      for i in xrange(len(chosen)):
          meansq.append(mean_squared_distance(np.roll(chosen,-i),observed))

      smallest_idx = get_smallest_index(meansq)
      min = float(smallest_idx-1)*360.0/float(self.noSonarReadings)
      max = float(smallest_idx+1)*360.0/float(self.noSonarReadings)
      return (min,max)
