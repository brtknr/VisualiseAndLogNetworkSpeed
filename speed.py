#!/home/bharat.kunwar/Anaconda3/bin/python

"""
	Analyses network log and produces a PDF report.
	Compatible with Python 3.3 and 2.7.
"""	

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# =======================================================

infile = '/home/bharat.kunwar/Network/_Speed/5mins.log'
outfile = '/home/bharat.kunwar/Network/_Speed/report.pdf'
logfreq = 5 # minutes

# =======================================================

date = []
download = []
upload = []
minutes = []
dayofweek = []
daysofweek = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']

with open(infile) as f:
	for line in f.readlines():
		dow = line[:3]
		hhmm = line[11:16]
		mins = sum([int(i)*j for i,j in zip(hhmm.split(':'),[60,1])])
		date.append(dow+' '+hhmm)
		dayofweek.append(daysofweek.index(dow)+mins/60/24)
		minutes.append(mins)

		parts = line[29:].split(' ')

		if parts[0] == 'Ping:':
			download.append(float(parts[4]))
			upload.append(float(parts[7]))
		else:
			download.append(0.)
			upload.append(0.)

# upbins = int(max(upload)*2)
# downbins = int(max(download)*2)
# weeklybins = 7*10
# hourlybins = 24*10
upbins = 50
downbins = 50
weeklybins = 50
hourlybins = 50

weights = np.ones_like(upload)/float(len(date))
uday = set(dayofweek)
weekly = 60//logfreq*24*7
hourly = 60//logfreq

plt.figure(figsize=(14,12))


plt.subplot(311)
plt.plot(upload[-weekly:],label='up')
plt.plot(download[-weekly:],label='down')
# Only show the last 7 days, ticks showing every 6 hours
lastweek = date[-(weekly+1):]
lastweekrange = range(weekly+1)
plt.xticks(lastweekrange[::hourly*6],lastweek[::hourly*6],rotation=40,ha='right')
plt.xlim(min(lastweekrange),max(lastweekrange))
plt.ylabel('Mbits/s')

plt.subplot(334)
plt.hist(upload,bins=upbins,histtype='step',label='up')
plt.hist(download,bins=downbins,histtype='step',label='down')
plt.xlabel('Mbits/s')
plt.ylabel('P.D.F.')

plt.subplot(337)
plt.hist2d(upload,download,bins=(upbins,downbins),norm=LogNorm())
plt.xlabel('up Mbits/s')
plt.ylabel('down Mbits/s')
plt.colorbar()

plt.subplot(335)
plt.hist2d(dayofweek,download,bins=(weeklybins,downbins),norm=LogNorm())
plt.xticks(range(7),daysofweek)
plt.xlabel('Day of week')
plt.ylabel('down Mbits/s')
plt.colorbar()

plt.subplot(338)
plt.hist2d(dayofweek,upload,bins=(weeklybins,upbins),norm=LogNorm())
plt.xticks(range(7),daysofweek)
plt.xlabel('Day of week')
plt.ylabel('up Mbits/s')
plt.colorbar()

plt.subplot(336)
plt.hist2d(minutes,download,bins=(hourlybins,downbins),norm=LogNorm())
plt.xticks(minutes[::hourly],[m//60 for m in minutes[::hourly]],rotation=90)
plt.xlabel('Hour of day')
plt.ylabel('down Mbits/s')
plt.colorbar()

plt.subplot(339)
plt.hist2d(minutes,upload,bins=(hourlybins,upbins),norm=LogNorm())
plt.xticks(minutes[::hourly],[m//60 for m in minutes[::hourly]],rotation=90)
plt.xlabel('Hour of day')
plt.ylabel('up Mbits/s')
plt.colorbar()

plt.tight_layout()

plt.savefig(outfile,bbox_inches='tight')

print('Success.')