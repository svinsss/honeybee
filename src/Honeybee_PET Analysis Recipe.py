# This component assembles an analysis recipe for the annual adaptive comfort component
#
# Honeybee: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
# 
# This file is part of Honeybee.
# 
# Copyright (c) 2013-2018, Chris Mackey <Chris@MackeyArchitecture.com> 
# Honeybee is free software; you can redistribute it and/or modify 
# it under the terms of the GNU General Public License as published 
# by the Free Software Foundation; either version 3 of the License, 
# or (at your option) any later version. 
# 
# Honeybee is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Honeybee; If not, see <http://www.gnu.org/licenses/>.
# 
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>


"""
Use this component to assemble an adaptive comfort recipe for the "Honeybee_Annual Indoor Comfort Analysis" component.
-
Provided by Honeybee 0.0.63
    
    Args:
        _viewFactorMesh: The data tree of view factor meshes that comes out of the  "Honeybee_Indoor View Factor Calculator".
        _viewFactorInfo: The python list that comes out of the  "Honeybee_Indoor View Factor Calculator".
        _epwFile: The epw file that was used to run the EnergyPlus model.  This will be used to generate sun vectors and get radiation data for estimating the temperature delta for sun falling on occupants.
        ===============: ...
        srfIndoorTemp_: A list surfaceIndoorTemp data out of the "Honeybee_Read EP Surface Result" component.
        _srfOutdoorTemp: A list surfaceOutdoorTemp data out of the "Honeybee_Read EP Surface Result" component.
        zoneAirTemp_: The airTemperature output of the "Honeybee_Read EP Result" component.
        zoneRelHumid_: The relativeHumidity output of the "Honeybee_Read EP Result" component.
        zoneAirFlowVol_: The airFlowVolume output of the "Honeybee_Read EP Result" component.
        zoneAirHeatGain_: The airHeatGainRate output of the "Honeybee_Read EP Result" component.
        bodyCharacteristics_: A list of body characteristics in the following order: age, sex, height, weight, bodyPosition, clothingInsulation, acclimated, metabolicRate, activityDuration.
              Use Ladybug's "Body Characteristics" component to generate it.
              -
              If not supplied, the following default values will be used:
              --
              30 - age
              "male" - sex
              175 - height in centimeters
              75 - weight in kilograms
              "standing" - bodyPosition
              None (clothingInsulation - "None" means that it will be calculated based on air temperature)
              37 - clothingAlbedo in % (for medium colored clothes)
              "unacclimated" - acclimated
              2.32 - metabolicRate in mets (2.32 corresponds to walking 4km/h)
              480 - activityDuration in minutes
        ===============: ...
        temperateOrTropical_: Set to "True" to have the component use the tropical/subtropical/humid categories to determine whether the conditions are cold, hot, or comfortable.  Set to "False" to use categories for a temperate climate.  The tropical categories were determined by Lin and Matzarakis (2008) and the temperate categories were determined by Matzarakis and Mayer (1996). The default is set to "True" for tropical/subtropical categories.
        wellMixedAirOverride_: Set to "True" if you know that your building will have a forced air system with diffusers meant to mix the air as well as possilbe.  This will prevent the calculation from running the air stratification function and instead assume well mixed conditions.  This input can also be a list of 8760 boolean values that represent the hours of the year when a forced air system or ceiling fans are run to mix the air.  The default is set to 'False' to run the stratification calculation for every hour of the year, assuming no forced air heating/cooling system.
        inletHeightOverride_: An optional list of float values that match the data tree of view factor meshes and represent the height, in meters, from the bottom of the view factor mesh to the window inlet height.  This will override the default value used in the air stratification calculation, which sets the inlet height in the bottom half of the average glazing height.
        windowShadeTransmiss_: A decimal value between 0 and 1 that represents the transmissivity of the shades on the windows of a zone (1 is no shade and 0 is fully shaded).  This input can also be a list of 8760 values between 0 and 1 that represents a list of hourly window shade transmissivities to be applied to all windows of the model. Finally and most importantly, this can be the 'windowTransmissivity' output of the 'Read EP Surface Result' component for an energy model that has been run with window shades.  This final option ensures that the energy model and the confort map results are always aligned although it is the most computationally expensive of the options.  The default is set to 0, which assumes no additional shading to windows. 
        cloAbsorptivity_: An optional decimal value between 0 and 1 that represents the fraction of solar radiation absorbed by the human body. The default is set to 0.7 for (average/brown) skin and average clothing.  You may want to increase this value for darker skin or darker clothing.
        windSpeed_: A value in m/s to set the wind speed of the comfort calculation. Use this input to account for objects like ceiling fans that might increase the interior wind speed or input custom wind speed values from a CFD simulation.
            _
            This input can also be a list of 8760 additional wind speed values that represent the hours of the year.
            Alternatively, this input can be a data tree of values with branches that are each 8760 values long and correspond to the branches of the input viewFactorMesh_.
            This can also be a data tree of values with one branch for each point in the input viewFactorMesh_.
            Finally, this input can be the file path to a .csv file that is organized with 8760 values in each column and a number of columns that correspond to the number of test points.  This last option is recommended if trying to synchronize CFD results with the microclimate maps.
            _
            If no value is input here, the comfort map components will compute a minimum indoor air speed from the zone volume and hourly flow volume and will use the EPW wind speed for outdoor conditions.
        outdoorTerrain_: An interger or text string that sets the terrain class associated with the wind speed used in outdoor wind calculations. Interger values represent the following terrain classes:
            0 = City: large city centres, 50% of buildings above 21m over a distance of at least 2000m upwind.
            1 = Suburban: suburbs, wooded areas.
            2 = Country: open, with scattered objects generally less than 10m high.
            3 = Water: Flat, unobstructed areas exposed to wind flowing over a large water body (no more than 500m inland).
        north_: Input a vector to be used as a true North direction for the comfort analysis or a number between 0 and 360 that represents the degrees off from the y-axis to make North.  The default North direction is set to the Y-axis (0 degrees).
    Returns:
        readMe!: ...
        ===============: ...
        comfRecipe: An analysis recipe for the "Honeybee_Annual Indoor Comfort Analysis" component.
"""

ghenv.Component.Name = "Honeybee_PET Analysis Recipe"
ghenv.Component.NickName = 'PETComfRecipe'
ghenv.Component.Message = 'VER 0.0.63\nJAN_20_2018'
ghenv.Component.IconDisplayMode = ghenv.Component.IconDisplayMode.application
ghenv.Component.Category = "Honeybee"
ghenv.Component.SubCategory = "10 | Energy | Energy"
#compatibleHBVersion = VER 0.0.56\nJul_24_2017
#compatibleLBVersion = VER 0.0.59\nJUN_07_2016
try: ghenv.Component.AdditionalHelpFromDocStrings = "6"
except: pass


from System import Object
from System import Drawing
import System
import Grasshopper.Kernel as gh
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
import Rhino as rc
import scriptcontext as sc
import math
import os


w = gh.GH_RuntimeMessageLevel.Warning
tol = sc.doc.ModelAbsoluteTolerance


def clothingInsulation(Ta):
    # by MENEX_2005 model
    if Ta > 25:
        Icl = 0.5  # summer clothes
    else:
        Icl = 1.691 - 0.0436*Ta
    
    if Icl > 4:
        Icl = 4.1  # Heavy polar outfit
    
    return Icl

def checkTheInputs():
    w = gh.GH_RuntimeMessageLevel.Warning
    
    #Unpack the viewFactorInfo.
    checkData25 = True
    try:
        viewFacInfoFromHive = hb_hive.visualizeFromHoneybeeHive(_viewFactorInfo)[0]
        testPtViewFactor, zoneSrfNames, testPtSkyView, testPtBlockedVec, testPtZoneWeights, \
        testPtZoneNames, ptHeightWeights, zoneInletInfo, zoneHasWindows, outdoorIsThere, \
        outdoorNonSrfViewFac, outdoorPtHeightWeights, testPtBlockName, zoneWindowTransmiss, \
        zoneWindowNames, zoneFloorReflectivity, constantTransmis, finalAddShdTransmiss = viewFacInfoFromHive.recallAllProps()
    except:
        testPtViewFactor, zoneSrfNames, testPtSkyView, testPtBlockedVec, testPtZoneWeights, testPtZoneNames, ptHeightWeights, zoneInletInfo, zoneHasWindows, outdoorIsThere, outdoorNonSrfViewFac, outdoorPtHeightWeights, testPtBlockName, zoneWindowTransmiss, zoneWindowNames, zoneFloorReflectivity, constantTransmis, finalAddShdTransmiss = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], True, []
        checkData25 = False
        warning = "_viewFactorInfo is not valid."
        print warning
        w = gh.GH_RuntimeMessageLevel.Warning
        ghenv.Component.AddRuntimeMessage(w, warning)
    
    # Get the full number of test points.
    testPtNum = 0
    for ptList in testPtViewFactor:
        for pt in ptList: testPtNum += 1
    
    #Convert the data tree of _viewFactorMesh to py data.
    viewFactorMesh = []
    checkData13 = True
    pathCheck = 0
    finalCheck = len(testPtViewFactor)
    if _viewFactorMesh.BranchCount != 0:
        if _viewFactorMesh.Branch(0)[0] != None:
            treePaths = _viewFactorMesh.Paths
            for path in treePaths:
                i = path.Indices[0]
                if i == pathCheck:
                    branchList = _viewFactorMesh.Branch(path)
                    dataVal = []
                    for item in branchList:
                        dataVal.append(item)
                    viewFactorMesh.append(dataVal)
                    pathCheck += 1
                else:
                    while pathCheck < i:
                        viewFactorMesh.append([])
                        pathCheck += 1
                    if i == pathCheck:
                        branchList = _viewFactorMesh.Branch(path)
                        dataVal = []
                        for item in branchList:
                            dataVal.append(item)
                        viewFactorMesh.append(dataVal)
                        pathCheck += 1
            if len(viewFactorMesh) < finalCheck:
                while len(viewFactorMesh) < finalCheck:
                    viewFactorMesh.append([])
        else:
            checkData13 = False
            print "Connect a data tree of view factor meshes from the 'Honeybee_Indoor View Factor Calculator' component."
    else:
        checkData13 = False
        print "Connect a data tree of view factor meshes from the 'Honeybee_Indoor View Factor Calculator' component."
    
    #Create a function to check and create a Python list from a datatree
    def checkCreateDataTree(dataTree, dataName, dataType):
        dataPyList = []
        for i in range(dataTree.BranchCount):
            branchList = dataTree.Branch(i)
            dataVal = []
            for item in branchList:
                try: dataVal.append(float(item))
                except: dataVal.append(item)
            dataPyList.append(dataVal)
        
        #Test to see if the data has a header on it, which is necessary to know if it is the right data type.  If there's no header, the data should not be vizualized with this component.
        checkHeader = []
        dataHeaders = []
        dataNumbers = []
        for list in dataPyList:
            if str(list[0]) == "key:location/dataType/units/frequency/startsAt/endsAt":
                checkHeader.append(1)
                dataHeaders.append(list[:7])
                dataNumbers.append(list[7:])
            else:
                dataNumbers.append(list)
        
        if sum(checkHeader) == len(dataPyList):
            dataCheck2 = True
        else:
            dataCheck2 = False
            warning = "Not all of the connected " + dataName + " has a Ladybug/Honeybee header on it.  This header is necessary to generate an indoor temperture map with this component."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        #Check to be sure that the lengths of data in in the dataTree branches are all the same.
        dataLength = len(dataNumbers[0])
        dataLenCheck = []
        for list in dataNumbers:
            if len(list) == dataLength:
                dataLenCheck.append(1)
            else: pass
        if sum(dataLenCheck) == len(dataNumbers) and dataLength <8761:
            dataCheck4 = True
        else:
            dataCheck4 = False
            warning = "Not all of the connected " + dataName + " branches are of the same length or there are more than 8760 values in the list."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        if dataCheck2 == True:
            #Check to be sure that all of the data headers say that they are of the same type.
            header = dataHeaders[0]
            
            headerUnits =  header[3]
            headerStart = header[5]
            headerEnd = header[6]
            simStep = str(header[4])
            headUnitCheck = []
            headPeriodCheck = []
            for head in dataHeaders:
                if dataType in head[2]:
                    headUnitCheck.append(1)
                if head[3] == headerUnits and str(head[4]) == simStep and head[5] == headerStart and head[6] == headerEnd:
                    headPeriodCheck.append(1)
                else: pass
            
            if sum(headPeriodCheck) == len(dataHeaders):
                dataCheck5 = True
            else:
                dataCheck5 = False
                warning = "Not all of the connected " + dataName + " branches are of the same timestep or same analysis period."
                print warning
                ghenv.Component.AddRuntimeMessage(w, warning)
            
            if sum(headUnitCheck) == len(dataHeaders):
                dataCheck6 = True
            else:
                dataCheck6 = False
                warning = "Not all of the connected " + dataName + " data is for the correct data type."
                print warning
                ghenv.Component.AddRuntimeMessage(w, warning)
            
            #See if the data is hourly.
            if simStep == 'hourly' or simStep == 'Hourly': pass
            else:
                dataCheck6 = False
                warning = "Simulation data must be hourly."
                print warning
                ghenv.Component.AddRuntimeMessage(w, warning)
            
        else:
            dataCheck5 = False
            dataCheck6 == False
            if dataLength == 8760: annualData = True
            else: annualData = False
            simStep = 'unknown timestep'
            headerUnits = 'unknown units'
            dataHeaders = []
        
        return dataCheck5, dataCheck6, headerUnits, dataHeaders, dataNumbers, [header[5], header[6]]
    
    #Run all of the EnergyPlus data through the check function.
    if outdoorIsThere == False and srfIndoorTemp_.BranchCount > 0 and zoneAirTemp_.BranchCount > 0  and zoneAirFlowVol_.BranchCount > 0 and zoneAirHeatGain_.BranchCount > 0:
        #Indoor only calculation and everything is good.
        checkData1, checkData2, airTempUnits, airTempDataHeaders, airTempDataNumbers, analysisPeriod = checkCreateDataTree(zoneAirTemp_, "zoneAirTemp_", "Air Temperature")
        checkData3, checkData4, srfTempUnits, srfTempHeaders, srfTempNumbers, analysisPeriod = checkCreateDataTree(srfIndoorTemp_, "srfIndoorTemp_", "Inner Surface Temperature")
        checkData21, checkData22, flowVolUnits, flowVolDataHeaders, flowVolDataNumbers, analysisPeriod = checkCreateDataTree(zoneAirFlowVol_, "zoneAirFlowVol_", "Air Flow Volume")
        checkData23, checkData24, heatGainUnits, heatGainDataHeaders, heatGainDataNumbers, analysisPeriod = checkCreateDataTree(zoneAirHeatGain_, "zoneAirHeatGain_", "Air Heat Gain Rate")
        checkData17, checkData18, relHumidUnits, relHumidDataHeaders, relHumidDataNumbers, analysisPeriod = checkCreateDataTree(zoneRelHumid_, "zoneRelHumid_", "Relative Humidity")
        outdoorClac = False
        checkData29, checkData30, outSrfTempUnits, outSrfTempHeaders, outSrfTempNumbers = True, True, 'C', [], []
    elif srfIndoorTemp_.BranchCount > 0 and zoneAirTemp_.BranchCount > 0  and zoneAirFlowVol_.BranchCount > 0 and zoneAirHeatGain_.BranchCount > 0:
        #All inputs are provided and it doesn't matter whether the indoor/outdoor is there.
        checkData1, checkData2, airTempUnits, airTempDataHeaders, airTempDataNumbers, analysisPeriod = checkCreateDataTree(zoneAirTemp_, "zoneAirTemp_", "Air Temperature")
        checkData3, checkData4, srfTempUnits, srfTempHeaders, srfTempNumbers, analysisPeriod = checkCreateDataTree(srfIndoorTemp_, "srfIndoorTemp_", "Inner Surface Temperature")
        checkData21, checkData22, flowVolUnits, flowVolDataHeaders, flowVolDataNumbers, analysisPeriod = checkCreateDataTree(zoneAirFlowVol_, "zoneAirFlowVol_", "Air Flow Volume")
        checkData23, checkData24, heatGainUnits, heatGainDataHeaders, heatGainDataNumbers, analysisPeriod = checkCreateDataTree(zoneAirHeatGain_, "zoneAirHeatGain_", "Air Heat Gain Rate")
        checkData17, checkData18, relHumidUnits, relHumidDataHeaders, relHumidDataNumbers, analysisPeriod = checkCreateDataTree(zoneRelHumid_, "zoneRelHumid_", "Relative Humidity")
        checkData29, checkData30, outSrfTempUnits, outSrfTempHeaders, outSrfTempNumbers, analysisPeriod = checkCreateDataTree(_srfOutdoorTemp, "__srfOutdoorTemp", "Outer Surface Temperature")
        outdoorClac = True
    elif outdoorIsThere == True:
        #Do a check to see if all of the zone lists are empty (except for the last one, which contains outdoor info.
        allListsEmpty = True
        for zoneList in testPtViewFactor[:-1]:
            if zoneList == []: pass
            else:allListsEmpty = False
        if allListsEmpty == True:
            #The user has input only outdoor srf temperature and only an outdoor mesh.  We can run the calculation just for the outdoors.
            checkData29, checkData30, outSrfTempUnits, outSrfTempHeaders, outSrfTempNumbers, analysisPeriod = checkCreateDataTree(_srfOutdoorTemp, "__srfOutdoorTemp", "Outer Surface Temperature")
            outdoorClac = True
            checkData1, checkData2, checkData3, checkData4, checkData21, checkData22, checkData23, checkData24, checkData17, checkData18 = True, True, True, True, True, True, True, True, True, True
            emptyLists = testPtViewFactor[:-1] + [[]]
            airTempDataHeaders, airTempDataNumbers, srfTempHeaders, srfTempNumbers, flowVolDataHeaders, heatGainDataHeaders, relHumidDataHeaders, relHumidDataNumbers = emptyLists, emptyLists, emptyLists, emptyLists, emptyLists, emptyLists, emptyLists, emptyLists
            numberLists = []
            for zoneCount, zoneList in enumerate(emptyLists):
                numberLists.append(range(len(outSrfTempNumbers[0])))
            flowVolDataNumbers, heatGainDataNumbers = numberLists, numberLists
            flowVolUnits = "m3/s"
            heatGainUnits = "W"
            airTempUnits = srfTempUnits = "C"
            relHumidUnits = "%"
        else:
            checkData1, checkData2, checkData3, checkData4, checkData21, checkData22, checkData23, checkData24, checkData17, checkData18 = False, False, False, False, False, False, False, False, False, False
            warning = 'If you have connected a viewFactorMesh that includes regions on the indoors, you must connect up energy simulation data for zoneAirTemp, srfIndoorTemp, zoneAirFlowVol, zoneAirHeatGain, and zoneRelHumid.'
            print warning
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    else:
        checkData1, checkData2, checkData3, checkData4, checkData21, checkData22, checkData23, checkData24, checkData17, checkData18 = False, False, False, False, False, False, False, False, False, False
        warning = 'If you have connected a viewFactorMesh that includes regions on the indoors, you must connect up energy simulation data for zoneAirTemp, srfIndoorTemp, zoneAirFlowVol, zoneAirHeatGain, and zoneRelHumid.'
        print warning
        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
    
    
    if checkData1 == True and checkData2 == True and checkData3 == True and checkData4 == True and checkData21 == True and checkData22 == True and checkData23 == True and checkData24 == True and checkData17 == True and checkData18 == True:
        #Check the windowShadeTransmiss_.
        checkData14 = True
        checkData32 = True
        winStatusNumbers = []
        winStatusHeaders = []
        allWindowShadesSame = True
        try:
            if windowShadeTransmiss_.BranchCount == 1 and len(windowShadeTransmiss_.Branch(0)) != 8767:
                windowShadeTransmiss = []
                for shadeValue in windowShadeTransmiss_.Branch(0):
                    windowShadeTransmiss.append(shadeValue)
                if len(windowShadeTransmiss) == 8760:
                    allGood = True
                    for transVal in windowShadeTransmiss:
                        transFloat = float(transVal)
                        if transFloat <= 1.0 and transFloat >= 0.0: winStatusNumbers.append(transFloat)
                        else: allGood = False
                    if allGood == False:
                        checkData14 = False
                        warning = 'windowShadeTransmiss_ must be a value between 0 and 1.'
                        print warning
                        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
                elif len(windowShadeTransmiss) == 1:
                    if float(windowShadeTransmiss[0]) <= 1.0 and float(windowShadeTransmiss[0]) >= 0.0:
                        for count in range(8760):
                            winStatusNumbers.append(float(windowShadeTransmiss[0]))
                    else:
                        checkData14 = False
                        warning = 'windowShadeTransmiss_ must be a value between 0 and 1.'
                        print warning
                        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
            elif windowShadeTransmiss_.BranchCount > 1 or len(windowShadeTransmiss_.Branch(0)) == 8767:
                allWindowShadesSame = False
                checkData14, checkData32, winStatusUnits, winStatusHeaders, winStatusNumbers, analysisPeriod = checkCreateDataTree(windowShadeTransmiss_, "windowShadeTransmiss_", "Surface Window System Solar Transmittance")
                #Convert all of the numbers in shade status data tree to window transmissivities.
                for winBCount, windowBranchList in enumerate(winStatusNumbers):
                    for shadHrCt, shadVal in enumerate(windowBranchList):
                        winStatusNumbers[winBCount][shadHrCt] = float(shadVal)
            elif constantTransmis == True:
                for count in range(8760):
                    winStatusNumbers.append(1)
                print 'No value found for windowShadeTransmiss_.  The window shade status will be set to 1 assuming no additional shading beyond the window glass transmissivity.'
        except:
            for count in range(8760):
                winStatusNumbers.append(1)
            print 'No value found for windowShadeTransmiss_.  The window shade status will be set to 1 assuming no additional shading beyond the window glass transmissivity.'
        
        
        #Check to see if there are hourly transmissivities for the additional shading.
        if constantTransmis == False:
            allWindowShadesSame = False
            for transmisslistCount, transmissList in enumerate(finalAddShdTransmiss):
                winStatusNumbers.append(transmissList)
                srfName = 'AddShd' + str(transmisslistCount)
                shdHeader = ['key:location/dataType/units/frequency/startsAt/endsAt', 'Location', 'Surface Window System Solar Transmittance for ' + srfName + ': Window', 'Fraction', 'Hourly', analysisPeriod[0], analysisPeriod[1]]
                winStatusHeaders.append(shdHeader)
        
        #Check the windSpeed_.
        checkData33 = True
        winSpeedNumbers = []
        pathCheck = 0
        allWindSpeedsSame = 1
        if windSpeed_.BranchCount == 1:
            additionalWindSpeed = []
            for windValue in windSpeed_.Branch(0):
                additionalWindSpeed.append(windValue)
            if len(additionalWindSpeed) == 1:
                try:
                    for count in range(8760):
                        winSpeedNumbers.append(float(additionalWindSpeed[0]))
                except:
                    try:
                        if additionalWindSpeed[0].upper().endswith('.CSV'):
                            allWindSpeedsSame = -1
                            result = open(additionalWindSpeed[0], 'r')
                            for lineCount, line in enumerate(result):
                                winSpeedNumbers.append([])
                                for column in line.split(','):
                                    winSpeedNumbers[lineCount].append(float(column))
                            result.close()
                        else:
                            checkData33 = False
                            warning = 'windSpeed_ values not recognized.'
                            print warning
                            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
                    except:
                        checkData33 = False
                        warning = 'windSpeed_ values not recognized.'
                        print warning
                        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
            elif len(additionalWindSpeed) == 8760:
                allGood = True
                for winSp in additionalWindSpeed:
                    windFloat = float(winSp)
                    if windFloat >= 0.0: winSpeedNumbers.append(windFloat)
                    else: allGood = False
                if allGood == False:
                    checkData33 = False
                    warning = 'windSpeed_ must be a value greater than 0.'
                    print warning
                    ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
            else:
                checkData33 = False
                warning = 'windSpeed_ must be either a list of 8760 values that correspond to hourly changing wind speeds over the year or a single constant value for the whole year.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        elif windSpeed_.BranchCount > 1:
            
            if windSpeed_.BranchCount == testPtNum:
                #Wind speed values for each point in the analysis.
                allWindSpeedsSame = -1
                winSpeedNumInit = []
                for i in range(windSpeed_.BranchCount):
                    branchList = windSpeed_.Branch(i)
                    dataVal = []
                    for item in branchList:
                        dataVal.append(float(item))
                    winSpeedNumInit.append(dataVal)
                winSpeedNumbers = zip(*winSpeedNumInit)
                
            elif windSpeed_.BranchCount == _viewFactorMesh.BranchCount:
                #Wind speed for each zone in the analysis.
                allWindSpeedsSame = 0
                treePaths = windSpeed_.Paths
                for path in treePaths:
                    i = path.Indices[0]
                    if i == pathCheck:
                        branchList = windSpeed_.Branch(path)
                        dataVal = []
                        for item in branchList:
                            dataVal.append(float(item))
                        winSpeedNumbers.append(dataVal)
                        pathCheck += 1
                    else:
                        while pathCheck < i:
                            winSpeedNumbers.append([])
                            pathCheck += 1
                        if i == pathCheck:
                            branchList = windSpeed_.Branch(path)
                            dataVal = []
                            for item in branchList:
                                dataVal.append(float(item))
                            winSpeedNumbers.append(dataVal)
                            pathCheck += 1
                if len(winSpeedNumbers) < finalCheck:
                    while len(winSpeedNumbers) < finalCheck:
                        winSpeedNumbers.append([])
            else:
                checkData33 = False
                warning = 'windSpeed_ data tree branches do not match those of the viewFactorMesh or the number of testPts.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        else:
            print 'No value found for windSpeed_. The components will use an indoor wind speed from the air flow volume or outdoor EPW wind speed.'
        
        
        #Check to be sure that the units of flowVol and heat gain are correct.
        checkData9 = True
        if flowVolUnits == "m3/s": pass
        else:
            checkData9 = False
            warning = "_zoneFlowVol must be in m3/s."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        checkData10 = True
        if heatGainUnits == "W": pass
        else:
            checkData10 = False
            warning = "_zoneHeatGain must be in W."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        checkData11 = True
        if airTempUnits == srfTempUnits == "C": pass
        else:
            checkData11 = False
            warning = "zoneAirTemp_ and srfIndoorTemp_ must be in degrees C."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        checkData19 = True
        if relHumidUnits == "%": pass
        else:
            checkData11 = False
            warning = "zoneRelHumid_ must be in %."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        checkData28 = True
        if outSrfTempUnits == "C": pass
        else:
            checkData28 = False
            warning = "_srfOutdoorTemp must be in degrees C."
            print warning
            ghenv.Component.AddRuntimeMessage(w, warning)
        
        #Try to parse the weather file in order to get direct rad, diffuse rad, and location data.
        checkData5 = True
        if not os.path.isfile(_epwFile):
            checkData5 = False
            warningM = "Failed to find the file: " + str(_epwFile)
            print warningM
            ghenv.Component.AddRuntimeMessage(w, warningM)
        else:
            locationData = lb_preparation.epwLocation(_epwFile)
            location = locationData[-1]
            weatherData = lb_preparation.epwDataReader(_epwFile, locationData[0])
            directNormalRadiation = weatherData[5]
            diffuseHorizontalRadiation = weatherData[6]
            globalHorizontalRadiation = weatherData[7]
            horizInfraredRadiation = weatherData[12]
            outDryBulbTemp = weatherData[0]
            outRelHumid = weatherData[2]
            outWindSpeed = weatherData[3]
        
        #Separate out the _dirNormRad, the diffuse Horizontal rad, and the location  data.
        directSolarRad = []
        diffSolarRad = []
        latitude = None
        longitude = None
        timeZone = None
        if checkData5 == True:
            directSolarRad = directNormalRadiation[7:]
            diffSolarRad = diffuseHorizontalRadiation[7:]
            globHorizRad = globalHorizontalRadiation[7:]
            horizInfraredRadiation = horizInfraredRadiation[7:]
            locList = location.split('\n')
            for line in locList:
                if "Latitude" in line: latitude = float(line.split(',')[0])
                elif "Longitude" in line: longitude = float(line.split(',')[0])
                elif "Time Zone" in line: timeZone = float(line.split(',')[0])
        
        #Check to be sure that the number of mesh faces and test points match.
        checkData8 = True
        if checkData25 == True:
            for zoneCount, zone in enumerate(viewFactorMesh):
                if len(zone) != 1:
                    totalFaces = 0
                    for meshCount, mesh in enumerate(zone):
                        totalFaces = totalFaces +mesh.Faces.Count
                    if totalFaces == len(testPtViewFactor[zoneCount]): pass
                    else:
                        totalVertices = 0
                        for meshCount, mesh in enumerate(zone):
                            totalVertices = totalVertices +mesh.Vertices.Count
                        
                        if totalVertices == len(testPtViewFactor[zoneCount]): pass
                        else:
                            checkData8 = False
                            warning = "For one of the meshes in the _viewFactorMesh, the number of faces in the mesh and test points in the _testPtViewFactor do not match.\n" + \
                            "This can sometimes happen when you have geometry created with one Rhino model tolerance and you generate a mesh off of it with a different tolerance.\n"+ \
                            "Try changing your Rhino model tolerance and seeing if it works."
                            print warning
                            ghenv.Component.AddRuntimeMessage(w, warning)
                else:
                    if zone[0].Faces.Count == len(testPtViewFactor[zoneCount]): pass
                    else:
                        if zone[0].Vertices.Count == len(testPtViewFactor[zoneCount]): pass
                        else:
                            checkData8 = False
                            warning = "For one of the meshes in the _viewFactorMesh, the number of faces in the mesh and test points in the _testPtViewFactor do not match.\n" + \
                            "This can sometimes happen when you have geometry created with one Rhino model tolerance and you generate a mesh off of it with a different tolerance.\n"+ \
                            "Try changing your Rhino model tolerance and seeing if it works."
                            print warning
                            ghenv.Component.AddRuntimeMessage(w, warning)
        
        #If there are no outdoor surface temperatures and there are outdoor view factors, remove it from the mesh.
        if outdoorClac == False and outdoorIsThere == True:
            zoneSrfNames = zoneSrfNames[:-1]
            testPtViewFactor = testPtViewFactor[:-1]
            viewFactorMesh = viewFactorMesh[:-1]
            testPtSkyView = testPtSkyView[:-1]
            testPtBlockedVec = testPtBlockedVec[:-1]
        
        # bodyCharacteristics
        checkData20 = True
        if (len(bodyCharacteristics_) != 10) and (len(bodyCharacteristics_) != 0):
            TaL = mrtL_calculated = TdpL = rhL = wsL = SRL = NL = TgroundL = RprimL = vapourPressureL = EpotL = HOYs = date = newAnalysisPeriod = age = sex = heightCM = heightM = weight = bodyPosition = IclL = ac = acclimated = ML = activityDuration = None
            checkData20 = False
            printMsg = "Your \"bodyCharacteristics_\" input is incorrect. Please use the \"bodyCharacteristics\" output from Ladybug's \"Body Characteristics\" component."
            print printMsg
            ghenv.Component.AddRuntimeMessage(w, printMsg)
        elif (len(bodyCharacteristics_) == 0) or (bodyCharacteristics_[0] is ""):
            bodyCharacteristics = {
            "age" : 35,
            "sex" : "male",
            "heightCM" : 175,  # in centimeters
            "heightM" : 1.75,  # in meters
            "weight" : 75,  # in kg
            "bodyPosition" : "standing",
            "Icl" : None,  # it will be calculated based on air temperature
            "ac" : 37,  # default in %, medium colored clothes
            "acclimated" : "unacclimated",
            "Mmets" : 2.32,  # default value: 2.32 met = 135 W/m2
            "activityDuration" : 480  # in minutes
            }
        elif (len(bodyCharacteristics_) == 10):
            bodyCharacteristics = {
            "age" : bodyCharacteristics_[0],
            "sex" : bodyCharacteristics_[1],
            "heightCM" : bodyCharacteristics_[2],
            "heightM" : bodyCharacteristics_[2]/100,
            "weight" : bodyCharacteristics_[3],
            "bodyPosition" : bodyCharacteristics_[4],
            "Icl" : bodyCharacteristics_[5],
            "ac" : bodyCharacteristics_[6],
            "acclimated" : bodyCharacteristics_[7],
            "Mmets" : bodyCharacteristics_[8],
            "activityDuration" : bodyCharacteristics_[9]
            }
        
        # check Icl and M from bodyCharacteristics
        if (bodyCharacteristics['Icl'] != None):
            # use "clothingInsulation" defined in "bodyCharacteristics_"
            bodyCharacteristics['Icl'] = [bodyCharacteristics['Icl'] for i in range(8760)]
        else:
            # nothing inputted to "bodyCharacteristics_" or something inputted to "bodyCharacteristics_" but "clothingInsulation" is not defined (equals to: None)
            bodyCharacteristics['Icl'] = [clothingInsulation(Ta) for Ta in outDryBulbTemp[7:]]
        
        #Figure out the number of times to divide the sky based on the length of the blockedVec list.
        numSkyPatchDivs = 0
        checkData12 = True
        if checkData25 == True:
            for blockList in testPtBlockedVec:
                if blockList != []:
                    if len(blockList[0]) == 145: numSkyPatchDivs = 0
                    elif len(blockList[0]) == 577: numSkyPatchDivs = 1
                    elif len(blockList[0]) == 1297: numSkyPatchDivs = 2
                    elif len(blockList[0]) == 2305: numSkyPatchDivs = 3
                    else:
                        checkData12 = False
                        warning = "You have an absurdly high number of view vectors from the 'Indoor View Factor' component such that it is not supported by the current component."
                        print warning
                        ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        
        #Check the clothing absorptivity.
        checkData7 = True
        cloA = 0.7
        if cloAbsorptivity_ != None:
            if cloAbsorptivity_ <= 1.0 and cloAbsorptivity_ >= 0.0: floorR = cloAbsorptivity_
            else:
                checkData7 = False
                warning = 'cloAbsorptivity_ must be a value between 0 and 1.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        else:
            print 'No value found for cloAbsorptivity_.  The absorptivity will be set to 0.7 for average brown skin and typical clothing.'
        
        #Check the outdoor terrain.
        checkData31, terrainType, d, a = lb_wind.readTerrainType(outdoorTerrain_)
        if checkData31 == False:
            warning = "Invalid input for terrainType_."
            ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        else:
            print "Terrain set to " + terrainType + "."
        
        #Check the inletHeightOverride_.
        inletHeightOverride = []
        checkData15 = True
        if checkData25 == True and len(inletHeightOverride_) > 0:
            if len(inletHeightOverride_) == len(viewFactorMesh): inletHeightOverride = inletHeightOverride_
            else:
                checkData15 = False
                warning = 'The length of data in the inletHeightOverride_ does not match the number of branches in the data tree of the _viewFactorMesh.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        
        #Check the wellMixedAirOverride_.
        checkData16 = True
        mixedAirOverride = []
        if wellMixedAirOverride_ != []:
            if len(wellMixedAirOverride_) == 8760:
                for val in wellMixedAirOverride_:
                    mixedAirOverride.append(int(val))
            elif len(wellMixedAirOverride_) == 1:
                for count in range(8760):
                    mixedAirOverride.append(int(wellMixedAirOverride_[0]))
            else:
                checkData16 = False
                warning = 'wellMixedAirOverride_ must be either a list of 8760 values that correspond to hourly air mixing over the year or a single constant value for the whole year.'
                print warning
                ghenv.Component.AddRuntimeMessage(gh.GH_RuntimeMessageLevel.Warning, warning)
        else:
            for count in range(8760):
                mixedAirOverride.append(0)
            print 'No value found for wellMixedAirOverride_.  The stratification calculation will be run for every hour of the year.'
        
        # Check the climate.
        climate = "humid"
        if temperateOrTropical_ == True:
            climate = "humid"
        elif temperateOrTropical_ == False:
            climate = "temperate"
        
        #Check the north direction.
        northAngle, northVector = lb_preparation.angle2north(north_)
        
        #Do a final check of everything.
        if checkData1 == True and checkData2 == True and checkData3 == True and checkData4 == True and checkData5 == True and checkData7 == True and checkData8 == True and checkData9 == True and checkData10 == True and checkData11 == True and checkData12 == True and checkData13 == True and checkData14 == True and checkData15 == True and checkData16 == True and checkData17 == True and checkData18 == True and checkData19 == True and checkData20 == True and checkData21 == True and checkData22 == True and checkData23 == True and checkData24 == True and checkData25 == True and checkData28 == True  and checkData29 == True and checkData30 == True and checkData31 == True and checkData32 == True  and checkData33 == True:
            checkData = True
        else: return -1
        
        return "PET", srfTempNumbers, srfTempHeaders, airTempDataNumbers, airTempDataHeaders, flowVolDataHeaders, flowVolDataNumbers, heatGainDataHeaders, heatGainDataNumbers, relHumidDataHeaders, relHumidDataNumbers, zoneSrfNames, testPtViewFactor, viewFactorMesh, latitude, longitude, timeZone, diffSolarRad, directSolarRad, globHorizRad, testPtSkyView, testPtBlockedVec, numSkyPatchDivs, winStatusNumbers, cloA, zoneFloorReflectivity, testPtZoneNames, testPtZoneWeights, ptHeightWeights, zoneInletInfo, inletHeightOverride, mixedAirOverride, zoneHasWindows, outdoorClac, outSrfTempHeaders, outSrfTempNumbers, outdoorNonSrfViewFac, outDryBulbTemp, outRelHumid, outWindSpeed, d, a, outdoorPtHeightWeights, allWindowShadesSame, winStatusHeaders, testPtBlockName, zoneWindowTransmiss, zoneWindowNames, allWindSpeedsSame, winSpeedNumbers, analysisPeriod, northAngle, bodyCharacteristics, climate, horizInfraredRadiation
    else:
        return -1


#Check to be sure that LB+HB are flying.
initCheck = False
if sc.sticky.has_key('honeybee_release') == False and sc.sticky.has_key('ladybug_release') == False:
    print "You should first let Ladybug and Honeybee fly..."
    ghenv.Component.AddRuntimeMessage(w, "You should first let Ladybug and Honeybee fly...")
else:
    initCheck = True
    lb_preparation = sc.sticky["ladybug_Preparation"]()
    lb_wind = sc.sticky["ladybug_WindSpeed"]()
    hb_hive = sc.sticky["honeybee_Hive"]()


#Check the data input.
checkData = False
if _viewFactorMesh.BranchCount > 0 and len(_viewFactorInfo) > 0 and _epwFile != None and _srfOutdoorTemp.BranchCount > 0 and initCheck == True:
    if _viewFactorInfo[0] != None:
        recipe = checkTheInputs()
        if recipe != -1:
            comfRecipe = recipe