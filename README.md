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

## Run

```
python sequence_emitter.py sequence.json
```

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