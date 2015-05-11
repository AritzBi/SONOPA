from snRequester import getProfile,getUsers, sendRecommendation
from profile_comparator import matchmaking
from datetime import datetime
from time import sleep

def makeMatchmaking():
	users=getUsers()
	total_users = {}
	for user in users:
		profile=getProfile(user)
		if profile:
			try:
				total_users[profile['location']].append(profile)
			except:
				print profile
				print ''
				print profile['location']
				total_users[profile['location']] = [profile]

	for location in total_users:
		users = total_users[location]
		results = matchmaking(total_users[location])
		for user in results:
			recommendations = results[user]
			for rec in recommendations:
				sendRecommendation(user, rec)


if __name__ == '__main__':

	while True:
		print 'matchmaking'
		makeMatchmaking()
		sleep(24 * 3600)



