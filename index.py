import os, json, random

class TrackId:
    hideuserinterface=random.randint(10000000, 99999999)
    vibration=random.randint(10000000, 99999999)

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
        mt={"COMPONENTS": [{"trackData": {"structure": {"markers": []}}}]} #empty
    try:
        dtape=json.loads(readCKD('input/'+map.lower()+'_tml_dance.dtape.ckd'))
    except:
        dtape={"__class": "Tape","Clips": [],"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": map,"SoundwichEvent": ""}  #empty
    startbeat=mt['COMPONENTS'][0]['trackData']['structure']['startBeat']
    endbeat=mt['COMPONENTS'][0]['trackData']['structure']['endBeat']
    starttimes=[]
    timeplusduration=[]
    
    try:
        tape=json.loads(readCKD('input/'+map.lower()+'_mainsequence.tape.ckd'))
    except:
        tape={"__class": "Tape","Clips": [],"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": map,"SoundwichEvent": ""}  #empty
    
    if setting['HideUserInterfaceClip']['isActive']==True:
        if not 'Clips' in tape: #sometimes, the 'Clips' array doesn't exist.
            tape['Clips']=[]
        if 'HideUserInterfaceClip' in tape['Clips']:
            continue
        else:
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
        if not 'Clips' in tape: #sometimes, the 'Clips' array doesn't exist.
            tape['Clips']=[]
        if 'VibrationClip' in tape['Clips']:
            continue
        else:
            for beat in range(len(mt['COMPONENTS'][0]['trackData']['structure']['markers'])):
                if setting['VibrationClip']['startOffset']>=beat:
                    continue
                else:
                    tape['Clips'].append({"__class": "VibrationClip","Id": random.randint(10000000, 99999999),"TrackId": TrackId.vibration,"IsActive": 1,"StartTime": beat*24,"Duration": setting['VibrationClip']['duration'],"VibrationFilePath": setting['VibrationClip']['path'],"Loop": 0,"DeviceSide": 0,"PlayerId": -1,"Context": 0,"StartTimeOffset": 0,"Modulation": 0.5})

    if setting['Settings']['MapDirectories']==True:
        os.makedirs('output/'+map.lower()+'/cinematics',exist_ok=True)
        json.dump(tape,open('output/'+map.lower()+'/cinematics/'+map.lower()+'_mainsequence.tape.ckd','w'))
    else:
        json.dump(tape,open('output/'+map.lower()+'_mainsequence.tape.ckd','w'))
