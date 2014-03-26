import numpy as np
import matplotlib.pylab as plt
import datetime, requests
from bs4 import BeautifulSoup

teams = ['TOR', 'BRK', 'NYK', 'BOS', 'PHI', 'IND', 'CHI', 'DET', 'CLE', 'MIL', 'MIA', 'WAS', 'CHA', 'ATL', 'ORL', 'OKC', 'POR', 'MIN', 'DEN', 'UTA', 'LAC', 'GSW', 'PHO', 'SAC', 'LAL', 'SAS', 'HOU', 'DAL', 'MEM', 'NOH']

BASE_URL = 'http://www.basketball-reference.com/teams/'
URL_TAIL = '/2009_games.html'


def updateRecord(record, gamedate, prev_date, result):
	difference = (gamedate - prev_date).days
	if result == 'W':
		record[0] += 1
		if difference == 1:
			record[2] += 1
	if result == 'L':
		record[1] += 1
		if difference == 1:
			record[3] += 1
	return record

teams.sort()
ovrWinPct = []
b2bWinPct = []
ovrRecs = []
b2bRecs = []

for x in teams:
	winloss = [0.0,0.0,0.0,0.0] #first two are overall record, second two are in back-to-backs
	url = BASE_URL + x + URL_TAIL
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	table = soup.tbody
	rows = table.find_all('tr')
	prev_date = datetime.date(1900, 1, 1)
	for row in rows:
		if 'thead' not in row['class']:
			data = row.find_all('td')
			date_array = data[1]['csk'].split('-')
			gamedate = datetime.date(int(date_array[0]), int(date_array[1]), int(date_array[2]))
			result = data[5].text
			winloss = updateRecord(winloss, gamedate, prev_date, result)
			prev_date = gamedate
	ovrPct = winloss[0]/(winloss[0]+winloss[1])
	ovrRecStr = str(int(winloss[0])) + '-' + str(int(winloss[1]))
	b2bPct = winloss[2]/(winloss[2]+winloss[3])
	b2bRecStr = str(int(winloss[2])) + '-' + str(int(winloss[3]))
	ovrWinPct.append(ovrPct)
	b2bWinPct.append(b2bPct)
	ovrRecs.append(ovrRecStr)
	b2bRecs.append(b2bRecStr)

teamrecs = []
i = 0
for team in teams:
	teamrecs.append(team + '\n' + b2bRecs[i])
	i = i + 1

ind = np.arange(0, 2*len(teams), 2)  # the x locations for the groups
width = 0.7       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

rects1 = ax.bar(ind, ovrWinPct, width, color='b')
rects2 = ax.bar(ind+width, b2bWinPct, width, color='r')

# add some

ax.set_ylabel('Win Percentage')
ax.set_title("Win Percentages in Back-to-Backs '08-'09")
ax.set_xticks(ind+width)
ax.set_xticklabels(teamrecs)

ax.legend( (rects1[0], rects2[0]), ('Overall', '2nd Night of B2B') ).draggable()

plt.show()
