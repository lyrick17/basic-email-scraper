import sys, pyperclip, emailScraper

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
from PyQt6.QtGui import QFont, QIcon

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window Title and Window Icon
        self.setWindowTitle("Clipboard Email Scraper")
        #self.setWindowIcon("")

        mainlayout = QVBoxLayout()
        self.setLayout(mainlayout)


        # contains the Title and the subtitles
        title = QLabel("Clipboard Email Scraper")
        title.setObjectName("title")
        subtitle1 = QLabel("A tool to get ALL emails from copied long text")
        subtitle2 = QLabel("Tip: use CTRL + A to copy the whole document")


        # contains the labels
        previewlabel = QLabel("Preview:")
        spaceLabel = QLabel("") # empty label
        self.copiedLabel = QLabel("") # will be altered if user clicked the Copy Results Button


        # contains the buttons
        updateBtn = QPushButton("Update")
        scrapBtn = QPushButton("Scrap Emails")
        self.copyResultsBtn = QPushButton("Copy Results")
        self.resetBtn = QPushButton("Reset")
            # contains when the buttons are clicked
        updateBtn.clicked.connect(self.updateCopiedText)  # Modified connection statement
        scrapBtn.clicked.connect(lambda: self.scrapBtnClicked(pyperclip.paste()))
        self.copyResultsBtn.clicked.connect(lambda: self.copyResultsBtnClicked(self.displayResults.toPlainText()))
        self.resetBtn.clicked.connect(self.resetBtnClicked)
            # contains some buttons when they are disabled
        self.copyResultsBtn.setEnabled(False)
        self.resetBtn.setEnabled(False)
        

        # contains the textbox for displaying the current copied text
        # and the text area that will display the results in email
        self.copiedText = QLineEdit(pyperclip.paste()[:20] + "...")
        self.displayResults = QPlainTextEdit("")
        
        #self.copiedText.setEnabled(False)
        #self.displayResults.setEnabled(False)
        self.copiedText.setReadOnly(True)
        self.displayResults.setReadOnly(True)


        # contains horizontal layouts
        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(previewlabel)
        hLayout1.addWidget(updateBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        hLayout1.addStretch()
        
        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(self.copiedText, alignment=Qt.AlignmentFlag.AlignLeft)
        hLayout2.addWidget(scrapBtn)
        hLayout2.addStretch()

        hLayout3 = QHBoxLayout()
        hLayout3.addWidget(self.copyResultsBtn, alignment=Qt.AlignmentFlag.AlignLeft)
        hLayout3.addWidget(self.copiedLabel)
        hLayout3.addStretch()

        # add the widgets in the main layout
        mainlayout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlayout.addWidget(subtitle1, alignment=Qt.AlignmentFlag.AlignCenter)
        mainlayout.addWidget(subtitle2, alignment=Qt.AlignmentFlag.AlignCenter)

        mainlayout.addWidget(spaceLabel)

        mainlayout.addLayout(hLayout1)
        mainlayout.addLayout(hLayout2)
        
        mainlayout.addWidget(spaceLabel)
        
        mainlayout.addLayout(hLayout3)
        #mainlayout.addWidget(self.copyResultsBtn, alignment=Qt.AlignmentFlag.AlignLeft)

        mainlayout.addWidget(self.displayResults)
        mainlayout.addWidget(self.resetBtn, alignment=Qt.AlignmentFlag.AlignRight)

        mainlayout.setContentsMargins(20, 20, 20, 20)

        # Show the Window
        self.show()
    


    # FUNCTIONS for BUTTONS
    # Button Update
    def updateCopiedText(self):
        self.copiedText.setText(pyperclip.paste()[:20] + "...")  # Updated method name

    # Button Scrap Email
    def scrapBtnClicked(self, copiedText):
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
        self.copiedLabel.setText("")
        self.displayResults.setPlainText("")
        
        self.resetBtn.setEnabled(False)
        self.copyResultsBtn.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # create the main window
    window = MainWindow()

    sys.exit(app.exec())
