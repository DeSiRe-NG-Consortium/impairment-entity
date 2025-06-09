from flask import Flask, json, request
import subprocess


api = Flask(__name__)

state = "STOPPED"
currentDatarate = 0
currentLatency = 0


# Get current state
@api.route('/state', methods=['get'])
def get_state():
  global state
  resultJSON= [{"state": state}]
  return json.dumps(resultJSON)

# Get current impairment parameters
@api.route('/params', methods=['get', 'post'])
def params():
  global currentDatarate
  global currentLatency
  if request.method == 'GET':
    resultJSON= [{"datarate": currentDatarate}, {"latency": currentLatency}]
    return json.dumps(resultJSON)
  elif request.method == 'POST':
    content=json.loads(request.json)
    currentDatarate = content['datarate']
    currentLatency = content['latency']
    print("Set datarate to " + str(currentDatarate) + "Mbps and " + str(currentLatency) + "ms.")
    if state == "RUNNING":
      cmdChangeImpairment = [ 'sudo', 'tc', 'qdisc', 'change', 'dev', 'eth2', 'root', 'netem',  'rate', str(currentDatarate) + "mbit", 'delay', str(currentLatency) + "ms"]
      changeImpairmentState = subprocess.Popen( cmdChangeImpairment, stdout=subprocess.PIPE ).communicate()[0].decode('utf-8', 'ignore')
      print("Changed netem")
    return json.dumps({"success": True}), 201

# Start Impairment
@api.route('/start', methods=['post'])
def start_impairment():
  global state
  cmdStartImpairment = [ 'sudo', 'tc', 'qdisc', 'add', 'dev', 'eth2', 'root', 'netem',  'rate', str(currentDatarate) + "mbit", 'delay', str(currentLatency) + "ms"  ]
  startImpairmentState = subprocess.Popen( cmdStartImpairment, stdout=subprocess.PIPE ).communicate()[0].decode('utf-8', 'ignore')
  state = "RUNNING"
  return json.dumps({"success": True}), 201

# Stop Impairment
@api.route('/stop', methods=['post'])
def stop_impairment():
  global state
  cmdStopImpairment = [ 'sudo', 'tc', 'qdisc', 'del', 'dev', 'eth2', 'root', 'netem']
  stopImpairmentState = subprocess.Popen( cmdStopImpairment, stdout=subprocess.PIPE ).communicate()[0].decode('utf-8', 'ignore')
  state = "STOPPED"
  return json.dumps({"success": True}), 201


if __name__ == '__main__':
    api.run(host="0.0.0.0", port="5010")
