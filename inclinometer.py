import sys
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import csv
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import os
from datetime import datetime
from gpiozero import MCP3004
import subprocess
command = ['nohup', 'python3', '/home/coopproject/AppCode/PowerOff.py', '&']
subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#app initialization
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Tilt Table App")
window.setGeometry(140, 170, 850, 525)
window.setFixedSize(850, 525)
window.setStyleSheet("background-color: lightgray;")

chy = MCP3004(1)    #set y axis green
chx = MCP3004(0)    #set x axis white

# var initialization
calValBool = False
startStopMeasureBool = False
startStopRecordingBool = False
showBothDgr = True
showXdgr = False
showYdgr= False
first_loop_recording_bool = True
log_time = 0
x_zero = 0
y_zero = 0
x_data = []
y_data = []
y_data2 = []
initData = []
file_name = ""

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
    global x_zero
    x_zero = chx.value
    global y_zero
    y_zero = chy.value
    xLabel.setText(f'X: 0.0°   ')
    yLabel.setText(f'Y: 0.0°   ')
    save_calibration()

def ShowBothDgr():
    global showBothDgr
    showBothDgr = True
    xLabel.move(70,92-62)
    yLabel.move(70,92+62)
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
    xLabel.move(70,92)
    bothDegree.setStyleSheet("")
    latDegreeX.setStyleSheet("background-color: red;")
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
    yLabel.move(70,92)
    bothDegree.setStyleSheet("")
    latDegreeX.setStyleSheet("")
    lonDegreeY.setStyleSheet("background-color: lightblue;")
    yLabel.show()
    xLabel.hide()

def StartStopRecording():
    global startStopRecordingBool
    startStopRecordingBool = not startStopRecordingBool


# Create a widget with a border
bordered_widget = QWidget(window)
bordered_widget.setStyleSheet("border: 2px solid black;")  # Set border style
bordered_widget.setGeometry(15, 410, 345, 100)  # Set position and size

file_recorded_label = QLabel('not recording data...                     ', bordered_widget)
file_recorded_label.setStyleSheet("border: 0px solid black;")
file_recorded_label.move(60, 42)

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
xLabel.move(70,92-62)
yLabel.move(70,92+62)

startMeasurement = QPushButton("START", window)
startMeasurement.setGeometry(610, 20, 180, 40)
startMeasurement.setStyleSheet("background-color: #FF4444; font-size: 14px; font-weight: Bold;")
startMeasurement.clicked.connect(StartStopMeasurment)

bothDegree = QPushButton("Both", window)
bothDegree.setGeometry(610, 120, 180, 40)
bothDegree.setStyleSheet("background-color: blue;")
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
plot_widget.setYRange(-50, 62)


counter = 0
calValCounter = 0
xAxisCount = 0
prevSecond = -1

def save_calibration():
    save_cal = QMessageBox()
    save_cal.setWindowTitle("Confirm Calibration...")
    save_cal.setText("Would you like to save this calibration to the system?")
    save_cal.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    save_cal.exec_()
    if save_cal.standardButton(save_cal.clickedButton()) == QMessageBox.Yes:
        global x_zero
        global y_zero
        file_path = f'/home/coopproject/AppCode/calibration.txt'
        with open(file_path, mode='w') as file:
            file.write(f'{x_zero}\n')
            file.write(f'{y_zero}\n')
    else:
        pass

def init_calibration():
    file_path = f'/home/coopproject/AppCode/calibration.txt'
    arr = []
    if os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as f:
            for line in f:
                arr.append(float(line))
        global x_zero
        global y_zero
        x_zero = arr[0]
        y_zero = arr[1]
    

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
    global x_zero
    global y_zero
    global log_time
    global first_loop_recording_bool
    global file_name
    
    # incl logic for reading analog
    buffer_size = 100
    x_axis = []
    y_axis = []
    
    if startStopMeasureBool == True:
        
        StartRecording.setEnabled(True)
        
        chy = MCP3004(1)    #set y axis green
        chx = MCP3004(0)    #set x axis white

        #Fill up buffer
        while len(x_axis) < buffer_size and len(y_axis) < buffer_size:
            x_axis.append(chx.value)
            y_axis.append(chy.value)
            
        # average of current buffer
        x_average = 0.0
        y_average = 0.0
        for i in range(0, buffer_size):
            x_average += x_axis[i]
            y_average += y_axis[i]
        x_average /= buffer_size
        y_average /= buffer_size
        
        #calculate degree
        x_average = (5*(x_average - x_zero)/.0553)
        y_average = (5*(y_average - y_zero)/.0552)
        
        if x_average > -0.1 and x_average < 0:
            x_average = 0
        if y_average > -0.1 and y_average < 0:
            y_average = 0
        
        if x_average > 9.9 or y_average > 9.9 or x_average < 0 or y_average < 0:
            degreeFont = QFont("Arial", 72, QFont.Normal)
            xLabel.setFont(degreeFont)
            yLabel.setFont(degreeFont)
        else:
            degreeFont = QFont("Arial", 85, QFont.Normal)
            xLabel.setFont(degreeFont)
            yLabel.setFont(degreeFont)
        
        xLabel.setText(f'X: {x_average:.1f}°   ')
        yLabel.setText(f'Y: {y_average:.1f}°   ')
        
        #graph logic
        x_data.append(xAxisCount)
        y_data2.append(x_average)
        y_data.append(y_average)
        initData.append(50)
        plot_widget.clear()
        PlotRoof = plot_widget.plot(x_data, initData, pen='black')
        if showBothDgr == True:
            PlotLon = plot_widget.plot(x_data, y_data, pen="b", name="Lat")
            PlotLat = plot_widget.plot(x_data, y_data2, pen="r", name="Lon")
        elif showXdgr == True:
            PlotLat = plot_widget.plot(x_data, y_data2, pen="r", name="Lon")
        elif showYdgr == True:
            PlotLon = plot_widget.plot(x_data, y_data, pen="b", name="Lat")
        if xAxisCount == 0:
            legend.addItem(PlotLat, "Lateral")
            legend.addItem(PlotLon, "Longitudal")
            legend.setPos(40, 0)
            # Zoom out by adjusting the x-axis range
        if len(x_data) > 25:  # Adjust this number as needed
            plot_widget.setXRange(len(x_data) - 25, len(x_data))
        xAxisCount+=1
    else:
        prevSecond = -1
        startStopRecordingBool = False
        StartRecording.setEnabled(False)
    
    if prevSecond == -1 and startStopMeasureBool == True:
        now = datetime.now()
        prev_s = now.second
        prevSecond = int(prev_s)
        RecordingLabel.setStyleSheet("color: red; border: None; font-size: 35px;")
        StartRecording.setText("Stop Recording")

    if calValBool == True:
        calValCounter+=1
        if calValCounter > 3:
            calValidationLabel.hide()
            calValBool = False
            calValCounter = 0

    if startStopRecordingBool == True and prevSecond != -1 and startStopMeasureBool == True:
        now = datetime.now()
        log_time += 2
        current_second = now.second
        current_second_int = int(current_second)
        if first_loop_recording_bool:
            date=now.strftime("%m%d_%H%M%S")
            date_string = str(date)
            file_name_display = f'rawdata_{date_string}.csv'
            file_name = f'/home/coopproject/Desktop/Recorded Data/rawdata_{date_string}.csv'
            with open(file_name, mode='w', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\')
                writer.writerow(["second x y"])
            file_recorded_label.setText(f'File: {file_name_display}')
            first_loop_recording_bool = False
        if prevSecond < current_second_int or (prevSecond == 59 and current_second_int == 0):
            log_string = f'{int(log_time/10)} {x_average:.1f} {y_average:.1f}'
            with open(file_name, mode='a', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar='\\')
                writer.writerow([log_string])
            prevSecond = -1
    elif startStopRecordingBool == False or startStopMeasureBool == False:
        RecordingLabel.setStyleSheet("color: gray; border: None; font-size: 35px;")
        StartRecording.setText("Start Recording")
        file_recorded_label.setText(f'not recording data...                       ')
        log_time = 0
        prevSecond = -1
        first_loop_recording_bool = True
    

# Set up the timer
timer = QTimer()
timer.timeout.connect(MainLoop)
timer.start(200)  # 1000 ms = 1 second

init_calibration()
window.show()

def appExec():
    app.exec_()

sys.exit(appExec())
