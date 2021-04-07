# WebSocket sequence emitter

A simple WebSocket sequence emitter for development purposes.

Open a sequence file and emit its data to all WebSocket clients.

Great for testing real-time WebSocket applications.


## Install


### Python

#### Requirements
- Python >= 3.7

#### Steps
```
git clone git@github.com:mullevik/websocket-sequence-emitter.git
cd websocket-sequence-emitter

python -m venv env
source env/bin/activate
pip install requirements
```

### Docker

TODO



## Run

```
python sequence_emitter.py sequence.json
```

#### Additional attributes
- ```-p [int]```, ```--port [int]``` - specify your favorite port (default is 46001)
- ```-l```, ```--loop``` - loop the sequence over and over (stop by KeyboardInterrupt)
- ```-s [float]```, ```--speed [float]``` - playback speed (default is 1.0) (NotImplementedYet)
- ```-d [float]```, ```--start-delay [float]``` - set delay in seconds before the first sample of the sequence is emitted (NotImplementedYet)


### Run with docker

TODO