import sys
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
# from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import random
from datetime import datetime

#app initialization
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Tilt Table App")
window.setGeometry(300, 300, 850, 525)
window.setStyleSheet("background-color: lightgray;")

# var initialization
calValBool = False
startStopMeasureBool = False
startStopRecordingBool = False
showBothDgr = True
showXdgr = False
showYdgr= False
x_data = []
y_data = []
y_data2 = []
initData = []

def StartStopMeasurment():
    global startStopMeasureBool
    startStopMeasureBool = not startStopMeasureBool
    if startStopMeasureBool == True:
        startMeasurement.setStyleSheet("background-color: #008000; font-size: 14px; font-weight: Bold;")
        startMeasurement.setText("STOP")
    else:
        startMeasurement.setStyleSheet("background-color: #FF4444; font-size: 14px; font-weight: Bold;")
        startMeasurement.setText("START")

def ZeroCalibrate():
    calValidationLabel.show()
    global calValBool
    calValBool = True

def ShowBothDgr():
    global showBothDgr
    showBothDgr = True
    xLabel.move(80,92-62)
    yLabel.move(80,92+62)
    bothDegree.setStyleSheet("background-color: lightblue;")
    latDegreeX.setStyleSheet("")
    lonDegreeY.setStyleSheet("")
    yLabel.show()
    xLabel.show()

def ShowXdgr():
    global showXdgr
    global showBothDgr
    global showYdgr
    showYdgr = False
    showBothDgr = False
    showXdgr = True
    xLabel.move(74,92)
    bothDegree.setStyleSheet("")
    latDegreeX.setStyleSheet("background-color: lightblue;")
    lonDegreeY.setStyleSheet("")
    yLabel.hide()
    xLabel.show()

def ShowYdgr():
    global showYdgr
    global showBothDgr
    global showXdgr
    showXdgr = False
    showBothDgr = False
    showYdgr = True
    yLabel.move(74,92)
    bothDegree.setStyleSheet("")
    latDegreeX.setStyleSheet("")
    lonDegreeY.setStyleSheet("background-color: lightblue;")
    yLabel.show()
    xLabel.hide()

def StartStopRecording():
    global startStopRecordingBool
    print(startStopRecordingBool)
    startStopRecordingBool = not startStopRecordingBool

def closeEvent(self, event):
    print('t')

# Create a widget with a border
bordered_widget = QWidget(window)
bordered_widget.setStyleSheet("border: 2px solid black;")  # Set border style
bordered_widget.setGeometry(15, 410, 345, 100)  # Set position and size

graph_border = QWidget(window)
graph_border.setStyleSheet("border: 0px solid black;")  # Set border style
graph_border.setGeometry(375, 300, 460, 220)  # Set position and size was 280

degree_border = QWidget(window)
degree_border.setStyleSheet("border: 2px solid black;")  # Set border style
degree_border.setGeometry(15, 15, 520, 275)  # Set position and size

zeroCalButton = QPushButton("Zero Sensor", window)
zeroCalButton.setGeometry(30, 328, 140, 40)
zeroCalButton.clicked.connect(ZeroCalibrate)

StartRecording = QPushButton("Start Recording Data", window)
StartRecording.setGeometry(205, 328, 140, 40)
StartRecording.clicked.connect(StartStopRecording)

calValidationLabel = QLabel("✔️", window)
calValidationLabel.move(170, 333)
calValidationLabel.setStyleSheet("color: green; font-size: 20px;")
calValidationLabel.hide()

RecordingLabel = QLabel("●", bordered_widget)
RecordingLabel.move(5, 5)
RecordingLabel.setStyleSheet("color: gray; font-size: 35px; border: None")

degreeFont = QFont("Arial", 85, QFont.Normal)
xLabel = QLabel("X:  0.0°", window)
xLabel.setStyleSheet("border: 0px solid black;")
yLabel = QLabel("Y:  0.0°", window)
yLabel.setStyleSheet("border: 0px solid black;")
xLabel.setFont(degreeFont)
yLabel.setFont(degreeFont)
xLabel.move(80,92-62)
yLabel.move(80,92+62)

startMeasurement = QPushButton("START", window)
startMeasurement.setGeometry(610, 20, 180, 40)
startMeasurement.setStyleSheet("background-color: #FF4444; font-size: 14px; font-weight: Bold;")
startMeasurement.clicked.connect(StartStopMeasurment)

bothDegree = QPushButton("Both", window)
bothDegree.setGeometry(610, 120, 180, 40)
bothDegree.setStyleSheet("background-color: lightblue;")
bothDegree.clicked.connect(ShowBothDgr)

latDegreeX = QPushButton("Lateral", window)
latDegreeX.setGeometry(610, 175, 180, 40)
latDegreeX.clicked.connect(ShowXdgr)

lonDegreeY = QPushButton("Longitudinal", window)
lonDegreeY.setGeometry(610, 230, 180, 40)
lonDegreeY.clicked.connect(ShowYdgr)

# graph logic
plot_widget = PlotWidget()
plot_widget.setBackground('black')
legend = pg.LegendItem(colCount=2)
legend.setParentItem(plot_widget.graphicsItem())
layout = QVBoxLayout(graph_border)
layout.addWidget(plot_widget)
layout.setSpacing(0)


counter = 0
calValCounter = 0
xAxisCount = 0
prevSecond = -1

# PlotRoof = plot_widget.plot(xAxisCount, 40, pen='w')

def MainLoop():
    # Increment the counter and update the label
    global counter
    global calValBool
    global startStopMeasureBool
    global calValCounter
    global x_data
    global y_data
    global y_data2
    global xAxisCount
    global initData
    global showBothDgr
    global showXdgr
    global showYdgr
    global startStopRecordingBool
    global prevSecond
    if startStopRecordingBool == True and prevSecond == -1 and startStopMeasureBool == True:
        now = datetime.now()
        prev_s = now.second
        prevSecond = int(prev_s)
        RecordingLabel.setStyleSheet("color: red; border: None; font-size: 35px;")
        StartRecording.setText("Stop Recording")

    if startStopMeasureBool == False:
        prevSecond = -1
        startStopRecordingBool = False
        StartRecording.setEnabled(False)
    else:
        StartRecording.setEnabled(True)

    if calValBool == True:
        calValCounter+=1
        if calValCounter > 3:
            calValidationLabel.hide()
            calValBool = False
            calValCounter = 0

    if startStopRecordingBool == True and prevSecond != -1 and startStopMeasureBool == True:
        now = datetime.now()
        log_time = now.strftime("%H:%M:%S")
        current_second = now.second
        current_second_int = int(current_second)
        if True:
            date=now.strftime("%m-%d-%y_%H:%M:%S")
            date_string = str(date)
            file_name = f'rawdata_{date_string}'
        if prevSecond < current_second_int or (prevSecond == 59 and current_second_int == 0):
            log_string = f'{log_time}, x, y'
            print(log_string)
            prevSecond = -1
    elif startStopRecordingBool == False or startStopMeasureBool == False:
        RecordingLabel.setStyleSheet("color: gray; border: None; font-size: 35px;")
        StartRecording.setText("Start Recording")
        prevSecond = -1
    
    if startStopMeasureBool == True:
        #get a random number
        
        counter+=1
        if counter%3 == 0:
            num1 = random.randint(1,35)
            num2 = random.randint(1,8)
            x_data.append(xAxisCount)
            y_data2.append(num2)
            y_data.append(num1)
            initData.append(40)
            plot_widget.clear()
            PlotRoof = plot_widget.plot(x_data, initData, pen='black')
            if showBothDgr == True:
                PlotLon = plot_widget.plot(x_data, y_data, pen="b", name="Lat")
                PlotLat = plot_widget.plot(x_data, y_data2, pen="r", name="Lon")
            elif showXdgr == True:
                PlotLat = plot_widget.plot(x_data, y_data2, pen="r", name="Lon")
            elif showYdgr == True:
                PlotLon = plot_widget.plot(x_data, y_data, pen="b", name="Lat")
            if counter < 4:
                legend.addItem(PlotLat, "Lateral")
                legend.addItem(PlotLon, "Longitudal")
                legend.setPos(40, 0)
            # Zoom out by adjusting the x-axis range
            if len(x_data) > 25:  # Adjust this number as needed
                plot_widget.setXRange(len(x_data) - 25, len(x_data))
            xAxisCount+=1
    else:
        pass

# Set up the timer
timer = QTimer()
timer.timeout.connect(MainLoop)
timer.start(300)  # 1000 ms = 1 second

window.setWindowIcon(QIcon('test1.ico'))

window.show()

def appExec():
    app.exec_()
    print("this worked")

sys.exit(appExec())