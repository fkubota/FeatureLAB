



from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import pandas as pd
path = '/home/fkubota/Project/JR_west/音による異常検知装置の開発/20190208_JR西_博多工場/data/20190208_車両音1_分割/feat/セットアップ作業音_1.csv'
data = pd.read_csv(path)
data2 = np.array(data.iloc[:,0:3])

appo = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()

g = gl.GLGridItem()
w.addItem(g)



sp = gl.GLScatterPlotItem(pos=data2)

w.addItem(sp)



if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
