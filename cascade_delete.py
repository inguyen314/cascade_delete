# name=Cascade Delete
# displayinmenu=true
# displaytouser=true
# displayinselector=true
# backgroundColor=255,204,102,255
'''
Author: Ivan Nguyen
Last Updated: 05-24-2023
Description: Cascade Delete
Version: 1.2
'''
from hec.script				import MessageBox, Constants
from hec.dataTable			import HecDataTableToExcel
import java
import time,calendar,datetime
from time					import mktime
from hec.dssgui				import ListSelection
from javax.swing				import JOptionPane, JDialog, JButton, JPanel
from java.awt.event			import ActionListener, FocusListener
from java.text				import SimpleDateFormat
from java.awt				import BorderLayout, GridLayout, FlowLayout, Toolkit, GraphicsEnvironment, Rectangle, Color, Font
from rma.swing				import DateChooser
from javax.swing.border		import EmptyBorder
from time					import mktime
import inspect
import DBAPI
import os
import urllib
from hec.heclib.util			import HecTime
from hec.hecmath				import TimeSeriesMath
from hec.io					import TimeSeriesContainer
from rma.services				import ServiceLookup
from java.util					import TimeZone
from hec.data.tx                    	import QualityTx

#=========================================================
# Data Dictionary: Check for each Tier to Determine Which TS to Cascade Delete from ElevRev
StartTw  = datetime.datetime.now()
print '='
print '='
print '='
print '=================================================================================='
print '====================================== START CASCADE DELETE  LOG RUN AT ' + str(StartTw) + '=='
print '================================================================================== '
print '='
print '='
print '='

# determine if the selected location is from TIER 1 or TIER 2. TIER 1 cascade from ElevRev to StageRev. TIER 2 cascade ElevRev to StageRev and Stage29
DataDict =  {   'TIER1'     :   {   'Station'              :     ( 'Sand Ridge-Big Muddy',
		                                                                    'Florence-Illinois',
		                                                                    'Hardin-Illinois',
		                                                                    'Arnold-Meramec',
		                                                                    'Pittsburg-Kaskaskia',
		                                                                    'Champion City-Bourbeuse',
		                                                                    'Desloge-Big',
		                                                                    'Pacific-Meramec',
		                                                                    'Fisk-St Francis',
		                                                                    'St Francis-St Francis',
		                                                                    'Valley Park-Meramec',
		                                                                    'Birds Point-Mississippi',
		                                                                    'Chain of Rocks-Mississippi',
		                                                                    'Commerce-Mississippi',
		                                                                    'Engineers Depot-Mississippi',
		                                                                    'Grays Pt-Mississippi',
		                                                                    'Hermann-Missouri',
		                                                                    'Herculaneum-Mississippi',
		                                                                    'Jefferson Brks-Mississippi',
		                                                                    'Moccasin Springs-Mississippi',
		                                                                    'Price Ldg-Mississippi',
		                                                                    'Pump Sta 1-Wood River E Alton',
		                                                                    'Red Rock Ldg-Mississippi',
		                                                                    'Thompson Ldg-Mississippi',
		                                                                    'Upper Bissell Pt-Mississippi',
		                                                                    'Cairo-Ohio',
		                                                                    'Fredericktown-L St Francis',
		                                                                    'Greenville-St Francis',
		                                                                    'Iron Bridge-St Francis',
		                                                                    'Millcreek-St Francis',
		                                                                    'Patterson-St Francis',
		                                                                    'Roselle-St Francis',
		                                                                    'Saco-St Francis',
		                                                                    'Byrnesville-Big',
		                                                                    'Sam A Baker Park-Big Cr'),
		                                    'Parameters'            : 'Stage',
		                                    'Version'                   : 'lrgsShef-rev',
		                                    'None'                      : 'None'
                                },        
                'TIER2'     :   {   'Station'                   :	  ( 'Mt Vernon-Big Muddy',
		                                                                    'Mt Vernon-Casey Fork',
		                                                                    'Murphysboro-Big Muddy',
		                                                                    'Plumfield-Big Muddy',
		                                                                    'Rend Lk TW-Big Muddy',
		                                                                    'Waltonville-Rayse Cr',
		                                                                    'Troy-Cuivre',
		                                                                    'Meredosia-Illinois', 
		                                                                    'Valley City-Illinois',
		                                                                    'Allenville-Whitley Cr',
		                                                                    'Breese-Shoal Cr',
		                                                                    'Brownstown-Hickory Cr',
		                                                                    'Carlyle-Kaskaskia',
		                                                                    'Carlyle Lk TW-Kaskaskia',
		                                                                    'Chesterville-Kaskaskia',
		                                                                    'Cooks Mill-Kaskaskia',
		                                                                    'Cowden-Kaskaskia',
		                                                                    'Fairman-E Fork', 
		                                                                    'Fayetteville-Kaskaskia',
		                                                                    'Freeburg-Silver Cr',
		                                                                    'Hecker-Richland Cr',
		                                                                    'Hoffman-Crooked Cr',
		                                                                    'Lovington-W Okaw',
		                                                                    'Mulberry Grove-Hurricane Cr',
		                                                                    'Nav Pool-Kaskaskia',
		                                                                    'Nav TW-Kaskaskia',
		                                                                    'Pierron-Shoal Cr',
		                                                                    'Posey-Kaskaskia',
		                                                                    'Ramsey-Kaskaskia',
		                                                                    'Red Bud-Kaskaskia',
		                                                                    'Lk Shelbyville-Kaskaskia',
		                                                                    'Shelbyville TW-Kaskaskia',
		                                                                    'Shelbyville-Robinson Cr',
		                                                                    'Vandalia-Kaskaskia',
		                                                                    'Venedy Station-Kaskaskia',
		                                                                    'Eureka-Meramec', 
		                                                                    'High Gate-Bourbeuse', 
		                                                                    'Irondale-Big',
		                                                                    'Richwoods-Big', 
		                                                                    'Steelville-Meramec', 
		                                                                    'Sullivan-Meramec',
		                                                                    'Union-Bourbeuse', 
		                                                                    'St Charles-Missouri',
		                                                                    'Alton-Mississippi', 
		                                                                    'Cape Girardeau-Mississippi',
		                                                                    'Chester-Mississippi', 
		                                                                    'Grafton-Mississippi', 
		                                                                    'Grand Tower-Mississippi', 
		                                                                    'LD 22 TW-Mississippi',
		                                                                    'LD 24 Pool-Mississippi',
		                                                                    'LD 24 TW-Mississippi',
		                                                                    'LD 25 Pool-Mississippi',
		                                                                    'LD 25 TW-Mississippi',
		                                                                    'LD 27 Pool-Mississippi', 
		                                                                    'LD 27 TW-Mississippi', 
		                                                                    'Louisiana-Mississippi',
		                                                                    'Mel Price Pool-Mississippi',
		                                                                    'Mel Price TW-Mississippi', 
		                                                                    'Mosier Ldg-Mississippi', 
		                                                                    'St Louis-Mississippi',
		                                                                    'Thebes-Mississippi',
		                                                                    'Ashburn-Salt',
		                                                                    'Frankford-Spencer Cr',
		                                                                    'Hagers Grove-N Fork Salt',
		                                                                    'Holliday-Mid Fork Salt',
		                                                                    'Madison-Elk Fork Salt',
		                                                                    'New London-Salt',
		                                                                    'Norton Bridge-Salt',
		                                                                    'Mark Twain Lk TW-Salt'
		                                                                    'Paris-Crooked Cr',
		                                                                    'Perry-Lick Cr',
		                                                                    'Santa Fe-S Fork Salt',
		                                                                    'Santa Fe-Long Branch',
		                                                                    'Shelbina-N Fork Salt',
		                                                                    'Rend Lk-Big Muddy',
		                                                                    'Sub-Big Muddy',
		                                                                    'Sub-Casey Fork',
		                                                                    'Carlyle Lk-Kaskaskia',
		                                                                    'Mark Twain Lk-Salt',
		                                                                    'ReReg Pool-Salt',
		                                                                    'Wappapello Lk-St Francis'),
		
		                                    'Parameters'            : ('StageRev', 'Stage29'),
		                                    'Version'                   : ('lrgsShef-rev', '29'),
		                                    'None'                      : 'None'
                                },
                    }

#==================================================================================================================
# created a delete function to replace ElevRev values and associated quality code to StageRev and Stage29 and save back to database

def DeleteFunction(ElevTSC, StageTSC,  mysdate, myedate):

	# check interval of selected Elev TSC
	interval =  ElevTSC.interval
	print 'interval = ' + str(interval)

	print 'DeleteFunction: Elev Interval = ' + str(ElevTSC.interval)

	# check to see  if there is data at the start date. if the interval is 60,30,15, replace to these
	if int(interval) == 60:
		teod = mysdate.replace('0000','0100')
		TestTSCElev= db.get(ElevTSC.fullName,mysdate, teod)
		TestTSCStage= db.get(StageTSC.fullName,mysdate, teod)
	elif int(interval) == 30:
		teod = mysdate.replace('0000','0030')
		TestTSCElev= db.get(ElevTSC.fullName,mysdate, teod)	
		TestTSCStage= db.get(StageTSC.fullName,mysdate, teod)
	elif int(interval) == 15:
		teod = mysdate.replace('0000','0015')
		TestTSCElev= db.get(ElevTSC.fullName,mysdate, teod)	
		TestTSCStage= db.get(StageTSC.fullName,mysdate, teod)
	else:
		pass
	

	# replace time to corresponding elev interval 
	print 'teod = ' + str(teod)

	# what is the ts for elev and stage
	print 'TestTSCElev = '    + str(TestTSCElev)
	print 'TestTSCStage = ' + str(TestTSCStage)
	
	# what is the number of data point in that interval
	print 'len(TestTSCElev.values) = '    + str(len(TestTSCElev.values))	
	print 'len(TestTSCStage.values) = ' + str(len(TestTSCStage.values))	
	
	# print out the fullname for elev and stage
	print 'ElevTSC.fullName = '    + ElevTSC.fullName
	print 'StageTSC.fullName = ' + StageTSC.fullName

	# check to see if you have data at the start date. exit if you dont have data
	if len(TestTSCElev.values) < 1 :
		MessageBox.showInformation('No Data at Beginning at Time Step. \nChange Time Window', 'Alert')
		sys.exit()
	if len(TestTSCStage.values) < 1 :
		MessageBox.showInformation('No Data at Beginning at Time Step. \nChange Time Window', 'Alert')
		sys.exit()

	# prepare mysdate and myedate for file save
	mysdate = mysdate.replace(' ',' ') 
	print 'mysdate = ' + str(mysdate)
	
	myedate = myedate.replace(' ',' ') 
	print 'myedate = ' + str(myedate)

	# prepare naming for saved text file
	TextFile = open('C:\wc\data_editing\data_deleted_' +  StageTSC.fullName +  ' - '  + mysdate + ' - ' +  myedate + '.txt', 'w' )
	

	print '*******************************************'
	print '****************** Loop Cascade Delete'
	print '*******************************************'

	# set counter to 0 as a start
	counter = 0

	# find total number of values for the time selected
	maxval = len(ElevTSC.values) #maxval = len(StageTSC.values)
	print 'maxval = ' + str(maxval)

	# do the while loop for all the values in tsc
	while counter < maxval:
		try:
			ElevVal = ElevTSC.values[counter]
			print 'ElevVal = ' + str(ElevVal)
		except:
			ElevVal = -3.40282346639e+38 

		# if ElevVal < -1000000 which indicate missing data with value of -3.40282346639e+38 
		if ElevVal < -1000000:
			print '-------------------------- ElevVal < -1000000'
			print 'counter = ' + str(counter)

			# date time
			dt = StageTSC.times[counter]
			print 'dt = StageTSC.times[counter] = ' + str(dt) 

			# date time hec
			date_time = HecTime();  date_time.set(dt)
			print 'date_time = ' +  str(date_time)

			# What is the data will be deleted
			DeletedData = str( StageTSC.values[counter]) + ' - ' + str(date_time) + '\n'

			print 'data will be deleted in StageTSC= ' + str(DeletedData)
			
			# BEFORE
			print  'StageTSC.value[counter] BEFORE = ' +  str(StageTSC.values[counter])
			print 'StageTSC.quality[counter] BEFORE = ' + str(StageTSC.quality[counter])

			# Remove protection flag in StageRev and Stage29
			StageTSC.quality[counter] = QualityTx.clearProtected_int(StageTSC.quality[counter])

			# write to txt file
			TextFile.write(DeletedData)
			
			print '***'

			# setup ElevTSC to be replace stage rev
			try:
				print  'ElevTSC.values[counter] (to be replace with this) = '+ str( ElevTSC.values[counter])
				print 'ElevTSC.quality[counter] (to be replace with this) = ' + str(ElevTSC.quality[counter])
			except:
				print 'Exception' + str(ElevVal)
				print 5

			# Remove missing by setting StageTSC = ElevTSC
			try:	
				#StageTSC.values[counter] = ElevTSC.values[counter]
				#StageTSC.quality[counter] = 5

				# TODO: when cascade data (protect/unprotect), dont cascade protection section while keep everything else the same!!! 
				# Quality Code 	Screened ID 	Validity ID 	Range ID 	Changed ID 	Repl Cause ID 		Repl Method ID 	Test Failed ID 		Protection ID
				# 2147483653		CREENED		MISSING		NO_RANGE	ORIGINAL	NONE			NONE			NONE			PROTECTED

				# have to hard coded a quality code of "5" because NOT ABLE TO OVERWRITE DATA WITH QUALITY 1 (SCREENED) WITH QUALITY 0 (UNSCREENED).
				if ElevTSC.quality[counter] == 1 or ElevTSC.quality[counter] == 0:
					StageTSC.values[counter] = ElevTSC.values[counter]
					StageTSC.quality[counter] = 5
				else:
					StageTSC.values[counter] = ElevTSC.values[counter]
					StageTSC.quality[counter] = ElevTSC.quality[counter]
			except:
				StageTSC.values[counter] = ElevVal
				StageTSC.quality[counter] = 5

		        print '***'
		        
			# AFTER	
			print  'StageTSC.value[counter] AFTER = ' +  str(StageTSC.values[counter])
			print  'StageTSC.quality[counter] AFTER = ' + str(StageTSC.quality[counter])
			
				
		counter += 1
		#counter = counter + 1

	TextFile.close()
	db.put(StageTSC)
	return 
	
#=========================================================
# Pick a station from a List
location_id_groupChoices = [  'Allenville-Whitley Cr','Alton-Mississippi','Arnold-Meramec','Ashburn-Salt','Birds Point-Mississippi','Breese-Shoal Cr','Brownstown-Hickory Cr','Byrnesville-Big','Cairo-Ohio',
						'Cape Girardeau-Mississippi','Carlyle Lk TW-Kaskaskia','Carlyle Lk-Kaskaskia','Carlyle-Kaskaskia','Champion City-Bourbeuse','Chester-Mississippi','Chesterville-Kaskaskia','Commerce-Mississippi',
						'Cooks Mill-Kaskaskia','Cowden-Kaskaskia','Desloge-Big','Engineers Depot-Mississippi','Eureka-Meramec','Fairman-E Fork','Fayetteville-Kaskaskia','Fisk-St Francis',
						'Florence-Illinois','Frankford-Spencer Cr','Fredericktown-L St Francis','Freeburg-Silver Cr','Grafton-Mississippi','Grand Tower-Mississippi','Grays Pt-Mississippi','Hagers Grove-N Fork Salt',
						'Hardin-Illinois','Hecker-Richland Cr','Herculaneum-Mississippi','Hermann-Missouri','High Gate-Bourbeuse','Hoffman-Crooked Cr', 'Holliday-Mid Fork Salt','Iron Bridge-St Francis','Irondale-Big',
						'Jefferson Brks-Mississippi','LD 22 TW-Mississippi','LD 22-Mississippi','LD 24 Pool-Mississippi','LD 24 TW-Mississippi',
						'LD 25 Pool-Mississippi','LD 25 TW-Mississippi','LD 27 Pool-Mississippi','LD 27 TW-Mississippi','Lk Shelbyville-Kaskaskia','Louisiana-Mississippi','Lovington-W Okaw','Madison-Elk Fork Salt',
						'Mark Twain Lk TW-Salt','Mark Twain Lk-Salt','Mel Price Pool-Mississippi','Mel Price TW-Mississippi','Meredosia-Illinois','Millcreek-St Francis','Moccasin Springs-Mississippi',
						'Mosier Ldg-Mississippi','Mt Vernon-Big Muddy','Mt Vernon-Casey Fork','Mulberry Grove-Hurricane Cr','Murphysboro-Big Muddy','Nav Pool-Kaskaskia','Nav TW-Kaskaskia','New London-Salt',
						'Norton Bridge-Salt','Pacific-Meramec','Paris-Crooked Cr','Patterson-St Francis','Perry-Lick Cr','Pierron-Shoal Cr','Plumfield-Big Muddy','Posey-Kaskaskia',
						'Price Ldg-Mississippi','Pump Sta 1-Wood River E Alton','Ramsey-Kaskaskia','ReReg Pool-Salt','Red Bud-Kaskaskia','Red Rock Ldg-Mississippi','Rend Lk TW-Big Muddy','Rend Lk-Big Muddy',
						'Richwoods-Big','Roselle-St Francis','Saco-St Francis','Sam A Baker Park-Big Cr','Sand Ridge-Big Muddy','Santa Fe-Long Branch','Santa Fe-S Fork Salt','Shelbina-N Fork Salt',
						'Shelbyville TW-Kaskaskia','Shelbyville-Robinson Cr','St Charles-Missouri','St Francis-St Francis','St Louis-Mississippi','Steelville-Meramec','Sub-Big Muddy','Sub-Casey Fork',
						'Sullivan-Meramec','Thebes-Mississippi','Thompson Ldg-Mississippi','Troy-Cuivre','Union-Bourbeuse','Valley City-Illinois','Valley Park-Meramec','Vandalia-Kaskaskia',
						'Venedy Station-Kaskaskia','Waltonville-Rayse Cr','Wappapello Lk-St Francis','Pittsburg-Kaskaskia' ]
						
location_id_Selected = JOptionPane.showInputDialog(None,"Choose a station to cascade delete","MVS_Deletor",JOptionPane.PLAIN_MESSAGE,None,location_id_groupChoices,location_id_groupChoices[0])


#=========================================================
print  'location_id_Selected = ' +  str(location_id_Selected)

#=========================================================
# select date option 2: hard coded in mysdate and myedate
mysdate = '15Jan2000 1930'
myedate = '31Dec2008 2400'
#=========================================================

#sys.exit()

#******************************************************
print 'mysdate = ' + mysdate
print 'myedate = ' + myedate
#******************************************************			


#******************************************************	
# Open the CWMS database and set the timezone
db = DBAPI.open()

# Set Timezone = GMT, UsCentralTz = TimeZone.getTimeZone('US/Central'), Gmt6Tz = TimeZone.getTimeZone('GMT-06:00')
db.setTimeZone('GMT')

# Set time window with start and end date
db.setTimeWindow(mysdate,myedate)
db.setOfficeId('MVS')

# override protected data
db.setStoreRule('Replace All')
db.setOverrideProtection(True)

# NEW: cascade with remove protection. scott hoffman
db.setTrimMissing(False)


#=========================================================
print '******************************************* TIER1'

# Special Case: Cairo-Ohio is the only location that have 1Hour time internal
if location_id_Selected in DataDict['TIER1']['Station']:
	check_delete = 1

	if location_id_Selected == 'Cairo-Ohio':
		ElevTSC = db.get (location_id_Selected + '.Elev.Inst.1Hour.0.lrgsShef-rev')
		StageTSC = db.get (location_id_Selected + '.Stage.Inst.1Hour.0.lrgsShef-rev')
	elif location_id_Selected == 'St Francis-St Francis':
		ElevTSC = db.get (location_id_Selected + '.Elev.Inst.1Hour.0.lrgsShef-rev')
		StageTSC = db.get (location_id_Selected + '.Stage.Inst.1Hour.0.lrgsShef-rev')
	elif location_id_Selected == 'Fisk-St Francis':
		ElevTSC = db.get (location_id_Selected + '.Elev.Inst.1Hour.0.lrgsShef-rev')
		StageTSC = db.get (location_id_Selected + '.Stage.Inst.1Hour.0.lrgsShef-rev')
	else:
		try:	
			ElevTSC = db.get (location_id_Selected + '.Elev.Inst.30Minutes.0.lrgsShef-rev')
			StageTSC = db.get (location_id_Selected + '.Stage.Inst.30Minutes.0.lrgsShef-rev')
		except:
			ElevTSC = db.get (location_id_Selected + '.Elev.Inst.15Minutes.0.lrgsShef-rev')
			StageTSC = db.get (location_id_Selected + '.Stage.Inst.15Minutes.0.lrgsShef-rev')
				
	#print  ElevTSC
	#print StageTSC
	
	print len(ElevTSC.values), " elev count"
	print len(StageTSC.values), " stage count"

	if check_delete == 1:
		print 'check_delete==1 > Run DeleteFunction'
		DeleteFunction(ElevTSC, StageTSC, mysdate, myedate)
		print 'check_delete = ' +  str(check_delete)
	print 'done'	

print '******************************************* TIER2'

if location_id_Selected in DataDict['TIER2']['Station']:
	# Special Case: Cairo-Ohio is the only location that have 1Hour time internal
	try:
		if location_id_Selected == 'Cairo-Ohio':
			ElevTSC = db.get (location_id_Selected + '.Elev.Inst.1Hour.0.lrgsShef-rev')
		else:
			ElevTSC = db.get (location_id_Selected + '.Elev.Inst.30Minutes.0.lrgsShef-rev')
	except:
		ElevTSC = db.get (location_id_Selected + '.Elev.Inst.15Minutes.0.lrgsShef-rev')
			
	for Param in DataDict['TIER2']['Parameters']:
		print 'Param = ' + Param

		# if check_delete = 0, no deletion
		check_delete = 0
		
		if Param == 'StageRev':
			check_delete_StageRev = 1

			# setting up TS for StageTSC
			try:
				try:
					StageTSC = db.get (location_id_Selected +   '.Stage.Inst.30Minutes.0.lrgsShef-rev')					
				except:
					StageTSC = db.get (location_id_Selected +  '.Stage.Inst.15Minutes.0.lrgsShef-rev')			
			except:
				print 'StageRev data type not found = ' +  location_id_Selected +  '.Stage.Inst.30Minutes.0.lrgsShef-rev'
				check_delete_StageRev = 0

			# delete data
			if check_delete_StageRev == 1:
				print 'check_delete_StageRev==1 > Run DeleteFunction'
				DeleteFunction(ElevTSC, StageTSC, mysdate, myedate)
				print 'check_delete_StageRev = ' +  str(check_delete_StageRev)
			print 'done'

		# setting up TS for Stage29TSC	
		elif Param == 'Stage29':
			check_delete_Stage29 = 1
			try:
				try:
					StageTSC = db.get (location_id_Selected + '.Stage.Inst.30Minutes.0.29')
				except:
					StageTSC = db.get (location_id_Selected +  '.Stage.Inst.15Minutes.0.29')
			except:
				print 'Stage29 data type not found = ' +  location_id_Selected +  '.Stage.Inst.30Minutes.0.29'
				check_delete_Stage29 = 0
		
			if check_delete_Stage29 == 1:
				print 'check_delete_Stage29==1 > Run DeleteFunction' 
				DeleteFunction(ElevTSC, StageTSC, mysdate, myedate)
				print 'check_delete_Stage29 = ' +  str(check_delete_Stage29)
			print 'done'

			
		print ElevTSC
		print StageTSC


#******************************************************	
print '='
print '='
print '='
print '=================================================================================='
print '====================================== END CASCADE DELETE  LOG RUN ======================='
print '================================================================================== '
print '='
print '='
print '='

db.close()

MessageBox.showInformation('Completed', 'Alert')
			
