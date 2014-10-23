import os
import subprocess
from node import Node
from RRD import RRD, DS, RRA

class NodeRRD(RRD):
    ds_list = [
        DS('upstate', 'GAUGE', 120, 0, 1),
        DS('clients', 'GAUGE', 120, 0, float('NaN')),
    ]
    rra_list = [
        RRA('AVERAGE', 0.5, 1, 120),    #  2 hours of  1 minute samples
        RRA('AVERAGE', 0.5, 5, 1440),   #  5 days  of  5 minute samples
        RRA('AVERAGE', 0.5, 60, 720),   # 30 days  of  1 hour   samples
        RRA('AVERAGE', 0.5, 720, 730),  #  1 year  of 12 hour   samples
    ]

    def __init__(self, filename, node = None):
        """
        Create a new RRD for a given node.

        If the RRD isn't supposed to be updated, the node can be omitted.
        """
        self.node = node
        super().__init__(filename)
        self.ensureSanity(self.ds_list, self.rra_list, step=60)

    @property
    def imagename(self):
        return os.path.basename(self.filename).rsplit('.', 2)[0] + ".png"

    def update(self):
        super().update({'upstate': 1, 'clients': self.node.clientcount})

    def graph(self, directory, timeframe):
        """
        Create a graph in the given directory. The file will be named
        basename.png if the RRD file is named basename.rrd
        """
        args = ['rrdtool','graph', os.path.join(directory, self.imagename),
                '-s', '-' + timeframe ,
                '--title', 'Clients 7d',
                '--watermark', '"`date`"',
                '-w', '800',
                '-h', '400',
                '-l', '0',
                '-Y',
#                '-y', '1:1',
                '-z',  # only generate the graph if the current graph is out of date
                'DEF:clients=' + self.filename + ':clients:AVERAGE',
                'VDEF:maxc=clients,MAXIMUM',
                'CDEF:c=0,clients,ADDNAN',
#                'CDEF:d=clients,UN,maxc,UN,1,maxc,IF,*',
                'CDEF:d=clients,UN,INF,UN,1,INF,IF,*',
#                'AREA:c#0F0:up\\l',
                'AREA:c#00cb35:connected clients',
                'AREA:d#dd0068:node offline\\l',
                'GPRINT:clients:MAX:Max\: %5.1lf',
                'GPRINT:clients:AVERAGE:Avg\: %5.1lf',
                'GPRINT:clients:LAST:Cur\: %5.1lf',
                'LINE1:c#550372:',
#                'LINE1:c#00F:clients connected\\l',
                ]
        subprocess.check_output(args)
