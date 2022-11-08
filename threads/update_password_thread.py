import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from workers.update_password import UpdatePasswordWorker

def update_password(self):
            
    # Create Google upload thread and google upload worker
    self.update_password_thread = QThread()  
    self.update_password_worker = UpdatePasswordWorker()

    # Move the worker process to the thread
    self.update_password_worker.moveToThread(self.update_password_thread)
    
    # signal to start the worker code when the thread starts
    self.update_password_thread.started.connect(self.update_password_worker.ask)
    
    # Close the loading screen after the worker thread is done
    # self.update_password_response method is defined in the main.py file
    self.update_password_worker.finished.connect(self.update_password_response)
    self.update_password_worker.finished.connect(self.update_password_thread.exit)
    self.update_password_worker.finished.connect(self.update_password_thread.quit)
    
    
    # Clean up the thread and worker
    self.update_password_worker.finished.connect(self.update_password_worker.deleteLater)
    self.update_password_thread.finished.connect(self.update_password_thread.deleteLater)
    
    self.update_password_thread.start()