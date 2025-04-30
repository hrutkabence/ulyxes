#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: freestation.py
    :platform: Linux, Windows
    :synopsis: interface modul to GNU Gama

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>

    calculate 3D coordinates of a station from polar observations as a
    free starion, blunders are eliminated

    :param argv[1]: input geo/coo or dmp/csv file
    :param argv[2]: gama-local path
"""

import sys
import os
import logging

# check PYTHONPATH
if len([p for p in sys.path if 'pyapi' in p]) == 0:
    if os.path.isdir('../pyapi/'):
        sys.path.append('../pyapi/')
    else:
        print("pyapi not found")
        print("Add pyapi directory to the Python path or start your application from ulyxes/pyapps folder")
        sys.exit(1)

from georeader import GeoReader
from csvreader import CsvReader
from gamaiface import GamaIface

class Freestation(object):
    """ Calculate freestation and remove blunders

        :param obs: list of observations
        :param coords: coordinates of points
        :param gama_path: path to gama-local
        :param dimiension: dimension of adjustment 1/2/3, optional default 3
        :param probability: probability level, optional, default 0.95
        :param stdev_angle: angle measurement standard deviation (seconds), optional, default 1"
        :param stdev_dist: distance measurement additive standard deviation (mm), optional, default 1 mm
        :param stdev_dist1: distance measurement multiplicative standdard deviation (mm/km), optional, default 1.5 mm/km
        :param blunders: remove blunders, optional, default True
    """

    def __init__(self, obs, coords, gama_path, dimension=3, probability=0.95,
                 stdev_angle=1, stdev_dist=1, stdev_dist1=1.5, blunders=False):
        """ initialize
        """
        # create gama interface
        self.g = GamaIface(gama_path, dimension, probability, stdev_angle,
                           stdev_dist, stdev_dist1)
        self.blunders = blunders
        ns = 0    # number of stations
        no = 0    # number of observations
        self.station = None
        for w in obs:
            if 'station' in w:
                ns += 1
                if ns > 1:
                    break    # stop after first station
                self.station = w['station']
                self.g.add_observation(w)
            elif 'id' in w and 'hz' in w and 'v' in w and 'distance' in w:
                no += 1 # number of observations
                self.g.add_observation(w)
        for w in coords:
            if 'id' in w and w['id'] == self.station:
                self.g.add_point(w, 'ADJ')
            elif 'east' in w and 'north' in w and 'elev' in w:
                self.g.add_point(w, 'FIX')

    def Adjustment(self):
        """ adjustment & and blunder removing

            :returns: adjusted coordinates or None
        """
        # adjustment loop
        last_res = None
        n = 0   # number of blunders removed
        while True:
            res, blunder = self.g.adjust()
            if res is None or 'east' not in res or 'north' not in res or \
                              'elev' not in res:
                # adjustment faild or too many blunders
                if last_res is not None:
                    logging.warning("blunders are not fully removed")
                    res = last_res
                else:
                    logging.error("adjustment failed")
                break
            elif not self.blunders:
                logging.warning("no blunders checked")
                break
            elif blunder['std-residual'] <= self.g.krit:
                logging.info("%d blunders removed", n)
                break
            else:
                logging.info("%s - %s observation removed",
                             blunder['from'], blunder['to'])
                self.g.remove_observation(blunder['from'], blunder['to'])
                last_res = res
                n += 1
        return [res]

if __name__ == "__main__":
    #logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.INFO)

    fname = "/home/siki/GeoEasy_old/data/freestation.geo"
    gama_path = '/home/siki/GeoEasy/gama-local'

    if len(sys.argv) > 1:
        fname = sys.argv[1]
        if not os.path.isfile(fname):
            print("File not found: " + fname)
            sys.exit(-1)
    else:
        print("Usage: freestation.py input_file gama_path")
        sys.exit(-1)
    if fname[-4:] not in ['.geo', '.coo', '.dmp', '.csv']:
        fname += '.geo'
    if len(sys.argv) > 2:
        gama_path = sys.argv[2]
    else:
        gama_path = '/home/siki/GeoEasy/src/gama-local'

    # load observations and coordinates
    fn = fname[:-4] # remove extension
    ext = fname[-4:]
    if ext in ['.geo', '.coo']:
        obs = GeoReader(fname=fn+'.geo')
    else:
        obs = CsvReader(fname=fn+'.dmp')
    # load observations
    observations = obs.Load()
    # load coordinates and add to adjustment
    if ext in ['.geo', '.coo']:
        coo = GeoReader(fname=fn+'.coo')
    else:
        coo = CsvReader(fname=fn+'.csv')
    n = 0   # number of points
    st = False  # station found
    coords = coo.Load()
    f = Freestation(observations, coords, gama_path)
    print(f.Adjustment())
