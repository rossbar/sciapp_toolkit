from __future__ import division

from multiprocessing import Process, Queue, Pipe
from Queue import Empty as QueueEmpty

class Thread(Process):
    def __init__(self, inpipe, name, inq=None, outq=None, dispq=None):
        # Base constructor
        super(Process, self).__init__(parent)
  
        # Thread status
        self.name = name
        self.paused = True
        self.abort = False
        # If the thread is only to be used for processing one batch of data 
        # (instead of streaming data), free up the thread after the processing
        # loop has completed its first iteration
        self.is_oneshot = False
        # Communication
        self.input_queue = inq
        self.output_queue = outq
        self.display_queue = dispq
        self.in_pipe = inpipe
        # Placeholders
        self.newdata = False
        self.messageList = []
        self.data_in = []
        self.data_out = []
  
    def run(self):
        # Once 'run' is invoked, a new python process is started. Initialize
        # the process.
        self.initialize()

        # Main run loop
        while not self.abort:
            # Thread starts in a paused state. If the thread is paused it waits
            # here for a message from the control pipe telling it to start,
            # pause, stop, or giving it other info
            if self.paused:
                self.in_pipe.poll(None)  # Blocking wait for message
  
            # Loop over control pipe for as long as there is something in it
            while self.in_pipe.poll():
                # Check for special signals: start, stop, and pause first
                message = self.in_pipe.recv()
                if "STOP" in message:
                    self.abort = True
                elif "PAUSE" in message:
                    self.paused = True
                elif "START" in message:
                    self.paused = False
                    self.start_hardware()
                # If the message wasn't one of the special signals, append it
                # to the message list
                else:
                    self.messageList.append(message)
  
            # NON-FLUSHING BEHAVIOR
            if self.abort: break
  
            # Now try to get data from the queue
            if self.input_queue != None:
                try:
                    # Blocking attempt to get data from queue
                    self.data_in = self.input_queue.get(True, 0.1)  
                    self.newdata = True
                except QueueEmpty: pass
            # If there is no input_queue, the thread must be a generator
            # (like a DAQ thread) so make sure self.newdata is always true so
            # that it can constantly be running its task
            elif not self.paused: self.newdata = True
            else: pass
  
            # After polling the messages and the data queue, if there is
            # something to do (either new data or a new non-control message),
            # do it.
            if self.newdata or len(self.messageList) > 0:
                self.task()
  
            # Back to top of the loop
  
        # Once out of the loop, run the cleanup function and notify the GUI the
        # thread is done
        self.cleanup()
  
    def task(self):
        '''
        Needs to be overridden by child object. Default behavior is to
        print messages and input data.
        '''
        if len(self.messageList) > 0:
            for i,message in enumerate(self.messageList): 
                print "\tMessage %s: %s" %(i, message)
            # Reset message list after using the messages
            self.messageList = []
        if self.newdata:
            # After using new data, set newdata flag back to false
            self.newdata = False
  
    def cleanup(self):
        '''
        Function to run after the run loop has exited. Must be overridden by
        child class
        '''
        pass
  
    def initialize(self):
        '''
        Function to run before the main run loop in self.run starts. This is
        for threads that deal with opening and closing files, since that gets
        screwed up when its not all contained within the run loop.
        '''
        self.in_pipe.send((self.name, self.pid, "READY"))
  
    def start_hardware(self):
        '''
        Function to start any hardware controlled by the thread. Must be
        overwritten.
        '''
        pass
