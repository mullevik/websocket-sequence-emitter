
import argparse
import logging

import json
import time
from typing import List, NamedTuple, Any

import gevent
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from collections import OrderedDict

log = logging.getLogger(__name__)


class SequenceEmitterApp(WebSocketApplication):

    def on_open(self):
        log.debug("New client joined")

    def on_message(self, message, **kwargs):
        log.debug("A message was received by client")

    def on_close(self, reason):
        log.debug("Client has disconnected")


class SequenceItem(NamedTuple):
    second: float
    data: Any


def load_sequence_from_file(path_to_file: str) -> List[SequenceItem]:
    # todo: support more file formats
    with open(args.file, "r") as file:
        sequence = json.load(file)

    return [SequenceItem(item["at_second"], item["data"]) for item in sequence]


def play_sequence(server: WebSocketServer,
                  sequence: List[SequenceItem],
                  args: argparse.Namespace):
    start_time = time.time()

    for head in range(len(sequence)):

        current = sequence[head]

        should_start_at = start_time + (current.second / args.speed)
        current_time = time.time()

        if current_time < should_start_at:
            # sleep if there is a delay
            delay = should_start_at - current_time
            log.debug(f"Sleep for {delay} seconds")
            gevent.sleep(delay)

        # send data
        log.info(f"Sequence data number {head}")
        for client in server.clients.values():
            # convert data to string
            data = json.dumps(current.data)
            log.debug(f"Sending message: {data}")
            client.ws.send(data)


def process_sequence(server: WebSocketServer, args: argparse.Namespace):

    log.info(f"Opening sequence file {args.file}")

    sequence = load_sequence_from_file(args.file)

    if args.start_delay > 0.:
        log.info(f"Sleeping on start delay ({args.start_delay}s)")
        gevent.sleep(args.start_delay)

    while True:
        play_sequence(server, sequence, args)
        if not args.loop:
            break

    log.info("Sequence has ended")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SequenceEmitter')

    parser.add_argument('file', action="store", type=str)
    parser.add_argument('-l', '--loop', action="store_true", default=False)
    parser.add_argument('-p', '--port', action="store", dest="port",
                        type=int, default="8080")
    parser.add_argument('-s', '--speed', action="store", dest="speed",
                        type=float, default=1.)
    parser.add_argument('-d', '--start-delay', action="store",
                        dest="start_delay", type=float, default=0.)
    args = parser.parse_args()

    logging.basicConfig(format='[%(asctime)s] %(levelname).1s - %(message)s',
                        level=logging.DEBUG)

    server = WebSocketServer(
        ('0.0.0.0', args.port),
        Resource(OrderedDict([('/', SequenceEmitterApp)]))
    )

    log.info(f"Starting emitter server on port {args.port}")
    server_task = gevent.spawn(server.start)
    sequence_task = gevent.spawn(process_sequence, server=server, args=args)

    gevent.joinall([server_task, sequence_task])
    log.info("Tasks joined successfully (ending gracefully)")
