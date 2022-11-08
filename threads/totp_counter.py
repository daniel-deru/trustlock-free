import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from workers.totp_counter import TOTPCounter


def totp_counter(self, code):
    # Create Google upload thread and google upload worker
    self.counter_thread = QThread()  
    self.counter_worker = TOTPCounter(code)
    
    # Move the worker process to the thread
    self.counter_worker.moveToThread(self.counter_thread)
    
    # signal to start the worker code when the thread starts
    self.counter_thread.started.connect(self.counter_worker.count)
    
    # Close the loading screen after the worker thread is done
    self.counter_worker.time_signal.connect(lambda time: display_time(self, time))
    # self.browser_import_worker.finished.connect(self.browser_import_thread.quit)
    
    # Clean up the thread and worker
    # self.browser_import_worker.finished.connect(self.browser_import_worker.deleteLater)
    self.counter_thread.finished.connect(self.counter_thread.deleteLater)
    
    self.counter_thread.start()
    

    
def display_time(self, time):
    self.lbl_counter.setText(f"{time}")