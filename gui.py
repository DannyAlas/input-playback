from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QFileDialog
)
import sys
sys.argv += ['-platform', 'windows:darkmode=2']

from main import Recorder, Player

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.recorder = Recorder
        self.player = Player

        self.setWindowTitle("Logging thing")
        self.file = None
        self.layout = QVBoxLayout() # type: ignore
        
        # add a file dialog to select the location to save the data
        self.file_dialog = QFileDialog()
        self.file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        self.file_dialog.setOption(QFileDialog.Option.ShowDirsOnly, True)

        # set the default location to the current directory
        self.file_dialog.setDirectory(".")

        # button to open the file dialog
        self.file_dialog_button = QPushButton("Select location")
        self.file_dialog_button.clicked.connect(lambda: self.set_file(self.file_dialog))
        self.layout.addWidget(self.file_dialog_button)
        
        # show the current file location
        self.file_label = QLabel("No file selected")
        self.layout.addWidget(self.file_label)

        # add the record and play buttons
        self.record_b = QPushButton("Record")
        self.layout.addWidget(self.record_b)
        self.play_b = QPushButton("Play")
        self.layout.addWidget(self.play_b)
        
        # set the buttons to disabled by default
        self.record_b.setEnabled(False)
        self.play_b.setEnabled(False)

        # connect the buttons to their functions
        self.record_b.clicked.connect(self.start_recording)
        self.play_b.clicked.connect(self.start_playing)

    def set_file(self, file_dialog):
        file = file_dialog.getExistingDirectory()

        if file == "" or None:
            self.record_b.setEnabled(False)
            self.play_b.setEnabled(False)
        elif file != None:
            self.file_label.setText(file)
            self.record_b.setEnabled(True)
            self.play_b.setEnabled(True)
            self.file = file
            print(self.file)
    
    def start_recording(self):
        assert self.file != None
        self.recorder(location=self.file).start()

    def start_playing(self):
        assert self.file != None
        self.player(location=self.file).play()
        


app = QApplication(sys.argv)
app.setStyle('Fusion')
window = MainWindow()
window.show()
app.exec()