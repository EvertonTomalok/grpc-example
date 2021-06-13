import threading
from random import randint
from time import sleep

import grpc

from proto import hello_pb2, hello_pb2_grpc


def worker(n: int, name_param: str):
    channel = grpc.insecure_channel('localhost:50051')
    stub = hello_pb2_grpc.GreeterStub(channel)
    name = hello_pb2.HelloRequest(name=name_param)

    sleep(randint(100, 750) / 100)
    response = stub.SayHello(name)

    print(f"[{n}] {response.message}")
    channel.close()


def main():
    for i in range(150):
        t = threading.Thread(target=worker, args=(i, "Everton"))
        t.start()


if __name__ == '__main__':
    main()
