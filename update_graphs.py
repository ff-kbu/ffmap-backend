#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

from rrddb import rrd

rrd_src_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "nodedb/")
dest_dir = os.path.join('/var/www/ffmap-d3', 'nodes/')
print(rrd_src_dir, dest_dir)

rrd = rrd(rrd_src_dir, dest_dir, displayTimeGlobal="28d", displayTimeNode="7d")

rrd.update_images()

