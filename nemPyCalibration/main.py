from PyQt5 import QtGui, QtCore, QtWidgets
import os
from calibrationUI import Ui_CalibrationUI
#from Capture import Capture
from managers import CaptureManager
from easyEBB import EasyEBB
import cv2
import logging
import sys
import threading
from _functools import partial
from utils import Point
import serial
import time
import numpy as np

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Gui(QtWidgets.QMainWindow):

    ## Signals
    #closeGui = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        
        
        ## Instantiate classes
        self.ui = Ui_CalibrationUI()
        self.ui.setupUi(self)

        self._cap = None
        self.ebb = None
        ## Stuff you can change in the UI
        self.width = None
        self.idealRes = [1280, 960]
        self.colSteps = 0
        self.rowSteps = 0
        self.multFactor = 1
        self.motorsAble = False
        self.showImage = False

        ## Stuff that doesn't change
        #self._cap = CaptureManager( cv2.VideoCapture(0) )
        
        
        

        ## Video stuff
        self._timer = QtCore.QTimer( self )
        self._timer.timeout.connect( self.play )
        self._timer.start(27)
        self.update()

        source = [0, 1, 2,3, 'led_move1.avi', 
                  'screencast.avi',
                  'screencast 1.avi',
                  'shortNoBox.avi',
                  'longNoBox.avi',
                  'H299.avi',
                  'testRec.avi',
                  'longDemo.avi']
        for s in source:
            self.ui.sourceCombo.addItem(str(s))

        ## Register button actions
        self.ui.buttonSet.clicked.connect( self.set )
        self.ui.buttonCenter.clicked.connect( self.center )
        self.ui.buttonReset.clicked.connect( self.reset )
        self.ui.buttonSave.clicked.connect( self.save )
        self.ui.buttonRight.clicked.connect( partial( self.motors, 'right' ) )
        self.ui.buttonLeft.clicked.connect( partial( self.motors, 'left' ) )
        self.ui.buttonUp.clicked.connect( partial( self.motors, 'up' ) )
        self.ui.buttonDown.clicked.connect( partial( self.motors, 'down' ) )
        self.ui.scalingSlider.valueChanged[int].connect( self.setMultFactor )
        self.ui.scaling.setText( 'Motor scaling is %d' % self.ui.scalingSlider.value() ) 
        self.ui.sourceCombo.activated[int].connect( self.setSource )
        self.ui.comboBox.activated.connect ( self.resolutionSelect )
                


        self.setAble('settings', False)
        self.setAble('motors', False)
        self.setAble('center', False)
        self.setAble('reset', False)
        self.setAble('save', False)
    
    def setSource ( self, value ):
        if self._cap:
            if self._cap._capture.isOpened(): #ugly access to VideoCapture object from managers
                self._cap._capture.release()
        
        self._cap = CaptureManager( cv2.VideoCapture(int(value)) )
        #self.indWindow = cv2.namedWindow("Camera Display")
        self.showImage = True
        self.actualRes = self._cap.getResolution()
        self.p = Point(200,300)
        self.c = Point(self.actualRes[0] // 2, self.actualRes[1] // 2)
        self.setAble('settings', True)
    def resolutionSelect ( self ):
        # Get desired resolution from the user: 
        self.idealRes = self.ui.comboBox.currentText().split('x')
        self.idealRes = map(lambda x: int(x), self.idealRes)

        logger.debug("User input res: %d %d" % (self.idealRes[0], self.idealRes[1])  )
            
        # Attempt to change the resolution:
        self._cap.setProp('width', self.idealRes[0])
        self._cap.setProp('height', self.idealRes[1])
        self.actualRes = self._cap.getResolution()
        # Something went wrong with resolution assignment -- possible need for shut down if resolution can't even be queried
        self.c = Point(self.actualRes[0] // 2, self.actualRes[1] // 2)
        if not ( self.actualRes == self.idealRes ):
            QtWidgets.QMessageBox.information( self, "Resolution",
                                              "That resolution isn't supported by the camera. Instead, your actual resolution is: %d x %d" % (self.actualRes[0], self.actualRes[1] ) )

    def save( self ):
        c = os.path.dirname(os.getcwd())
        cc = os.path.dirname(c)
        f = open( ("%s\\config.txt" % cc) , "w")
        f.write('%d|%d|%s|%s\n' % ( self.actualRes[0], self.actualRes[1], self.ui.widthLine.text(), self.ui.sourceCombo.currentText() ))
        f.close()
        
         
        

    def setMultFactor ( self, value ):
        self.multFactor = value
        self.ui.scaling.setText( 'Step scaling is %d' % value)
    
    def setAble( self, group, ability ):
        groups = { 'motors' : [self.ui.buttonLeft, 
                               self.ui.buttonRight,
                               self.ui.buttonUp, 
                               self.ui.buttonDown, 
                               self.ui.scalingSlider, 
                               self.ui.scaling],
                  'center' : [self.ui.buttonCenter], 
                  'reset' : [self.ui.buttonReset],
                  
                  'settings': [self.ui.resDesc,
                               self.ui.framewDesc,
                               self.ui.buttonSet, 
                               self.ui.widthLine,
                               self.ui.comboBox],
                  'save': [self.ui.buttonSave]
                  }
        
        for g in groups[group]:
            g.setEnabled(ability)

            



    def motors( self, direction):
        xdir = 1
        ydir = 1
        t = 300

        dir ={ 'left': (t, xdir * self.multFactor * (-1), 0 ) ,
              'right': ( t, xdir * self.multFactor * (1), 0 ),
              'up': (t, 0, ydir * self.multFactor * (1) ),
              'down': (t, 0, ydir * self.multFactor * (-1) )
              }

        #print dir[direction]
        th = threading.Thread(target  = self.ebb.move , args = dir[direction] )
        try:
            #partial(self.ebb.move, dir[direction]) 
            th.start()
            #th.join()
        except Exception as e:
            logger.exception( str(e) )


    def reset ( self ):
        
        self.ebb.move(300, -self.colSteps, -self.rowSteps)
        if self.ebb.connected:
            self.ebb.closeSerial()

        self.setAble('settings', True)

    def center ( self ):
        #th = threading.Thread(target  = self.ebb.move , args = (100,200,300) )
        try:
            #partial(self.ebb.move, dir[direction]) 
            self.colSteps, self.rowSteps = self.ebb.centerWorm(300,200,300)
            #th.join()
        except Exception as e:
            logger.exception( str(e) )

        
        self.setAble('reset', True)
        self.setAble('save', True)
        

    def set( self ):
        if self.ui.widthLine.text():
            try:
                float( self.ui.widthLine.text() )
            except ValueError as e:
                QtWidgets.QMessageBox.information( self, "Invalid Width", "Cannot convert that width to a float! Make sure you enter a number (decimals accepted)")
                return
       
        if self.ui.widthLine.text() and self.ui.comboBox.currentText():
            self.resolutionSelect()
            # Instantiate motors    
            try:
                self.ebb = EasyEBB( resolution = self.actualRes, sizeMM = float(self.ui.widthLine.text() ) )
                  

                self.setAble('settings', False)
                self.setAble('motors', True)
                self.setAble('center', True)
            except serial.SerialException as e:
                logger.exception(e)
                QtWidgets.QMessageBox.information( self, "Motors Issue",
                                                "Please connect motors or restart them, having issues connecting now")
        else:
            QtWidgets.QMessageBox.information( self, "Validation",
                                                  "Please enter a measurement for the width and double-check your resolution choice") 

        

    def closeEvent ( self, event):
        logger.debug("closing")
        if self._cap._capture.isOpened():
            self._cap._capture.release()
        #if self._cap:
        #    cv2.destroyWindow("Camera Display")
        #    cv2.destroyAllWindows()
        if self.ebb:
            self.ebb.closeSerial()
    
    def isColor( self, imgIn ):
        try:
            ncolor = np.shape(imgIn)[2]
            boolt = int(ncolor) > 2
            return boolt
        except IndexError:
            QtWidgets.QMessageBox.information( self, "Camera Issue", "Please Check Camera Source")
            logger.error("Something wrong with camera input")
            self.showImage = False
        
         
        
    def play( self ):
        if self.showImage:
            self._cap.enterFrame()
            self.currentFrame = self._cap.frame
        
            self.color = self.isColor(self.currentFrame)
            t1 = time.time()
            if self.color:
                try:
                    self.currentFrame = cv2.cvtColor(self.currentFrame, cv2.COLOR_BGR2GRAY)
                    self.currentFrame = self.p.draw(self.currentFrame, 'gray-1')
                    self.currentFrame = self.c.draw(self.currentFrame, 'gray-1')
                    self.ui.videoFrame.setPixmap(self._cap.convertFrame(self.currentFrame))
                    self.ui.videoFrame.setScaledContents(True)
                    #cv2.imshow( "Camera Display",self.currentFrame)
                except TypeError:
                    logger.exception("No Frame")
                finally:
                    self._cap.exitFrame()
            self._cap.exitFrame()
        
    #def keyPressEvent( self, e ):
        #logger.debug('\tPressed\t%d' % e.key() )
        
        #options = {
        #           QtCore.Qt.Key_Escape : self.close(),
        #           QtCore.Qt.Key_Left : self.motors( 'left' ),
        #           QtCore.Qt.Key_Right : self.motors( 'right' ),
        #           QtCore.Qt.Key_Up : self.motors( 'up' ),
        #           QtCore.Qt.Key_Down : self.motors( 'down' ) 
        #       }
        #logging.debug( str(options[e.key()]) )
        #options[e.key()]
        
        





def main():
    app = QtWidgets.QApplication( sys.argv )
    #filter = ValEventFilter()
    #app.installEventFilter(filter)
    g = Gui()
    g.show()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()
