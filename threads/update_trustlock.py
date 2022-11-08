import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtCore import QThread

from workers.update_trustlock import UpdateTrustLockWorker

def update_trustlock(self):
                
    # Create Google upload thread and google upload worker
    self.update_trustlock_thread = QThread()  
    self.update_trustlock_worker = UpdateTrustLockWorker()

    # Move the worker process to the thread
    self.update_trustlock_worker.moveToThread(self.update_trustlock_thread)
    
    # signal to start the worker code when the thread starts
    self.update_trustlock_thread.started.connect(self.update_trustlock_worker.start)
    
    # Close the loading screen after the worker thread is done
    # self.update_password_response method is defined in the main.py file
    self.update_trustlock_worker.progress.connect(self.update_trustlock_progress)
    self.update_trustlock_worker.downloading.connect(lambda: self.update_state("Download in progress..."))
    self.update_trustlock_worker.requested.connect(lambda: self.update_state("Waiting for server..."))
    self.update_trustlock_worker.finished.connect(lambda: self.update_state("Download finished."))
    self.update_trustlock_worker.finished.connect(self.open_zip)
    
    self.update_trustlock_worker.error.connect(self.update_trustlock_thread.exit)
    self.update_trustlock_worker.error.connect(self.update_trustlock_thread.quit)
    self.update_trustlock_worker.error.connect(self.cancel_update)
    self.update_trustlock_worker.error.connect(self.update_trustlock_worker.deleteLater)    
    
    self.update_trustlock_worker.finished.connect(self.update_trustlock_thread.exit)
    self.update_trustlock_worker.finished.connect(self.update_trustlock_thread.quit)    
    
    # Clean up the thread and worker
    self.update_trustlock_worker.finished.connect(self.update_trustlock_worker.deleteLater)
    self.update_trustlock_thread.finished.connect(self.update_trustlock_thread.deleteLater)
    
    self.update_trustlock_thread.start()
