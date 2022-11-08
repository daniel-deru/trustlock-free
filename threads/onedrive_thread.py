import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.message import Message

from workers.onedrive_worker import OneDriveUpload, OneDriveDownload

from windows.loading import Loading


def upload_onedrive(self, show_message=True):
        
    # Create Google upload thread and google upload worker
    self.upload_onedrive_thread = QThread()  
    self.onedrive_upload_worker = OneDriveUpload()

    # Move the worker process to the thread
    self.onedrive_upload_worker.moveToThread(self.upload_onedrive_thread)
    
    # signal to start the worker code when the thread starts
    self.upload_onedrive_thread.started.connect(self.onedrive_upload_worker.upload)
    
    # Close the loading screen after the worker thread is done
    self.onedrive_upload_worker.finished.connect(lambda: self.onedrive_upload_loading.close())
    self.onedrive_upload_worker.finished.connect(self.upload_onedrive_thread.exit)
    self.onedrive_upload_worker.finished.connect(self.upload_onedrive_thread.quit)
    
    
    # Clean up the thread and worker
    self.onedrive_upload_worker.finished.connect(self.onedrive_upload_worker.deleteLater)
    self.upload_onedrive_thread.finished.connect(self.upload_onedrive_thread.deleteLater)
    
    self.upload_onedrive_thread.start()
    
    # Show loading screen while worker is busy
    self.onedrive_upload_loading = Loading("Saving to OneDrive...")
    self.onedrive_upload_loading.exec_()
    
    if show_message:
        message: Message = Message("The backup is complete", "Backup Successful")
        message.exec_()
        

def download_onedrive(self):
        
    # Create a new thread
    self.onedrive_download_thread = QThread()
    
    # Create instance of worker
    self.onedrive_download_worker = OneDriveDownload()
    
    # Move the worker to the new thread
    self.onedrive_download_worker.moveToThread(self.onedrive_download_thread)
    
    # Connect thread started signal to worker to start worker when thread is started
    self.onedrive_download_thread.started.connect(self.onedrive_download_worker.download)
    
    # Connect worker finished signal to slot for processing after worker is done
    self.onedrive_download_worker.finished.connect(self.update_db)
    
    # Clean up the processes for better memory management
    self.onedrive_download_worker.finished.connect(self.onedrive_download_worker.deleteLater)
    self.onedrive_download_worker.finished.connect(self.onedrive_download_thread.exit)
    self.onedrive_download_worker.finished.connect(self.onedrive_download_thread.quit)
    self.onedrive_download_thread.finished.connect(self.onedrive_download_thread.deleteLater)
    
    self.onedrive_download_thread.start()
    
    self.loading = Loading("Syncing from OneDrive...")
    self.loading.exec_()
    
    # message: Message = Message("The restore is complete", "Restore Successful")
    # message.exec_()
        