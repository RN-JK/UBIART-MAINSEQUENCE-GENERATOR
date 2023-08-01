import json, random

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
    mt=json.load(open('input/'+map.lower()+'_musictrack.tpl.ckd'))
    dtape=json.load(open('input/'+map.lower()+'_tml_dance.dtape.ckd'))
    startbeat=mt['COMPONENTS'][0]['trackData']['structure']['startBeat']
    endbeat=mt['COMPONENTS'][0]['trackData']['structure']['endBeat']
    starttimes=[]
    timeplusduration=[]
    
    try:
        tape=json.load(open('input/'+map.lower()+'_mainsequence.tape.ckd'))
    except:
        tape={"__class": "Tape","Clips": [],"TapeClock": 0,"TapeBarCount": 1,"FreeResourcesAfterPlay": 0,"MapName": map,"SoundwichEvent": ""}
    
    if setting['HideUserInterfaceClip']['isActive']==True:
        if 'HideUserInterfaceClip' in tape['Clips']:
            continue
        else:
            for clip in dtape['Clips']:
                starttimes.append(clip['StartTime'])
                timeplusduration.append(clip['StartTime']+clip['Duration'])
            hideuioffset=setting['HideUserInterfaceClip']['offset']*24
            endduration=endbeat*24
            tape['Clips'].append({"__class": "HideUserInterfaceClip","Id": random.randint(10000000, 99999999),"TrackId": random.randint(10000000, 99999999),"IsActive": 1,"StartTime": startbeat*24,"Duration": int(min(starttimes))-hideuioffset,"EventType": 18,"CustomParam": ""})
            tape['Clips'].append({"__class": "HideUserInterfaceClip","Id": random.randint(10000000, 99999999),"TrackId": random.randint(10000000, 99999999),"IsActive": 1,"StartTime": max(timeplusduration)+hideuioffset,"Duration": endbeat*24,"EventType": 18,"CustomParam": ""})
            tape['Clips'][-1]['Duration']=endduration-tape['Clips'][-1]['StartTime']

    if setting['VibrationClip']['isActive']==True:
        if 'VibrationClip' in tape['Clips']:
            continue
        else:
            for beat in range(len(mt['COMPONENTS'][0]['trackData']['structure']['markers'])):
                if setting['VibrationClip']['startOffset']>=beat:
                    continue
                else:
                    tape['Clips'].append({"__class": "VibrationClip","Id": random.randint(10000000, 99999999),"TrackId": random.randint(10000000, 99999999),"IsActive": 1,"StartTime": beat*24,"Duration": setting['VibrationClip']['duration'],"VibrationFilePath": setting['VibrationClip']['path'],"Loop": 0,"DeviceSide": 0,"PlayerId": -1,"Context": 0,"StartTimeOffset": 0,"Modulation": 0.5})

    json.dump(tape,open('output/'+map.lower()+'_mainsequence.tape.ckd','w'))