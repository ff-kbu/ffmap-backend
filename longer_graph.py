#!/usr/bin/env python3

import os

from GlobalRRD import GlobalRRD

dbPath = '/srv/ffmap-backend/nodedb/'
imgPath = '/var/www/ffmap-d3/nodes/year.png'

globalDB = GlobalRRD(dbPath)
globalDB.nodesGraph(imgPath, "1y")
