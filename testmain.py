import multiprocessing
import time

class MyProcess(multiprocessing.Process):

    def __init__(self, ):
        multiprocessing.Process.__init__(self)
        self.exit = multiprocessing.Event()
        self.n =0
    def run(self):
        while not self.exit.is_set():
            time.sleep(1)
            print(self.n)
            self.n += 1
        print ("You exited!")

    def shutdown(self):
        print("Shutdown initiated")
        self.exit.set()


if __name__ == "__main__":
    process = MyProcess()
    process.start()
    print("Waiting for a while")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
    process.shutdown()
    time.sleep(3)
    print("Child process state: %d" % process.is_alive())