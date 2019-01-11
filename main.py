"""
MFCC_analysis
"""

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pickle
import scatter_mod as sctr

class mfcc_analysis(QG.QMainWindow):
    def __init__(self, parent=None):
        self.feat_names = ['zcr','energy','energy_entropy','spectral_centroid','spectral_spread','spectral_entropy','spectral_flux','spectral_rolloff',
                            'mfcc_1','mfcc_2','mfcc_3','mfcc_4','mfcc_5','mfcc_6','mfcc_7','mfcc_8','mfcc_9','mfcc_10','mfcc_11','mfcc_12','mfcc_13',
                            'chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11','chroma_12','chroma_std']


        # scatter
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

        # data browser
        self.w_data0 = QG.QWidget(self)
        self.w_data0.resize(100, 100)
        self.le_data0 = QG.QLineEdit(self)
        self.btn_data0 = QG.QPushButton('...')
        self.btn_data0.setFixedWidth(25)
        self.btn_data0.clicked.connect(self.get_data)
        self.hbox_data0= QG.QHBoxLayout()
        self.hbox_data0.addWidget(self.le_data0)
        self.hbox_data0.addWidget(self.btn_data0)
        self.w_data0.setLayout(self.hbox_data0)


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
        self.mdi.addSubWindow(self.w_data0)
        self.mdi.addSubWindow(self.w0)


        # self.plot()
        self.get_data()


    def get_data(self):
        # data_path = QG.QFileDialog.getOpenFileName(self, 'Open File', '/home/')
        data_path = '/home/fkubota/Project/ALSOK/data/稲成ビルFeat/kubota/feat_正常音.pkl'
        self.le_data0.setText(data_path)
        with open(data_path, mode='rb') as f:
            self.feat = pickle.load(f)



    def show_scatter(self):

        self.scatter += 1
        self.w_scatterV.append(sctr.scatter_mod(self))
        w_scatter = self.w_scatterV[len(self.w_scatterV) -1]
        w_scatter.id = self.scatter
        w_scatter.btn_scatter.clicked.connect(lambda : self.plot_scatter(w_scatter.id))
        w_scatter.cb_scatter0.currentIndexChanged.connect(lambda :self.plot_scatter(w_scatter.id))
        w_scatter.cb_scatter1.currentIndexChanged.connect(lambda :self.plot_scatter(w_scatter.id))
        w_scatter.le_scatter0.editingFinished.connect(lambda :self.plot_scatter(w_scatter.id))
        # for feat in self.feat_names:

        self.mdi.addSubWindow(w_scatter)
        w_scatter.show()


    def plot_scatter(self, id):
        w_scatter = self.w_scatterV[id]
        step = int(w_scatter.le_scatter0.text())
        feat0 = self.feat[::step, int(w_scatter.cb_scatter0.currentIndex())]
        feat1 = self.feat[::step, int(w_scatter.cb_scatter1.currentIndex())]
        w_scatter.plot_scatter.setPoints(feat0, feat1)

        # self.scatter0.setPoints(feat[::100, 15], feat[::100, feat0*10])


def main():
    app = QG.QApplication(sys.argv)

    ui =mfcc_analysis()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
