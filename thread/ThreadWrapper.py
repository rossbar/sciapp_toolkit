from __future__ import division
import os

from multiprocessing import Process, Queue, Pipe
from Queue import Empty as QueueEmpty

class Thread(Process):
    """
    Processing 'thread' with I/O and runloop based on multiprocessing.Process
    """
    _data_timeout = 0.1     # 100 ms
    def __init__(self, inpipe, name, inq=None, outq=None, dispq=None):
        """
        Multiprocessing-based run loop.
        """
        super(Thread, self).__init__()
        # Status
        self._name = name
        self._paused = True
        self._abort = False
        self._verbose = False
        self._is_oneshot = False
        self._newdata = False
        self._parent_pid = os.getpid()
        # Communication
        self.input_queue = inq
        self.output_queue = outq
        self.display_queue = dispq
        self.in_pipe = inpipe
        # Containers for data/messages
        self.message_list = []
        self.data_in = None
        self.data_out = None

    def poll_control_pipe(self):
        """
        Extract and parse messages on control pipe. 

        If standard control message received, take appropriate action.
        """
        while self.in_pipe.poll():
            msg = self.in_pipe.recv()
            # Handle standard control messages here
            if   "STOP"  in msg: self._abort = True
            elif "PAUSE" in msg: self._paused = True
            elif "START" in msg: self._paused = False
            # Non-standard message - append to list for subsequent action
            else: self.message_list.append(msg)

    def poll_data_queue(self):
        """
        Extract and notify of new data in input queue.
        """
        # I/O Process: relies on input queue for data
        if self.input_queue is not None:
            try:
                self.data_in = self.input_queue.get(True, self._data_timeout)
                self._newdata = True
            except QueueEmpty: self._newdata = False
        # Output-only thread (e.g. data acquisition)
        else:
            if not self._paused: self._newdata = True

    def process_messages(self):
        """
        Handle messages if necessary.

        Must be implemented in base class.
        """
        raise NotImplementedError

    def process_data(self):
        """
        Process data if necessary.

        Must be implemented in base class.
        """
        raise NotImplementedError

    def cleanup(self):
        """
        Clean up function run once thread run loop is terminated.
        """
        pass

    def initialize(self):
        """
        Function run before entering main run loop.

        NOTE: It is necessary to implement some things here (such as opening/
        closing files). This is a quirk of multiprocessing, which fails to
        pass non-picklable things from the constructor to the newly-created
        process.
        """
        self._pid = os.getpid()

    def run(self):
        """
        Override Process run method with an interruptible run-loop.
        """
        # Process initialization
        self.initialize()
        if self._verbose: print "%s initialized" %(self._name)
        # Main run loop
        while not self._abort:
            # Thread starts in paused state. If thread is paused, wait here for
            # message from control pipe (start, pause, stop, etc.)
            if self._paused:
                self.in_pipe.poll(None)     # Blocking
            # Handle all control messages
            self.poll_control_pipe()
            # NON-FLUSHING BEHAVIOR
            if self._abort: break
            # Process non-control messages
            if len(self.message_list) > 0:
                self.process_messages()
            # Handle incoming data
            self.poll_data_queue()
            if self._newdata:
                self.process_data()
        # Once out of run loop, clean up
        self.cleanup()

