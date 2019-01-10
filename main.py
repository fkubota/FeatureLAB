"""
MFCC_analysis
"""

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pickle


class mfcc_analysis(QG.QMainWindow):
    def __init__(self, parent=None):
        self.scatter = -1
        self.w_scatterV = []

        # constracta
        super(mfcc_analysis, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.resize(1000, 700)
        self.move(200, 200)

        # tool bar
        self.add_scatter = QG.QAction(QG.QIcon('./icon_file/plus_icon2.png'), 'scatter', self)
        self.add_scatter.triggered.connect(self.show_scatter)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.add_scatter)


        # multi window
        self.mdi = QG.QMdiArea(self)
        self.setCentralWidget(self.mdi)


        # widget rd0
        self.w0 = QG.QWidget(self)
        self.w0.resize(100,100)
        self.rd0 = QG.QRadioButton('feat0')
        self.rd1 = QG.QRadioButton('feat1')
        self.rd2 = QG.QRadioButton('feat2')
        self.group0 = QG.QButtonGroup(self)
        self.group0.addButton(self.rd0, 0)
        self.group0.addButton(self.rd1, 1)
        self.group0.addButton(self.rd2, 2)
        self.group0.buttonClicked.connect(self.plot)
        self.rd0.setChecked(True)
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.rd0)
        self.vbox0.addWidget(self.rd1)
        self.vbox0.addWidget(self.rd2)
        self.w0.setLayout(self.vbox0)



        # グラフウィンドウ
        self.w_plot = pg.GraphicsWindow()
        self.w_plot.resize(300,300)
        self.p0 = self.w_plot.addPlot()
        self.scatter0 = pg.ScatterPlotItem(pen=(None), brush=(225, 225, 0, 20))
        self.p0.addItem(self.scatter0)

        #layout
        self.mdi.addSubWindow(self.w0)
        self.mdi.addSubWindow(self.w_plot)



        # self.plot()

    def plot(self):
        print(self.group0.checkedId())
        feat0 = self.group0.checkedId()
        # feat_path = '/home/fkubota/Project/ALSOK/data/稲成ビルFeat/kubota/feat_正常音.pkl'
        # with open(feat_path, mode='rb') as f:
        #     feat = pickle.load(f)


        # self.scatter0.setPoints(feat[::100, 15], feat[::100, feat0*10])




    def show_scatter(self):
        self.scatter += 1
        self.w_scatterV.append(QG.QWidget())
        self.mdi.addSubWindow(self.w_scatterV[self.scatter])

        self.btn = QG.QPushButton('hello', self.w_scatterV[self.scatter])
        self.vbox_scatter0 = QG.QVBoxLayout()
        self.vbox_scatter0.addWidget(self.btn)
        self.w_scatterV[self.scatter].setLayout(self.vbox_scatter0)
        self.w_scatterV[self.scatter].show()






def main():
    app = QG.QApplication(sys.argv)

    ui =mfcc_analysis()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
