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

Build from local ```Dockerfile```:
```
docker build . -t sequence_emitter
```

## Specify the sequence

The sequence file can have following types:

### JSON
```json
[
    {"at_second": 0.0, "data": {"first": "object"}},
    {"at_second": 2.2, "data": 2},
    {"at_second": 3, "data": "three"},
    {"at_second": 4, "data": ["f", "o", "u", "r"]}
]
```
This ```sequence.json``` file would initiate a sequence that starts immediately at second ```0.0```.
It has 4 samples. The ```at_second``` defines at which second from the sequence start
should this sample be sent to all clients. Anything inside the ```data``` is sent
over the WebSocket after Python's ```json.dumps``` function is applied to it.

## Run the server

```
python sequence_emitter.py sequence.json
```

After this command, the server cycles through the sequence.
Anytime a new WebSocket client is connected, it immediately subscribes for all
new sequence messages produced by the server.
WebSocket clients can connect or disconnect at any time. The server does not care.

#### Additional attributes
- ```-p [int]```, ```--port [int]``` - specify your favorite port (default is 8080)
- ```-l```, ```--loop``` - loop the sequence over and over (stop by KeyboardInterrupt)
- ```-s [float]```, ```--speed [float]``` - playback speed (default is 1.0)
- ```-d [float]```, ```--start-delay [float]``` - set delay in seconds before the first sample of the sequence is emitted (default is 0.0)


### Run with docker

Run local container with ```sequence.json``` passed as a volume and redirected port:
```
docker run --rm -v $(pwd)/sequence.json:/app/sequence_file -p 40001:8080 -it sequence_emitter
```

Note that the app inside the  container always loads file ```/app/sequence_file``` and listens on port ```8080```.

Additional arguments can be passed to the container like so:
```
docker run --rm -v $(pwd)/sequence.json:/app/sequence_file -p 40001:8080 -it sequence_emitter -l -s 2.5
```