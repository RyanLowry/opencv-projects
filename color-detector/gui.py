import sys
from PyQt5.QtWidgets import QWidget,QLabel,QMainWindow,QApplication,QGridLayout,QSlider
from PyQt5.QtCore import pyqtSlot,Qt
from tracker import Tracker
import threading



class App(QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Color detector"
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle(self.title)
        self.grid_layout = QGridLayout()
        self.addTracker()

        ## slider/label widgets
        lower_label = QLabel("Lower threshold:")
        self.lower_h = QSlider(Qt.Horizontal,self)
        self.lower_h.setRange(0,360)
        self.lower_h_label = QLabel("0",self)
        self.lower_s = QSlider(Qt.Horizontal,self)
        self.lower_s.setRange(0,255)
        self.lower_s_label = QLabel("0",self)
        self.lower_v = QSlider(Qt.Horizontal,self)
        self.lower_v.setRange(0,255)
        self.lower_v_label = QLabel("0",self)

        upper_label = QLabel("Upper threshold:")
        self.upper_h = QSlider(Qt.Horizontal,self)
        self.upper_h.setRange(0,359)
        self.upper_h.setValue(359)
        self.upper_h_label = QLabel("359",self)
        self.upper_s = QSlider(Qt.Horizontal,self)
        self.upper_s.setRange(0,255)
        self.upper_s.setValue(255)
        self.upper_s_label = QLabel("255",self)
        self.upper_v = QSlider(Qt.Horizontal,self)
        self.upper_v.setRange(0,255)
        self.upper_v.setValue(255)
        self.upper_v_label = QLabel("255",self)

        ## slider change values
        self.lower_h.valueChanged.connect(self.update_value)
        self.lower_s.valueChanged.connect(self.update_value)
        self.lower_v.valueChanged.connect(self.update_value)
        self.upper_h.valueChanged.connect(self.update_value)
        self.upper_s.valueChanged.connect(self.update_value)
        self.upper_v.valueChanged.connect(self.update_value)

        ## layout positions lower
        self.grid_layout.addWidget(lower_label,0,0)
        self.grid_layout.addWidget(self.lower_h,1,0)
        self.grid_layout.addWidget(self.lower_s,2,0)
        self.grid_layout.addWidget(self.lower_v,3,0)
        self.grid_layout.addWidget(self.lower_h_label,1,1)
        self.grid_layout.addWidget(self.lower_s_label,2,1)
        self.grid_layout.addWidget(self.lower_v_label,3,1)
        ## layout positions upper
        self.grid_layout.addWidget(upper_label,0,2)
        self.grid_layout.addWidget(self.upper_h,1,2)
        self.grid_layout.addWidget(self.upper_s,2,2)
        self.grid_layout.addWidget(self.upper_v,3,2)
        self.grid_layout.addWidget(self.upper_h_label,1,3)
        self.grid_layout.addWidget(self.upper_s_label,2,3)
        self.grid_layout.addWidget(self.upper_v_label,3,3)

        self.central = QWidget()
        self.central.setLayout(self.grid_layout)
        self.setCentralWidget(self.central)
        self.show()
    
    @pyqtSlot()
    def update_value(self):
        ## use sender to use same function, contain values, makes easier to save/send data.
        if self.sender() == self.lower_h:
            self.lower_h_label.setText("{}".format(self.lower_h.value()))
        elif self.sender() == self.lower_s:
            self.lower_s_label.setText("{}".format(self.lower_s.value()))
        elif self.sender() == self.lower_v:
            self.lower_v_label.setText("{}".format(self.lower_v.value()))
        elif self.sender() == self.upper_h:
            self.upper_h_label.setText("{}".format(self.upper_h.value()))
        elif self.sender() == self.upper_s:
            self.upper_s_label.setText("{}".format(self.upper_s.value()))
        elif self.sender() == self.upper_v:
            self.upper_v_label.setText("{}".format(self.upper_v.value()))

        self.tracker.update_bounds([self.lower_h.value(),self.lower_s.value(),self.lower_v.value()],[self.upper_h.value(),self.upper_s.value(),self.upper_v.value()])
            
    @pyqtSlot()
    def addTracker(self):
        
        self.tracker = Tracker()
        ## add threading to prevent freezing in while loop.
        self.tracker_thread = threading.Thread(target=self.tracker.track)
        self.tracker_thread.start()
                    
    def closeEvent(self,event):
        ## ends tracking thread, will stay on if not here.
        self.tracker.break_loop()
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
