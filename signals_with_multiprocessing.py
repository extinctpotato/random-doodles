import multiprocessing, time, sys, signal, os, inspect

# Sending SIGTERM will terminate the main process
# but the process running the 'a' function will remain dangling.

def signal_handler(sig, fr):
    print(inspect.stack()[0][3])
    print('{}: Received {}'.format(os.getpid(), sig))
    sys.exit(3)
    # the statement below never executes, leaving the process dangling.
    # p.terminate()

signal.signal(signal.SIGTERM, signal_handler)

def a(b):
    def signal_handler(sig, fr):
        print(inspect.stack()[0][3])
        print('{}: 2Received {}'.format(os.getpid(), sig))
        sys.exit(5)

    # The process normally inherits parent signal handler
    # but we overwrite it here.
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        print('{}: {}'.format(os.getpid(), b))
        time.sleep(1)

p = multiprocessing.Process(target=a, args=('cool test',))
p.start()

print('PID: {}'.format(os.getpid()))

sys.exit(4)
