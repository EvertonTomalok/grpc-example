import logging
import os

import grpc
from concurrent import futures

from proto import hello_pb2, hello_pb2_grpc


logging.basicConfig(
    format="[%(levelname)s][%(asctime)s] %(filename)s - %(message)s",
    level=os.environ.get("LOGLEVEL", "INFO"),
)
logger = logging.getLogger("MAIN")


class GreetingServicer(hello_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        response = hello_pb2.HelloReply()
        response.message = f"Hello {request.name}"
        return response


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(GreetingServicer(), server)

    logger.info('Starting server. Listening on port 50051.')
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
