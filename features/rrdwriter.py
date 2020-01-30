"""
 * RRD writer plugin
 * for sma-em daemon
 *
"""
import subprocess
import os

def config(config):
    """
    Configure the stuff
    """
    print("Loaded rrdwriter")
    if not os.path.isfile(config['file']):
       print("Create RRD database " + config['file'])
       cmd = ['rrdcreate', config['file'], '--start','now', '--step', '1']
       channels = config['values'].split(" ")
       for channel in channels:
           cmd.append('DS:%s:GAUGE:10:0:U' % channel)
       cmd.extend(['RRA:MAX:0.5:1:864000'])
       #cmd.extend(['RRA:MAX:0.5:1:864000', 'RRA:AVERAGE:0.5:60:129600', 'RRA:AVERAGE:0.5:3600:13392', 'RRA:AVERAGE:0.5:86400:3660'])
       print('Exec: ' + str(cmd))
       subprocess.run(cmd)

def run(emparts,config):
    """
    * sma-em daemon calls run for each measurement package
    * emparts: all measurements of one sma-em package
    * config: all config items from section FEATURE-[featurename] in /etc/smaemd/config
    *
    """
    values = "N"
    for key in config['values'].split(','):
       values += ":"+str(emparts[key])
    cmd= ['rrdupdate', config['file'], values]
    subprocess.run(cmd)

