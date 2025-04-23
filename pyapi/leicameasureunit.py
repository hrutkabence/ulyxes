#!/usr/bin/env python
"""
.. module:: leicameasureunit.py
   :platform: Unix, Windows
   :synopsis: Ulyxes - an open source project to drive total stations and
       publish observation results. GPL v2.0 license Copyright (C)
       2010- Zoltan Siki <siki.zoltan@epito.bme.hu>

.. moduleauthor:: Zoltan Siki <siki.zoltan@epito.bme.hu>,
    Daniel Moka <mokadaniel@citromail.hu>

"""

import re
import logging
from measureunit import MeasureUnit
from angle import Angle

class LeicaMeasureUnit(MeasureUnit):
    """ This class contains the Leica robotic total station specific functions
        common to all leica robot TS

            :param name: name of ts (str), default 'Leica generic'
            :param type: type of ts (str), default 'TPS'
    """
    # Constants for message codes
    codes = {
        'SWITCHON': 111,
        'SWITCHOFF': 112,
        'SETPC': 2024,
        'GETPC': 2023,
        'INSTRNO': 5003,
        'INSTRNAME': 5004,
        'INTTEMP': 5011,
        'SETATR': 9018,
        'GETATR': 9019,
        'SETLOCK': 9020,
        'GETLOCK': 9021,
        'LOCKIN': 9013,
        'SETATMCORR': 2028,
        'GETATMCORR': 2029,
        'SETREFCORR': 2030,
        'GETREFCORR': 2031,
        'GETSTN': 2009,
        'SETSTN': 2010,
        'SETEDMMODE': 2020,
        'GETEDMMODE': 2021,
        'SETORI': 2113,
        'MOVE': 9027,
        'MEASURE': 2008,
        'GETMEASURE': 2108,
        'MEASUREANGDIST': 17017,
        'COORDS': 2082,
        'GETANGLES': 2003,
        'CHANGEFACE': 9028,
        'SETSEARCHAREA': 9043,
        'POWERSEARCH': 9052,
        'SEARCHNEXT': 9051,
        'SETREDLASER': 1004,
        'GETPT': 17009,
        'SETPT': 17008,
        'GETSPIRAL': 9040,
        'SETSPIRAL': 9041,
        'SEARCHTARGET': 17020
    }

    # Constants for EMD modes
    edmModes = {'STANDARD': 0, 'PRECISE': 1, 'FAST': 2, 'TRACKING': 3,
                'AVERAGING': 4, 'FASTTRACKING': 5}

    # Constants for EDM programs
    edmProg = {'STOP': 0, 'DEFAULT': 1, 'TRACKING': 2, 'CLEAR': 3}

    def __init__(self, name='Leica generic', typ='TPS'):
        """ Constructor to leica generic ts
        """
        # call super class init
        super().__init__(name, typ)

    @staticmethod
    def GetCapabilities():
        """ Get instrument specialities

            :returns: empty list, do not use generic instrument
        """
        return []

    def Result(self, msgs, anss):
        """ Parse answer from message

            :param msgs: messages sent to instrument
            :param anss: aswers got from instrument
            :returns: dictionary
        """
        msgList = re.split(r'\|', msgs)
        ansList = re.split(r'\|', anss)
        res = {}
        for msg, ans in zip(msgList, ansList):
            # get command id form message
            msgBufflist = re.split(':|,', msg)
            try:
                commandID = int(msgBufflist[1])
            except Exception:
                commandID = -1
            # get error code from answer
            ansBufflist = re.split(':|,', ans)
            try:
                errCode = int(ansBufflist[3])
                if commandID == self.codes['GETMEASURE']:
                    res['hz'] = Angle(float(ansBufflist[4]))
                    res['v'] = Angle(float(ansBufflist[5]))
                    res['distance'] = float(ansBufflist[6])
                # MeasureDistAng
                elif commandID == self.codes['MEASUREANGDIST']:
                    res['hz'] = Angle(float(ansBufflist[4]))
                    res['v'] = Angle(float(ansBufflist[5]))
                    res['distance'] = float(ansBufflist[6])
                # Prism constant
                elif commandID == self.codes['GETPC']:
                    res['pc'] = float(ansBufflist[4])
                # Prism type
                elif commandID == self.codes['GETPT']:
                    res['pt'] = int(ansBufflist[4])
                # ATR
                elif commandID == self.codes['GETATR']:
                    res['atrStatus'] = int(ansBufflist[4])
                #GetLockStatus()
                elif commandID == self.codes['GETLOCK']:
                    res['lockStat'] = int(ansBufflist[4])
                #GetAtmCorr()
                elif commandID == self.codes['GETATMCORR']:
                    res['lambda'] = ansBufflist[4]
                    res['pressure'] = float(ansBufflist[5])
                    res['dryTemp'] = float(ansBufflist[6])
                    res['wetTemp'] = float(ansBufflist[7])
                #GetRefCorr()
                elif commandID == self.codes['GETREFCORR']:
                    res['status'] = ansBufflist[4]
                    res['earthRadius'] = float(ansBufflist[5])
                    res['refractiveScale'] = float(ansBufflist[6])
                elif commandID == self.codes['GETSTN']:
                    res['east'] = float(ansBufflist[4])
                    res['north'] = float(ansBufflist[5])
                    res['elev'] = float(ansBufflist[6])
                    res['ih'] = float(ansBufflist[7])
                elif commandID == self.codes['GETEDMMODE']:
                    res['edmMode'] = int(ansBufflist[4])
                #Coords()
                elif commandID == self.codes['COORDS']:
                    res['east'] = float(ansBufflist[4])
                    res['north'] = float(ansBufflist[5])
                    res['elev'] = float(ansBufflist[6])
                #GetAngles()
                elif commandID == self.codes['GETANGLES']:
                    res['hz'] = Angle(float(ansBufflist[4]))
                    res['v'] = Angle(float(ansBufflist[5]))
                    res['crossincline'] = Angle(float(ansBufflist[8]))
                    res['lengthincline'] = Angle(float(ansBufflist[9]))
                # GetSpiral()
                elif commandID == self.codes['GETSPIRAL']:
                    res['hzRange'] = Angle(float(ansBufflist[4]))
                    res['vRange'] = Angle(float(ansBufflist[5]))
                elif commandID == self.codes['INSTRNO']:
                    res['instrNo'] = ansBufflist[4]
                elif commandID == self.codes['INSTRNAME']:
                    res['instrName'] = ansBufflist[4]
                elif commandID == self.codes['INTTEMP']:
                    res['intTemp'] = float(ansBufflist[4])
            except ValueError:
                errCode = -1   # invalid answer
            except IndexError:
                errCode = -2   # instrument off?
            if errCode != 0:
                logging.error(" error from instrument: %d (command %d)", errCode, commandID)
                res['errorCode'] = errCode
                #if not errCode in (1283, 1284, 1285, 1288):
                # do not stop if accuracy is not perfect
        return res

    def SetPcMsg(self, pc):
        """ Set prism constant

            :param pc: prism constant [mm]
            :returns: set prism constant message
        """
        return f"%R1Q,{self.codes['SETPC']}:{pc}"

    def GetPcMsg(self):
        """ Get prism constant

            :returns: get prism constant message
        """
        return f"%R1Q,{self.codes['GETPC']}:"

    def SetPrismTypeMsg(self, typ):
        """ Set prism type

            :param typ: prism type (0/1/2/3/4/5/6/7 round/mini/tape/360/user1/user2/user3/360 mini)
        """
        return f"%R1Q,{self.codes['SETPT']}:{typ}"

    def GetPrismTypeMsg(self):
        """ Get prism type

            :returns: prism type (0/1/2/3/4/5/6/7 round/mini/tape/360/user1/user2/user3/360 mini)
        """
        return f"%R1Q,{self.codes['GETPT']}:"

    def SetATRMsg(self, atr):
        """ Set ATR status on/off

            :param atr: 0/1 = off/on
            :returns: set atr message string
        """
        return f"%R1Q,{self.codes['SETATR']}:{atr}"

    def GetATRMsg(self):
        """ Get ATR status

            :returns: get atr message
        """
        return f"%R1Q,{self.codes['GETATR']}:"

    def SetLockMsg(self, lock):
        """ Set Lock status

            :param lock: 0/1 = off/on
            :returns: set lock status message
        """
        return f"%R1Q,{self.codes['SETLOCK']}:{lock}"

    def GetLockMsg(self):
        """ Get Lock status

            :returns: get lock status message
        """
        return f"%R1Q,{self.codes['GETLOCK']}:"

    def LockInMsg(self):
        """ Activate lock

            :returns: active lock message
        """
        return f"%R1Q,{self.codes['LOCKIN']}:"

    def SetAtmCorrMsg(self, valueOfLambda, pres, dry, wet):
        """ Set atmospheric correction settings

            :param valueOfLambda: Constant for the instrument not changeable, use GetAtmCorr to get value
            :param pres: pressure value
            :param dry: dry temperature
            :param wet: wet temperature
            :returns: set atmospheric correction message
        """
        return f"%R1Q,{self.codes['SETATMCORR']}:{valueOfLambda:.8f},{pres},{dry},{wet}"

    def GetAtmCorrMsg(self):
        """ Get atmospheric correction settings

            :returns: iget atmospheric settings message
        """
        return f"%R1Q,{self.codes['GETATMCORR']}:"

    def SetRefCorrMsg(self, status, earthRadius, refracticeScale):
        """ Set refraction correction settings

            :param status: 0/1 = off/on
            :param earthRadius: radius ot the Earth
            :param refracticeScale: refractice scale
            :returns: set refraction message
        """
        return f"%R1Q,{self.codes['SETREFCORR']}:{status},{earthRadius},{refracticeScale}"

    def GetRefCorrMsg(self):
        """ Get refraction correction setting

            :returns: get refraction correction message

        """
        return f"%R1Q,{self.codes['GETREFCORR']}:"

    def SetStationMsg(self, e, n, z, ih=0.0):
        """ Set station coordinates

            :param e: easting
            :param n: northing
            :param z: elevation
            :param ih: instrument height (optional, default 0)
            :returns: set station coordinates message
        """
        return f"%R1Q,{self.codes['SETSTN']}:{e},{n},{z},{ih}"

    def GetStationMsg(self):
        """ Get station coordinates

        :returns: get station coordinates message

        """
        return f"%R1Q,{self.codes['GETSTN']}:"

    def SetEDMModeMsg(self, mode):
        """ Set EDM mode

            :param mode: string name/code
            :returns: set edm mode message
        """
        if type(mode) is str:
            imode = self.edmModes[mode]
        else:
            imode = mode
        return f"%R1Q,{self.codes['SETEDMMODE']}:{imode}"

    def GetEDMModeMsg(self):
        """ Get EDM mode

            :returns: get edm mode message
        """
        return f"%R1Q,{self.codes['GETEDMMODE']}:"

    def SetOriMsg(self, ori):
        """ Set orientation angle

            :param ori: bearing of direction (Angle)
            :returns: 0 or error code

        """
        ori_rad = ori.GetAngle('RAD')
        return f"%R1Q,{self.codes['SETORI']}:{ori_rad}"

    def MoveMsg(self, hz, v, atr=0):
        """ Rotate instrument to direction with ATR or without ATR

            :param hz: horizontal direction (Angle)
            :param v: zenith angle (Angle)
            :param atr: 0/1 atr off/on, default off
            :returns: rotate message

        """
        # change angles to radian
        hz_rad = hz.GetAngle('RAD')
        v_rad = v.GetAngle('RAD')
        return f"%R1Q,{self.codes['MOVE']}:{hz_rad},{v_rad},0,{atr},0"

    def MeasureMsg(self, prg=1, incl=0):
        """ Measure distance

            :param prg: measure program 1/2/3/... = default/track/clear..., optional (default 1, mode set before)
            :param incl: inclination calculation - 0/1/2 = measure always (slow)/calculate (fast)/automatic, optional (default 0)

            :returns: measure message
        """
        return f"%R1Q,{self.codes['MEASURE']}:{prg},{incl}"

    def GetMeasureMsg(self, wait=15000, incl=0):
        """ Get measured distance

            :param wait: time in ms, optional (default 15000), it must be greater than 12000, the default on the instrument
            :param incl: inclination calculation - 0/1/2 = measure always (slow)/calculate (fast)/automatic, optional (default 0)
            :returns: get simple measurement message
        """
        return f"%R1Q,{self.codes['GETMEASURE']}:{wait},{incl}"

    def MeasureDistAngMsg(self, prg):
        """ Measure angles and distance

            :param prg: EDM program
            :returns: measure angle distance message

        """
        if type(prg) is str:
            prg = self.edmProg[prg]
        return f"%R1Q,{self.codes['MEASUREANGDIST']}:{prg}"

    def CoordsMsg(self, wait=15000, incl=0):
        """ Get coordinates

            :param wait: wait-time in ms, optional (default 15000), it must be greater than 12000, the default on instrument
            :param incl: inclination calculation - 0/1/2 = measure always (slow)/calculate (fast)/automatic, optional (default 0)
            :returns: get coordinates message
        """
        return f"%R1Q,{self.codes['COORDS']}:{wait},{incl}"

    def GetAnglesMsg(self):
        """ Get angles

                :returns: get angles message
        """
        return f"%R1Q,{self.codes['GETANGLES']}:0"

    def ClearDistanceMsg(self):
        """ Clearing distance

                :returns: clear distance message
        """
        return self.MeasureMsg(self, 3)

    def ChangeFaceMsg(self):
        """ Change face

            :returns: change face message
        """
        return f"%R1Q,{self.codes['CHANGEFACE']}:"

    def GetSpiralMsg(self):
        """ Get search spiral parameters

            :returns: get spiral message
        """
        return f"%R1Q,{self.codes['GETSPIRAL']}:"

    def SetSpiralMsg(self, dRangeHz, dRangeV):
        """ Set search priral parameters

            :param dRangeHz: horizontal range of search (Angle)
            :param dRangeV: vertical range of search (Angle)
            :returns: set search spiral message
        """
        return f"%R1Q,{self.codes['SETSPIRAL']}:{dRangeHz.GetAngle('RAD')},{dRangeV.GetAngle('RAD')}"

    def SearchTargetMsg(self):
        """ Search target using user spiral

            :returns: Search target message
        """
        return f"%R1Q,{self.codes['SEARCHTARGET']}:"

    def SwitchOnMsg(self, mode=1):
        """ Switch on instrument or wake up and change to remote mode

            :param mode: startup mode 0/1 local/remote
            :returns: switch on message
        """
        return f"%R1Q,{self.codes['SWITCHON']}:{mode}"

    def SwitchOffMsg(self):
        """ Switch off instrument

        """
        return 'b'

    def GetInstrumentNoMsg(self):
        """ Get instrument factory number

            :returns: get instrument factory number message
        """
        return f"%R1Q,{self.codes['INSTRNO']}:"

    def GetInstrumentNameMsg(self):
        """ Get instrument name

            :returns: get instrument name
        """
        return f"%R1Q,{self.codes['INSTRNAME']}:"

    def GetInternalTemperatureMsg(self):
        """ Get instrument internal temperature

            :returns: instrument internal temperature
        """
        return f"%R1Q,{self.codes['INTTEMP']}:"
