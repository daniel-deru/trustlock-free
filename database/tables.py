from msilib import Table
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from enum import Enum

class TableEnum(Enum):
    apps = 'apps'
    notes = 'notes'
    todos = 'todos'
    settings = 'settings'
    user = 'user'
    vault = 'vault'
    metadata = 'metadata'
    groups = 'groups'
    
  

class Tables:
            
    apps = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "path": "TEXT NOT NULL",
        "sequence": "INTEGER NOT NULL",
        "group_id": "INTEGER",
    }
    
    notes = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "body": "TEXT",
        "group_id": "INTEGER",
    }
    
    settings = {
        "id": "TEXT PRIMARY KEY",
        "nightmode": "TEXT NOT NULL",
        "font": "TEXT NOT NULL",
        "color": "TEXT NOT NULL",
        "vault_on": "TEXT NOT NULL",
        "timer": "TEXT NOT NULL",
        "calendar": "TEXT NOT NULL",
        "twofa": "TEXT",
        "auto_save": "TEXT"
    }
    
    vault = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "type": "TEXT NOT NULL",
        "name": "TEXT NOT NULL",
        "data": "TEXT NOT NULL",
        "group_id": "INTEGER",
    }
    
    metadata = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "data": "TEXT NOT NULL"
    }
    
    groups = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "description": "TEXT NOT NULL"
    }
    
    user = {
        "id": "TEXT PRIMARY KEY",
        "name": "TEXT",
        "email": "TEXT",
        "password": "TEXT",
        "passphrase": "TEXT",
        "twofa_key": "TEXT",
        "password_exp": "TEXT",
        "last_update_request": "TEXT",
    }
    
    todos = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "complete": "TEXT NOT NULL",
        "deadline": "TEXT",
        "description": "TEXT",
        "group_id": "INTEGER",
    }
    
    tablesDict = {
        TableEnum.apps.name:        apps,
        TableEnum.notes.name:       notes,
        TableEnum.todos.name:       todos,
        TableEnum.settings.name:    settings,
        TableEnum.user.name:        user,
        TableEnum.vault.name:       vault,
        TableEnum.metadata.name:    metadata,
        TableEnum.groups.name:      groups
    }