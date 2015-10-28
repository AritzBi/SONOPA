"""
Copyright (c) 2015 Aritz Bilbao, Aitor Almeida

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@author: "Aritz Bilbao, Aitor Almeida"
@contact: aritzbilbao@deusto.es, aitor.almeida@deusto.es
"""

from snRequester import getProfile,getUsers, sendRecommendation
from profile_comparator import matchmaking
from datetime import datetime
from time import sleep

def makeMatchmaking():
	users=getUsers()
	total_users = {}
	print 'Recovering all the locations:', len(users)
	for i, user in enumerate(users):
		print i, 'of', len(users)
		profile=getProfile(user['username'])
		if profile:
			try:
				user_location = profile['location']
				try:
					total_users[location].append({user['username']:profile})
				except:
					total_users[profile['location']] = {user['username']:profile}
			except KeyError:
				print 'User has no location'
				pass
		
			
	print 'Starting the matchmaking process'
	for location in total_users:
		print "Finding matches in:",location
		users = total_users[location]
		results = matchmaking(total_users[location])
		if len(results)==0:
			print "No matches found in:",location
		for user in results:
			recommendations = results[user]
			user_connections = total_users[location][user]['connections']
			for rec in recommendations:
				if rec not in user_connections:
					print user,rec
					sendRecommendation(user, rec)


if __name__ == '__main__':

	while True:
		print 'matchmaking'
		makeMatchmaking()
		sleep(24 * 3600)



