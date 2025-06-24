import os, json, random

class TrackId:
    hideuserinterface=random.randint(10000000, 99999999)
    soundset=random.randint(10000000, 99999999)
    vibration=random.randint(10000000, 99999999)

def generateTPL(tpl):
    tpl['__class']='Actor_Template'
    tpl['WIP']=0
    tpl['LOWUPDATE']=0
    tpl['UPDATE_LAYER']=0
    tpl['PROCEDURAL']=0
    tpl['STARTPAUSED']=0
    tpl['FORCEISENVIRONMENT']=0
    tpl['COMPONENTS']=[]

def SoundComponent_Template(mapname, ambname):
    return {
			"__class": "SoundComponent_Template",
			"soundList": [
				{
					"__class": "SoundDescriptor_Template",
					"name": "amb_"+mapname.lower()+"_"+ambname.lower(),
					"volume": 0,
					"category": "amb",
					"limitCategory": "",
					"limitMode": 0,
					"maxInstances": 4294967295,
					"files": [
						"world/maps/"+mapname.lower()+"/audio/amb/amb_"+mapname.lower()+"_"+ambname.lower()+".wav"
					],
					"serialPlayingMode": 0,
					"serialStoppingMode": 0,
					"params": {
						"__class": "SoundParams",
						"loop": 0,
						"playMode": 1,
						"playModeInput": "",
						"randomVolMin": 0,
						"randomVolMax": 0,
						"delay": 0,
						"randomDelay": 0,
						"pitch": 1,
						"randomPitchMin": 1,
						"randomPitchMax": 1,
						"fadeInTime": 0,
						"fadeOutTime": 0,
						"filterFrequency": 0,
						"filterType": 2,
						"transitionSampleOffset": 0
					},
					"pauseInsensitiveFlags": 0,
					"outDevices": 4294967295,
					"soundPlayAfterdestroy": 0
				}
			]
		}

def readCKD(ckd):
    jsonbytes=open(ckd,'rb')
    bytedata=jsonbytes.read()
    bytelength=len(bytedata)
    uselessbyte=bytedata[bytelength-1:]
    if uselessbyte==b'\x00':
        jsondata=bytedata[:bytelength-1]
    else:
        jsondata=bytedata
    return jsondata.decode('utf-8')

setting=json.load(open('input.json'))

for map in setting['Maps']:
    print(map)
    try:
        mt=json.loads(readCKD('input/'+map.lower()+'_musictrack.tpl.ckd'))
    except:
        mt={"COMPONENTS": [{"trackData": {"structure": {"markers": [], "signatures": [], "sections": [], "startBeat": 0, "endBeat": 0, "videoStartTime": 0.0}}}]} #empty
    try:
        dtape=json.loads(readCKD('input/'+map.lower()+'_tml_dance.dtape.ckd'))
    except:
        dtape={"__class": "Tape","Clips": [],"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": map,"SoundwichEvent": ""}  #empty
    startbeat=mt['COMPONENTS'][0]['trackData']['structure']['startBeat']
    endbeat=mt['COMPONENTS'][0]['trackData']['structure']['endBeat']
    videostarttime=mt['COMPONENTS'][0]['trackData']['structure']['videoStartTime']
    starttimes=[]
    timeplusduration=[]

    #amb tpls
    intro={}
    generateTPL(intro)
    intro['COMPONENTS'].append(SoundComponent_Template(map, 'intro'))

    full={}
    generateTPL(full)
    full['COMPONENTS'].append(SoundComponent_Template(map, 'full'))
    
    try:
        tape=json.loads(readCKD('input/'+map.lower()+'_mainsequence.tape.ckd'))
    except:
        tape={"__class": "Tape","Clips": [],"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": map,"SoundwichEvent": ""}  #empty
    
    if setting['HideUserInterfaceClip']['isActive']==True:
        ifhideuiexist=False
        if not 'Clips' in tape: #sometimes, the 'Clips' array doesn't exist.
            tape['Clips']=[]
        for clip in tape['Clips']:
            if 'HideUserInterfaceClip' in clip['__class']:
                ifhideuiexist=True
        if ifhideuiexist==False:
            for clip in dtape['Clips']:
                starttimes.append(clip['StartTime'])
                timeplusduration.append(clip['StartTime']+clip['Duration'])
            hideuioffset=setting['HideUserInterfaceClip']['offset']*24
            endduration=endbeat*24
            if not len(dtape['Clips'])==0:
                tape['Clips'].append({"__class": "HideUserInterfaceClip","Id": random.randint(10000000, 99999999),"TrackId": TrackId.hideuserinterface,"IsActive": 1,"StartTime": startbeat*24,"Duration": int(min(starttimes))-hideuioffset,"EventType": 18,"CustomParam": ""})
                tape['Clips'].append({"__class": "HideUserInterfaceClip","Id": random.randint(10000000, 99999999),"TrackId": TrackId.hideuserinterface,"IsActive": 1,"StartTime": max(timeplusduration)+hideuioffset,"Duration": endbeat*24,"EventType": 18,"CustomParam": ""})
                tape['Clips'][-1]['Duration']=endduration-tape['Clips'][-1]['StartTime']

    if setting['VibrationClip']['isActive']==True:
        ifvibrationexist=False
        if not 'Clips' in tape: #sometimes, the 'Clips' array doesn't exist.
            tape['Clips']=[]
        if 'VibrationClip' in tape['Clips']:
            continue
        for clip in tape['Clips']:
            if 'VibrationClip' in clip['__class']:
                ifvibrationexist=True
        if ifvibrationexist==False:
            for beat in range(len(mt['COMPONENTS'][0]['trackData']['structure']['markers'])):
                if setting['VibrationClip']['startOffset']>=beat:
                    continue
                else:
                    tape['Clips'].append({"__class": "VibrationClip","Id": random.randint(10000000, 99999999),"TrackId": TrackId.vibration,"IsActive": 1,"StartTime": beat*24,"Duration": setting['VibrationClip']['duration'],"VibrationFilePath": setting['VibrationClip']['path'],"Loop": 0,"DeviceSide": 0,"PlayerId": -1,"Context": 0,"StartTimeOffset": 0,"Modulation": 0.5})

    if setting['SoundSetClip']['isActive']==True:
        if not 'Clips' in tape: #sometimes, the 'Clips' array doesn't exist.
            tape['Clips']=[]

        #checking if intro amb exist
        ifintroexist=False
        if setting['SoundSetClip']['intro']==True:
            for clip in tape['Clips']:
                if 'SoundSetPath' in list(clip):
                    if 'amb_'+map.lower()+'_intro' in clip['SoundSetPath']:
                        ifintroexist=True

            if ifintroexist==False:
                if startbeat <= 0:
                    tape['Clips'].append({"__class": "SoundSetClip","Id": random.randint(10000000, 99999999),"TrackId": TrackId.soundset,"IsActive": 1,"StartTime": startbeat*24, "Duration": abs(startbeat)*24, "SoundSetPath": "world/maps/"+map.lower()+"/audio/amb/amb_"+map.lower()+"_intro.tpl", "SoundChannel": 0, "StartOffset": 0, "StopsOnEnd": 0, "AccountedForDuration": 0})

        if setting['SoundSetClip']['full']==True:
            tape['Clips'].append({"__class": "SoundSetClip","Id": random.randint(10000000, 99999999),"TrackId": TrackId.soundset,"IsActive": 1,"StartTime": startbeat*24, "Duration": abs(startbeat)+abs(endbeat)*24, "SoundSetPath": "world/maps/"+map.lower()+"/audio/amb/amb_"+map.lower()+"_full.tpl", "SoundChannel": 0, "StartOffset": 0, "StopsOnEnd": 0, "AccountedForDuration": 0})

    if setting['Settings']['MapDirectories']==True:
        if setting['SoundSetClip']['intro']==True:
            os.makedirs('output/'+map.lower()+'/audio/amb',exist_ok=True)
            json.dump(intro,open('output/'+map.lower()+'/audio/amb/amb_'+map.lower()+'_intro.tpl.ckd','w'))

        if setting['SoundSetClip']['full']==True:
            os.makedirs('output/'+map.lower()+'/audio/amb',exist_ok=True)
            json.dump(full,open('output/'+map.lower()+'/audio/amb/amb_'+map.lower()+'_full.tpl.ckd','w'))

        os.makedirs('output/'+map.lower()+'/cinematics',exist_ok=True)
        json.dump(tape,open('output/'+map.lower()+'/cinematics/'+map.lower()+'_mainsequence.tape.ckd','w'))

    else:
        if setting['SoundSetClip']['intro']==True:
            json.dump(intro,open('output/'+map.lower()+'/amb_'+map.lower()+'_intro.tpl.ckd','w'))

        if setting['SoundSetClip']['full']==True:
            json.dump(full,open('output/'+map.lower()+'/amb_'+map.lower()+'_full.tpl.ckd','w'))
        
        json.dump(tape,open('output/'+map.lower()+'_mainsequence.tape.ckd','w'))
