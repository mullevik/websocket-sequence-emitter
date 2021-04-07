import csv

import argparse
import logging

import json

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


def process_sequence(server: WebSocketServer, args: argparse.Namespace):

    log.info(f"Opening sequence file {args.file}")
    with open(args.file, "r") as file:
        sequence = json.load(file)

    head = 0
    last_seconds = 0

    while True:

        if head >= len(sequence):
            # handle sequence ending
            if args.loop:
                # start the sequence again
                last_seconds = 0
                head = 0
                log.info("Starting over (looping is active)")
            else:
                # end sequence loop
                log.info("Ending sequence (looping is disabled)")
                break

        current = sequence[head]
        current_seconds = current["time"]
        delay = current_seconds - last_seconds
        last_seconds = current_seconds

        # sleep
        gevent.sleep(delay)

        # send data
        log.info(f"Sending sequence data number {head}")
        for client in server.clients.values():
            client.ws.send(current["data"])

        # move head
        head += 1

    log.info("Sequence has ended")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SequenceEmitter')

    parser.add_argument('file', action="store", type=str)
    parser.add_argument('-l', '--loop', action="store_true", default=False)
    parser.add_argument('-p', '--port', action="store", dest="port", type=int,
                        default="40001")
    args = parser.parse_args()

    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
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
