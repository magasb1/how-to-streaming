import argparse
import subprocess

parser = argparse.ArgumentParser(description='Pull HLS and restream over SRT.')
parser.add_argument('hlsurl')
parser.add_argument('address')
parser.add_argument('--srtmode', dest='srtmode', help='SRT mode [caller|listener]. Default is listener')
parser.add_argument('--streamid', dest='streamid', help='SRT StreamId [string]')
parser.add_argument('--with-debug', dest='debug', action='store_true')
args = parser.parse_args()

srtmode = "&mode=listener"
if args.srtmode == "caller":
  srtmode = ""

srtoutput = "-f mpegts srt://%s?pkt_size=1316%s&streamid=publish:%s" % (args.address, srtmode, args.streamid)

ffmpeg = "ffmpeg -fflags +genpts -re -i %s -strict -2 -y -acodec copy -vcodec copy %s " % (args.hlsurl, srtoutput)

if args.debug:
  print("%s" % ffmpeg)
  print(ffmpeg.split())

p1 = subprocess.Popen(ffmpeg.split())
output,err = p1.communicate()

# python example-ffmpeg.py https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/hzDaPl9KkIbkcZFUvWFfg/master.m3u8 example.com:8890 --srtmode caller --streamid demo