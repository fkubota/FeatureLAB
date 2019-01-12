"""
MFCC_analysis
"""

import sys
import os
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pickle
import scatter_mod as sctr
import data_browser as db

class mfcc_analysis(QG.QMainWindow):
    def __init__(self, parent=None):
        self.feat_names = ['zcr','energy','energy_entropy','spectral_centroid','spectral_spread','spectral_entropy','spectral_flux','spectral_rolloff',
                            'mfcc_1','mfcc_2','mfcc_3','mfcc_4','mfcc_5','mfcc_6','mfcc_7','mfcc_8','mfcc_9','mfcc_10','mfcc_11','mfcc_12','mfcc_13',
                            'chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11','chroma_12','chroma_std']

        # scatter
        self.scatter = -1
        self.w_scatterV = []

        # data_browser
        self.data_id = -1
        self.dataV = []
        self.data_basenameV = []

        # constracta
        super(mfcc_analysis, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.setWindowTitle('MFCC analysis')
        self.resize(1000, 500)
        self.move(200, 100)

        # tool bar
        self.add_scatter = QG.QAction(QG.QIcon('./icon_file/plus_icon2.png'), 'scatter', self)
        self.add_scatter.triggered.connect(self.show_scatter)
        self.toolbar = self.addToolBar("")
        self.toolbar.addAction(self.add_scatter)

        # statusbar
        self.statusBar().showMessage('Ready')


        # multi window
        self.mdi = QG.QMdiArea(self)
        self.setCentralWidget(self.mdi)

        # data browser
        self.data_browser = db.data_browser(self)
        self.data_browser.btn_data0.clicked.connect(self.get_data)

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
        self.rd0.setChecked(True)
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.rd0)
        self.vbox0.addWidget(self.rd1)
        self.vbox0.addWidget(self.rd2)
        self.w0.setLayout(self.vbox0)

        #layout
        self.mdi.addSubWindow(self.data_browser)
        self.mdi.addSubWindow(self.w0)


        # self.plot()
        self.get_data()


    def get_data(self):
        self.data_id += 1
        # data_path = QG.QFileDialog.getOpenFileName(self, 'Open File', '/home/')
        # data_path = '/home/fkubota/Project/ALSOK/data/稲成ビルFeat/kubota/feat_正常音.pkl'
        # data_path = '/home/fkubota/Project/Yokogawa/data/feat/徳山201809/mfcc-0502/Yokogawa_mfcc-0502_20180831_085430.pkl'
        self.data_path = '/home/fkubota/MyData/030_GoogleDrive/Python/pyfile/my_APP/MFCC_analysis/data/sample.pkl'
        with open(self.data_path, mode='rb') as f:
            self.feat = pickle.load(f)
        self.feat = self.feat['data']
        self.dataV.append(self.feat)
        self.data_basenameV.append(os.path.basename(self.data_path))
        self.data_browser.table.setRowCount(self.data_id+1)
        self.data_browser.table.setItem(0, self.data_id, QG.QTableWidgetItem(self.data_path))

        self.update_scatter_cb()






    def show_scatter(self):

        self.scatter += 1
        self.w_scatterV.append(sctr.scatter_mod(self))
        w_scatter = self.w_scatterV[len(self.w_scatterV) -1]
        w_scatter.id = self.scatter
        w_scatter.setWindowTitle('scatter: ' + str(w_scatter.id))
        w_scatter.btn_scatter.clicked.connect(lambda : self.plot_scatter(w_scatter.id))
        w_scatter.cb_scatter0.currentIndexChanged.connect(lambda :self.plot_scatter(w_scatter.id))
        w_scatter.cb_scatter1.currentIndexChanged.connect(lambda :self.plot_scatter(w_scatter.id))
        w_scatter.le_scatter0.editingFinished.connect(lambda :self.plot_scatter(w_scatter.id))
        # for feat in self.feat_names:

        self.mdi.addSubWindow(w_scatter)
        self.update_scatter_cb()
        w_scatter.show()


    def plot_scatter(self, id):
        w_scatter = self.w_scatterV[id]
        step = int(w_scatter.le_scatter0.text())
        feat0 = self.feat[::step, int(w_scatter.cb_scatter0.currentIndex())]
        feat1 = self.feat[::step, int(w_scatter.cb_scatter1.currentIndex())]
        w_scatter.plot_scatter.setPoints(feat0, feat1)

    def update_scatter_cb(self):
        for idx in range(len(self.w_scatterV)):
            self.w_scatterV[idx].cb_scatter2.clear()
            self.w_scatterV[idx].cb_scatter2.addItems(self.data_basenameV)
            self.w_scatterV[idx].cb_scatter2.update()




def main():
    app = QG.QApplication(sys.argv)

    ui =mfcc_analysis()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
