import sys, pyperclip, emailScraper

from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ---Window Title and Window Icon
        self.setWindowTitle("Clipboard Email Scraper")
        self.setWindowIcon(QIcon('./assets/ESicon.png'))


        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)


        # ---contains the Title and the subtitles
        self.title = QLabel("Clipboard Email Scraper")
        self.subtitle1 = QLabel("A tool to get ALL emails from copied long text")
        self.subtitle2 = QLabel("Tip: use CTRL + A to copy the whole document and click Update button")
        

        # ---contains the labels
        self.previewLabel = QLabel("Preview:")
        self.spaceLabel = QLabel("") # empty label
        self.copiedLabel = QLabel("") # will be altered if user clicked the Copy Results Button


        # ---contains the buttons
        self.updateBtn = QPushButton("Update")
        self.scrapBtn = QPushButton("Scrap Emails")
        self.copyResultsBtn = QPushButton("Copy Results")
        self.resetBtn = QPushButton("Reset")

            # contains when the buttons are clicked
        self.updateBtn.clicked.connect(self.updateCopiedText)
        self.scrapBtn.clicked.connect(lambda: self.scrapBtnClicked(pyperclip.paste()))
        self.copyResultsBtn.clicked.connect(lambda: self.copyResultsBtnClicked(self.displayResults.toPlainText()))
        self.resetBtn.clicked.connect(self.resetBtnClicked)

            # some buttons are disabled before the display of the output
        self.copyResultsBtn.setEnabled(False)
        self.resetBtn.setEnabled(False)

            # since the buttons are designed in StyleSheet, set the cursor into pointing hand when hovered
        self.updateBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.scrapBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.copyResultsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.resetBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


        # ---contains the textbox for displaying the current copied text
        #    and the text area that will display the results in email
        self.copiedText = QLineEdit(pyperclip.paste()[:15] + "...")
        self.displayResults = QPlainTextEdit("")
        
        self.copiedText.setReadOnly(True)
        self.displayResults.setReadOnly(True)


        # ---contains horizontal layouts
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(self.previewLabel)
        hLayout1.addWidget(self.updateBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        hLayout1.addStretch()
        
        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.copiedText, alignment=Qt.AlignmentFlag.AlignLeft)
        hLayout2.addWidget(self.scrapBtn)
        hLayout2.addStretch()

        hLayout3 = QHBoxLayout()
        hLayout3.addWidget(self.copyResultsBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        hLayout3.addWidget(self.copiedLabel)
        hLayout3.addStretch()


        # ---add all the widgets in the main layout
        mainlayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlayout.addWidget(self.subtitle1, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlayout.addWidget(self.subtitle2, alignment=Qt.AlignmentFlag.AlignCenter)

        mainlayout.addWidget(self.spaceLabel)

        mainlayout.addLayout(hLayout1)
        mainlayout.addLayout(hLayout2)
        
        mainlayout.addWidget(self.spaceLabel)
        
        mainlayout.addLayout(hLayout3)
        
        mainlayout.addWidget(self.displayResults)
        mainlayout.addWidget(self.resetBtn, alignment=Qt.AlignmentFlag.AlignRight)

        mainlayout.setContentsMargins(20, 20, 20, 20)


        # set specific object names for stylesheet
        self.title.setObjectName("title")
        self.subtitle2.setObjectName("subtitle2")


        # Show the Window
        self.show()
    


    # FUNCTIONS for BUTTONS ---

    # Button Update
    def updateCopiedText(self):
        # display updated method name
        self.copiedText.setText(pyperclip.paste()[:15] + "...")

    # Button Scrap Email
    def scrapBtnClicked(self, copiedText):
        # get all emails using regex pattern, and display them in text area
        #   enable some buttons
        #   the copiedLabel is set to empty just in case user scrapped emails again 
        self.displayResults.setPlainText(emailScraper.scrapEmails(copiedText))

        self.copyResultsBtn.setEnabled(True)
        self.resetBtn.setEnabled(True)

        self.copiedLabel.setText("")

    # Button Copy Results
    def copyResultsBtnClicked(self, result):
        pyperclip.copy(result)
        self.copiedLabel.setText("Copied!")

    # Button Reset
    def resetBtnClicked(self):
        # reset the app into default mode
        self.copiedLabel.setText("")
        self.displayResults.setPlainText("")
        
        self.resetBtn.setEnabled(False)
        self.copyResultsBtn.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(Path('design.qss').read_text())

    # create the main window
    window = MainWindow()

    sys.exit(app.exec())
