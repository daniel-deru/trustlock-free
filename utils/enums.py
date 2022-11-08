from enum import Enum

class ServerConnectStatus(Enum):
    verified: str = "verified"
    denied: str = "denied"
    failed: str = "failed"
    
class RegisterStatus(Enum):
    user_created: str = "user created"
    window_closed: str = "window closed"
    
class LoginSignal(Enum):
    logged_in: str = "logged in"
    logged_out: str = "logged out"
    login_requested: str = "login requested"
    logout_requested: str = "logout requested"
    success: str = "success"
    failure: str = "failure"
    
class TwofaStatus(Enum):
    success: str = "success"
    failure: str = "failure"