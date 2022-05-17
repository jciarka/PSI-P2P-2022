def synchronized(f):
    def wrapped_function(*args):
        self = args[0]
        self.lock.acquire()
        f(*args)
        self.lock.release()
    return wrapped_function
