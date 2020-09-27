
from multiprocessing import Process, Pipe
from os import getpid
import time


def process_a(pipe_b, pipe_c):
    vector = [0,0,0]
    pipe_dim = 0
    vector = send_vector(pipe_b, pipe_dim, vector)
    vector = send_vector(pipe_b, pipe_dim, vector)
    vector = internal_action(vector, pipe_dim)
    vector = recv_vector(pipe_b, vector, pipe_dim)
    vector = internal_action(vector, pipe_dim)
    vector = internal_action(vector, pipe_dim)
    vector = recv_vector(pipe_b, vector, pipe_dim)

    print(vector)

def process_b(pipe_a, pipe_c):
    vector = [0,0,0]
    pipe_dim = 1
    vector = recv_vector(pipe_a, vector, pipe_dim)
    vector = recv_vector(pipe_a, vector, pipe_dim)
    vector = send_vector(pipe_a, pipe_dim, vector)
    vector = recv_vector(pipe_c, vector, pipe_dim)
    vector = internal_action(vector, pipe_dim)
    vector = send_vector(pipe_a, pipe_dim, vector)
    vector = send_vector(pipe_c, pipe_dim, vector)
    vector = send_vector(pipe_c, pipe_dim, vector)
    time.sleep(1)
    print(vector)

def process_c(pipe_a, pipe_b):
    vector = [0,0,0]
    pipe_dim = 2
    vector = send_vector(pipe_b, pipe_dim, vector)
    vector = recv_vector(pipe_b, vector, pipe_dim)
    vector = internal_action(vector, pipe_dim)
    vector = recv_vector(pipe_b, vector, pipe_dim)
    time.sleep(2)
    print(vector)

def send_vector(pipe, process_dimension, vector):
    vector[process_dimension] += 1
    pipe.send(vector)
    return vector

def recv_vector(pipe, vector, process_dimension):
    incomin_vector = pipe.recv()

    for i in range (3):
        if vector[i]>incomin_vector[i]:
            incomin_vector[i] = vector[i]
    incomin_vector[process_dimension] += 1
    return incomin_vector

def internal_action(vector, process_dimension):
    vector[process_dimension] += 1
    return vector


if __name__ == '__main__':
    a_b, b_a = Pipe()
    a_c, c_a = Pipe()
    b_c, c_b = Pipe()

    process1 = Process(target=process_a,
                       args=(a_b, a_c))
    process2 = Process(target=process_b,
                       args=(b_a, b_c))
    process3 = Process(target=process_c,
                       args=(c_a, c_b))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

