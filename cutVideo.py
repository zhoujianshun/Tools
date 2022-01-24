
import subprocess

def getVideoTime(path):
    cmdline = "ffprobe '%s' -show_entries format=duration -of compact=p=0:nk=1 -v 0" % path
    print(cmdline)
    gettime=subprocess.check_output(cmdline, shell=True)
    timeT=int(float(gettime.strip()))
    return timeT

videoPath='/Users/zhoujianshun/Documents/study/Python/5.mp4'
cutTime=4 #切割为4秒没段
timeT=getVideoTime(videoPath)
firstTime=0
index=1
while firstTime<timeT:
    cmdLine = 'ffmpeg -ss %s -i %s -c copy -t %s %s.mp4 -loglevel quiet -y'%(firstTime,videoPath,cutTime,'cut_%s'%index)
    print(cmdLine)
    returnCmd = subprocess.call(cmdLine, shell=True)
    firstTime+=cutTime
    index+=1

