import sys
import os
from operator import itemgetter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from PyQt5.QtWidgets import QComboBox

from database.model import Model

class ComboBox(QComboBox):
    current_index: int
    def showPopup(self) -> None:
        # Store the current index since it will be removed by "self.clear()"
        self.current_index = self.currentIndex()
        # Clear the old data
        self.clear()
        # Get the new groups from the database
        groups = Model().read("groups")
        
        groups = sorted(groups, key=itemgetter(1))
        # Add the groups to the combobox
        group_list = []
        for group in groups:
            group_list.append(group[1])

        self.addItems(group_list)
        # Set the original index back
        self.setCurrentIndex(self.current_index)
        # Call the parent method
        super(ComboBox, self).showPopup()