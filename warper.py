#!/usr/bin/env python
import json
import os
import time

import alfred
import batman
import d3mapbuilder
import nodedb

def wrapper(options):
	db = nodedb.NodeDB(int(time.time()))
	if options['mesh']:
		for mesh_interface in options['mesh']:
			bm = batman.batman(mesh_interface)
			db.parse_vis_data(bm.vis_data(options['alfred']))
			for gw in bm.gateway_list():
				db.mark_gateways([gw['mac']])
	else:
		bm = batman.batman()
		db.parse_vis_data(bm.vis_data(options['alfred']))
		for gw in bm.gateway_list():
			db.mark_gateways([gw['mac']])

	if options['aliases']:
		for aliases in options['aliases']:
			db.import_aliases(json.load(open(aliases)))
	
	if options['alfred']:
		db.import_aliases(alfred.alfred().fw_version())


	db.load_state('state.json') # FIXME
	db.prune_offline(time.time() - 10*24*60*60)
	db.dump_state('state.json') # FIXME

	return db
	

if __name__ == '__main__':
	options = {
		'alfred': True,
		'mesh'	: None,
		'aliases': ['aliases.json', 'aliases_kbu.json'],
	}

	db = wrapper(options)
	m = d3mapbuilder.D3MapBuilder(db)
	m.build()
