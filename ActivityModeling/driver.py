# driver.py

import sys
import time
from pyke import knowledge_engine, krb_traceback, goal

engine = knowledge_engine.engine(__file__)

def run():
	engine.reset()
	try:
		fc_goal = goal.compile('sensor_data.processed($time, $activations, $concurrentActivations)')
		start_time = time.time()
		engine.activate('rule_system')
		fc_end_time = time.time()
		fc_time = fc_end_time - start_time
		print "Starting the proof"
		with fc_goal.prove(engine) as gen:
			for vars, plan in gen:
				#print vars['activations']
				#print vars['concurrentActivations']
				print vars
		print 
		print "done"
		engine.print_stats()
	except StandardError:
		krb_traceback.print_exc()
		sys.exit(1)

