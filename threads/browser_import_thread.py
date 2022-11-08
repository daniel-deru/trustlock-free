import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.message import Message
from workers.browser_import_worker import BrowserImport


def browser_import(self, data):
    # Create Google upload thread and google upload worker
    self.browser_import_thread = QThread()  
    self.browser_import_worker = BrowserImport(data)
    
    # Move the worker process to the thread
    self.browser_import_worker.moveToThread(self.browser_import_thread)
    
    # signal to start the worker code when the thread starts
    self.browser_import_thread.started.connect(self.browser_import_worker.save)
    
    # Close the loading screen after the worker thread is done
    self.browser_import_worker.finished.connect(lambda: worker_finished(self))
    # self.browser_import_worker.finished.connect(self.browser_import_thread.quit)
    
    # Clean up the thread and worker
    # self.browser_import_worker.finished.connect(self.browser_import_worker.deleteLater)
    self.browser_import_thread.finished.connect(self.browser_import_thread.deleteLater)
    
    self.browser_import_thread.start()
    

    
def worker_finished(self):
    self.browser_import_thread.exit()
    self.browser_import_thread.quit()
    self.browser_import_worker.deleteLater()
    self.updateWindow()
    
    message: Message = Message("The import was successfull", "Import Successful")
    message.exec_()