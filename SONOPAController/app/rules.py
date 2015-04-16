import json
def computeTimeinterval(sensor_id, start_time, end_time):
	return True
with open('../rules.json') as rules_file:
    rules_json=json.load(rules_file)
    rules=[]
    for rule_json in rules_json:
    	for condition in rule_json[0]:
    		print condition
    		if condition['condition_type']=="Time interval":
    			continue_loop=computeTimeinterval(condition['sensor_id'],condition['start_time'],condition['end_time'])
    			if not continue_loop:
    				break;
    	for consequence in rule_json[1]:
			print consequence
			if consequence['consequence_type']=='State':
				print "Set state: "+consequence['state']
			elif consequence['consequence_type']=='Message':   		
				print "Message: "+consequence['message']