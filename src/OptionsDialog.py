from PyQt4.QtGui import *
from PyQt4.QtCore import *
from init import *
import logger
import images


class OptionsDialog(QDialog):
    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent)

        logger.error_msg("__init__: Started OptionsDialog.", None)
        map_options_label = QLabel("<b>Map options:</b>")
        map_options_label.setAlignment(Qt.AlignCenter)
        min_favourited_label = QLabel("Minimum number of favourited times: ")
        self.min_favourited_lineedit = QLineEdit(str(SETTINGS['MIN_FAVOURITED']))
        self.min_favourited_lineedit.setMaximumWidth(80)
        min_difficulty_label = QLabel("Minimum difficulty of beatmap: ")
        self.min_difficulty_lineedit = QLineEdit(str(SETTINGS['MIN_DIFFICULTY']))
        self.min_difficulty_lineedit.setMaximumWidth(80)
        mapper_options_label = QLabel("<b>Mapper options:</b>")
        mapper_options_label.setAlignment(Qt.AlignCenter)
        min_ranked_label = QLabel("Minimum number of ranked maps: ")
        self.min_ranked_lineedit = QLineEdit(str(SETTINGS['MIN_RANKED']))
        self.min_ranked_lineedit.setMaximumWidth(80)
        min_non_ranked_label = QLabel("Minimum number of pending/graveyarded maps: ")
        self.min_non_ranked_lineedit = QLineEdit(str(SETTINGS['MIN_NON_RANKED']))
        self.min_non_ranked_lineedit.setMaximumWidth(80)
        min_pp_rank_label = QLabel("Minimum rank: ")
        self.min_pp_rank_lineedit = QLineEdit(str(SETTINGS['MIN_PP_RANK']))
        self.min_pp_rank_lineedit.setMaximumWidth(80)
        ok_button = QPushButton("Ok")
        cancel_button = QPushButton("Cancel")

        min_favourited_layout = QHBoxLayout()
        min_favourited_layout.addWidget(min_favourited_label)
        min_favourited_layout.addWidget(self.min_favourited_lineedit)
        min_difficulty_layout = QHBoxLayout()
        min_difficulty_layout.addWidget(min_difficulty_label)
        min_difficulty_layout.addWidget(self.min_difficulty_lineedit)
        min_ranked_layout = QHBoxLayout()
        min_ranked_layout.addWidget(min_ranked_label)
        min_ranked_layout.addWidget(self.min_ranked_lineedit)
        min_non_ranked_layout = QHBoxLayout()
        min_non_ranked_layout.addWidget(min_non_ranked_label)
        min_non_ranked_layout.addWidget(self.min_non_ranked_lineedit)
        min_pp_rank_layout = QHBoxLayout()
        min_pp_rank_layout.addWidget(min_pp_rank_label)
        min_pp_rank_layout.addWidget(self.min_pp_rank_lineedit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        button_layout.setAlignment(Qt.AlignRight)

        layout = QVBoxLayout()
        layout.addWidget(map_options_label)
        layout.addItem(min_favourited_layout)
        layout.addItem(min_difficulty_layout)
        layout.addWidget(mapper_options_label)
        layout.addItem(min_ranked_layout)
        layout.addItem(min_non_ranked_layout)
        layout.addItem(min_pp_rank_layout)
        layout.addItem(button_layout)
        self.setLayout(layout)

        self.connect(ok_button, SIGNAL("clicked()"), self.validate)
        self.connect(cancel_button, SIGNAL("clicked()"), self, SLOT("reject()"))

        self.setWindowTitle("Options")
        self.setWindowIcon(images.get_icon())

    def throw_warning(self, text, widget):
        widget.setFocus()
        QMessageBox.warning(self, "Wrong value", text)

    def validate(self):
        try:
            min_favourited = int(self.min_favourited_lineedit.text())
            if min_favourited < 0:
                raise ValueError()
        except ValueError:
            self.throw_warning("Number of favourited times should be a non-negative integer.",
                               self.min_favourited_lineedit)
            return
        try:
            min_difficulty = float(self.min_difficulty_lineedit.text())
            if min_difficulty < 0:
                raise ValueError()
        except ValueError:
            self.throw_warning("Minimum difficulty should be a non-negative number.",
                               self.min_difficulty_lineedit)
            return
        try:
            min_ranked = int(self.min_ranked_lineedit.text())
            if min_ranked < 0:
                raise ValueError()
        except ValueError:
            self.throw_warning("Number of ranked maps should be a non-negative integer.",
                               self.min_ranked_lineedit)
            return
        try:
            min_non_ranked = int(self.min_non_ranked_lineedit.text())
            if min_non_ranked < 0:
                raise ValueError()
        except ValueError:
            self.throw_warning("Number of pending/graveyarded maps should be a non-negative integer.",
                               self.min_non_ranked_lineedit)
            return
        try:
            min_pp_rank = int(self.min_pp_rank_lineedit.text())
            if min_pp_rank < 0:
                raise ValueError()
        except ValueError:
            self.throw_warning("Minimum rank of a mapper should be a non-negative integer.",
                               self.min_pp_rank_lineedit)
            return

        self.accept()
