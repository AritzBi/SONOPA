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
			for rec in recommendations:
				print user,rec
				sendRecommendation(user, rec)


if __name__ == '__main__':

	while True:
		print 'matchmaking'
		makeMatchmaking()
		sleep(24 * 3600)



