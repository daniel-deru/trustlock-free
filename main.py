from datetime import date, datetime
import sys
import time
import json

from PyQt5.QtWidgets import QApplication, QWidget, QSplashScreen, QTabWidget, QMessageBox
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor, QCloseEvent, QFontDatabase
from PyQt5.QtCore import QTimer, Qt, pyqtSlot

from designs.python.main_widget import Ui_main_container

from database.model import Model

from tabs.apps_tab import Apps_tab
from tabs.notes_tab import Notes_tab
from tabs.todos_tab import Todo_tab
from tabs.settings_tab import SettingsTab
from tabs.vault_tab import Vault_tab

from widgetStyles.TabWidget import TabWidget
from widgetStyles.Widget import Widget, MainWidget

from widgets.tabbar import TabBar, ProxyStyle

from utils.helpers import StyleSheet
from utils.enums import RegisterStatus
from utils.message import Message
from utils.globals import VERSION

from windows.register_window import Register
from windows.login_window import Login
from windows.setup_window import InitialSetup
from windows.update_password import UpdatePassword

from threads.update_password_thread import update_password

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class Main(Ui_main_container, QWidget):
    def __init__(self):
        super(Main, self).__init__()
        
        self.expired_passwords: list = []
        self.twofa_passed = True
        
        QFontDatabase.addApplicationFont(":/fonts/RobotoCondensed")
        
        self.timer = QTimer(self)
        self.logged_in = False
        self.count = 0
        self.duration = int(Model().read("settings")[0][5]) * 60
        
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowTitle("TrustLock")
        self.read_style()
        self.tab_widget.setDocumentMode(True)
        self.custom_tabbar = TabBar(self.tab_widget)
        self.tab_widget.setTabBar(self.custom_tabbar)
        self.set_screen_size()

        self.add_tabs()
        self.tab_widget.setCurrentIndex(4)
        self.previous_index = 4
        self.setTabIcons()
        self.update_status(False)

        self.tab_widget.currentChanged.connect(self.changed)    
        
        self.user = Model().read("user")

        if len(self.user) != 1:
            self.register = Register()
            self.register.register_close_signal.connect(self.register_event)
            self.register.exec_()
        else:
            # self.check_updates()
            self.get_user_password_expiration()
            self.get_vault_password_expiration()
            
            # Check if there are any expired passwords
            if len(self.expired_passwords) > 0:
                update_password(self)
                
    # def check_updates(self):
    #     current_time = int(time.time())
    #     SECONDS_IN_DAY = 24 * 60 * 60
    #     last_checked = Model().read("user")[0][7]
        
    #     if not last_checked:
    #         return Model().update("user", {"last_update_request": current_time}, "user")
        
        # if(current_time < int(last_checked) + SECONDS_IN_DAY):
        #     return
        
        # data = None
        
        # try:
        #     data = requests.get("https://api.smartmetatec.com/index.php/update/version")
        # except:
        #     return Model().update("user", {"last_update_request": current_time}, "user")
            
        # response = json.loads(json.loads(data.json()['data']))

        # if response['version'] == VERSION:
        #     Model().update("user", {"last_update_request": current_time}, "user")
        # else:
        #     do_update = Message("There is a new update. Do you want to update TrustLock", "Update Available").prompt()
            
        #     if do_update == QMessageBox.Yes:
        #         download_window = DownloadWindow()
        #         download_window.close_app.connect(sys.exit)
        #         download_window.exec_()
        #     else:
        #         Model().update("user", {"last_update_request": current_time}, "user")
                

        
    def get_vault_password_expiration(self):
        # Get all the vault entries
        all_vault_entries = Model().read("vault")
        
        # Get only the app and crypto entries
        app_crypto_entries = list(filter(lambda entry: entry[1] != 'general', all_vault_entries))
        
        for entry in app_crypto_entries:
            vault_data = json.loads(entry[3])
            exp_date_string = vault_data['password_exp']
            
            # Get the datetime object from the date string
            exp_datetime = datetime.strptime(exp_date_string, "%Y-%m-%d")
            
            # Get the date object from the datetime object
            exp_date = date(exp_datetime.year, exp_datetime.month, exp_datetime.day)
            
            # Get the current date
            current_date = date.today()
            
            # Put the expired passwords in the expired passwords list
            if exp_date <= current_date:
                self.expired_passwords.append(["vault", entry])
           
    
    def get_user_password_expiration(self):
        password_exp_string: str = self.user[0][6]
        
        # Get the datetime object from the string
        exp_date = datetime.strptime(password_exp_string, "%Y-%m-%d")
        
        # Convert to date objext
        password_exp_date = date(exp_date.year, exp_date.month, exp_date.day)
        
        # Get the current date
        current_date = date.today()
        
        if password_exp_date <= current_date:
            self.expired_passwords.append(["user", self.user[0]])
    
    # Get the response from asking if the user wants to update passwords 
    @pyqtSlot(bool)  
    def update_password_response(self, response):
        if response == True:
            update_password_window = UpdatePassword(self.expired_passwords)
            update_password_window.finished.connect(self.updateWindow)
            update_password_window.exec_()

    def register_event(self, event):
        if event == RegisterStatus.window_closed:
            return sys.exit()
        
        self.register.close()
        setup_wizard = InitialSetup()
        setup_wizard.setup_finished.connect(self.updateWindow)
        setup_wizard.exec_()
     
       
    def read_style(self):
        styles = [
            Widget,
            MainWidget, 
            TabWidget,
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]

        self.tab_widget.setFont(QFont(font))
        self.setTabIcons()

    def updateWindow(self):
        self.apps_tab.app_signal.emit("update")
        self.notes_tab.note_signal.emit("update")
        self.todo_tab.todo_signal.emit("update")
        self.vault_tab.vault_signal.emit("update") # problem lies here
        self.settings_tab.settings_update_signal.emit("update")
        self.custom_tabbar.update_bar.emit(True)
        self.read_style()
    
    # This is to update the vault window after a new app has been added
    def updateVault(self):
        pass
    
    def updateTable(self):
        self.vault_tab.vault_signal.emit("update")

    def add_tabs(self):        
        self.tab_widget.setTabPosition(QTabWidget.West)
        
        self.vault_tab = Vault_tab().create_tab()
        self.vault_tab.login_signal.connect(self.check_login)
        self.vault_tab.logout_signal.connect(self.lock)
        self.tab_widget.addTab(self.vault_tab, "Vault")
        
        self.apps_tab = Apps_tab().create_tab()
        self.apps_tab.table_signal.connect(self.updateTable)
        self.tab_widget.addTab(self.apps_tab, "Apps")

        self.notes_tab = Notes_tab().create_tab()
        self.tab_widget.addTab(self.notes_tab, "Notes")

        self.todo_tab = Todo_tab().create_tab()
        self.tab_widget.addTab(self.todo_tab, "To-dos")

        self.settings_tab = SettingsTab().create_tab()
        self.settings_tab.settings_signal.connect(self.updateWindow)
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        self.tab_widget.tabBar().setCursor(QCursor(Qt.PointingHandCursor))

        self.main_layout.addWidget(self.tab_widget)
        
    @pyqtSlot()
    def lock(self):
        self.tab_widget.blockSignals(True)
        self.tab_widget.setCurrentIndex(1)
        self.update_status(False)
        self.previous_index = self.tab_widget.currentIndex()
        self.tab_widget.blockSignals(False)
        
    def set_screen_size(self):
        # Get the primary screen
        app = QApplication.primaryScreen()
        # Get the size of the screen
        screen = app.size()
        
        # Get the screen dimensions
        screen_width: int = screen.width()
        screen_height: int = screen.height()
        # Scale factor to determine minimum size
        scale_factor = 0.7
        
        # If the screen is not full hd increase the scale factor
        if(screen_width < 1920 and screen_height < 1080):
            scale_factor = 0.8
            
        # Set the minimum size
        self.setMinimumSize(int(screen_width * scale_factor), int(screen_height * scale_factor))

    def setTabIcons(self):

        # Get the night mode setting from the database
        nightModeOn = int(Model().read("settings")[0][1])
        icons = [
                "_vault.svg",
                "_apps.svg",
                "_notes.svg",
                "_task.svg",
                "_settings.svg"
        ]
        for i in range(len(icons)):
            # Set the icon color for the tabbar
            icon_color = "black"
            active_icon_color = "white" if nightModeOn else "black"
            self.tab_widget.setTabIcon(i, QIcon(f":/tabicons/{icon_color}{icons[i]}"))

        active_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.setTabIcon(active_tab_index, QIcon(f":/tabicons/{active_icon_color}{icons[active_tab_index]}"))
    
    def changed(self):
        self.setTabIcons()
        current_index = self.tab_widget.currentIndex()
        if(current_index == 0 and not self.logged_in):
            self.tab_widget.setCurrentIndex(self.previous_index)
            login_window = Login()
            login_window.login_status.connect(self.access_vault)
            login_window.exec_()
        elif(self.previous_index == 0 and self.logged_in):
            
            lock_vault = Message("Do you want to lock the vault?", "Lock The Vault").prompt()
            if lock_vault == QMessageBox.Yes:
                self.update_status(False)
            self.previous_index = current_index
        else:
            self.previous_index = current_index
            
        if self.previous_index == 4:
            self.settings_tab.logout_signal.emit(True)
    
    @pyqtSlot(str)
    def access_vault(self, signal):
        if signal == "success":
            self.update_status(True)
            current_index = self.tab_widget.currentIndex()
            self.previous_index = current_index
            self.tab_widget.setCurrentIndex(0)

    def check_login(self, signal):
        # The user wants to log in

        if signal == "login requested" and self.logged_in == False:
            login_window = Login()
            login_window.login_status.connect(self.login)
            login_window.exec_()
        # The user wants to log out
        elif signal == "logout requested" and self.logged_in == True:
            if self.tab_widget.currentIndex() == 0:
                self.tab_widget.setCurrentIndex(1)
            self.update_status(False)

    # slot for the login window signal to verify if the user successfully logged in
    def login(self, signal):
        if signal == "success":
            self.update_status(True)

            
    # This function gets called at a set interval by timer.timeout
    def start_timer(self):
        # Variable to keep track of time left
        time_left = self.count - time.time()
        # This will run when there is 10 seconds left before logout
        if(time_left < 10 and time_left > 0):
            # Window to ask user to stay logged in or not
            stay_logged_in = Message("Do you want to stay logged in?", "Stay Logged In?").prompt()

            # If user wants to stay logged in reset the timer
            if stay_logged_in == QMessageBox.Yes and self.count > time.time():
                self.count = time.time() + self.duration
            # If the user wants to stay logged in but the timer expired
            elif(stay_logged_in == QMessageBox.Yes and self.count <= time.time()):
                self.timer.stop()
                self.update_status(False)
                Message("Login window has expired.", "Too Late").exec_()
            # The user doesn't want to stay signed in
            elif stay_logged_in == QMessageBox.No:
                self.update_status(False)
                self.timer.stop()
        # Stop the Timer when the manually manually logs out since self.count is set to 0 in update_status method
        elif time_left < 0:
            self.update_status(False)
            self.timer.stop()
    
    def update_status(self, logged_in):
        # If auth is on and the user is logged in
        if logged_in:
            self.logged_in = True
            self.send_signals("logged in")
            # Set the counter to the current time plus the duration of the timer
            self.count = time.time() + int(Model().read("settings")[0][5]) * 60
            self.timer.timeout.connect(self.start_timer)
            self.timer.start(1000)
        # If auth is on and the user is not logged in
        elif not logged_in:
            self.count = 0
            self.logged_in = False
            self.send_signals("logged out")

    def send_signals(self, signal):
        self.vault_tab.login_signal.emit(signal)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(ProxyStyle())
    splash_image = QPixmap(":/other/splash.png")
    splash = QSplashScreen(splash_image)
    splash.show()
    time.sleep(1)
    splash.close()
    main = Main()
    main.show()
    sys.exit(app.exec_())