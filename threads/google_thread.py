import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.message import Message

from workers.google_drive_worker import GoogleUpload, GoogleDownload

from windows.loading import Loading

# Method to create Thread for uploading to Google Drive
def upload_google(self, show_message=True):
    
    # Create Google upload thread and google upload worker
    self.upload_google_thread = QThread()  
    self.google_upload_worker = GoogleUpload()
    
    # Move the worker process to the thread
    self.google_upload_worker.moveToThread(self.upload_google_thread)
    
    # signal to start the worker code when the thread starts
    self.upload_google_thread.started.connect(self.google_upload_worker.upload)
    
    # Close the loading screen after the worker thread is done
    self.google_upload_worker.finished.connect(lambda: self.google_upload_loading.close())
    self.google_upload_worker.finished.connect(self.upload_google_thread.exit)
    self.google_upload_worker.finished.connect(self.upload_google_thread.quit)
    
    # Clean up the thread and worker
    self.google_upload_worker.finished.connect(self.google_upload_worker.deleteLater)
    self.upload_google_thread.finished.connect(self.upload_google_thread.deleteLater)
    
    self.upload_google_thread.start()
    
    # Show loading screen while worker is busy
    self.google_upload_loading = Loading("Saving to Google Drive...")
    self.google_upload_loading.exec_()
    
    if show_message:
        message: Message = Message("The backup is complete", "Backup Successful")
        message.exec_()
        
def download_google(self):
        
    # Create a new thread
    self.google_download_thread = QThread()
    
    # Create instance of worker
    self.google_download_worker = GoogleDownload()
    
    # Move the worker to the new thread
    self.google_download_worker.moveToThread(self.google_download_thread)
    
    # Connect thread started signal to worker to start worker when thread is started
    self.google_download_thread.started.connect(self.google_download_worker.download)
    
    # Connect worker finished signal to slot for processing after worker is done
    self.google_download_worker.finished.connect(self.update_db)
    
    # Clean up the processes for better memory management
    self.google_download_worker.finished.connect(self.google_download_worker.deleteLater)
    self.google_download_worker.finished.connect(self.google_download_thread.exit)
    self.google_download_worker.finished.connect(self.google_download_thread.quit)
    self.google_download_thread.finished.connect(self.google_download_thread.deleteLater)
    
    self.google_download_thread.start()
    
    self.loading = Loading("Syncing from Google Drive...")
    self.loading.exec_()
    
    # Message("The restore is complete", "Restore Successful").exec_()
    