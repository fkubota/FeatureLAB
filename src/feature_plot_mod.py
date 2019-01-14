'''
feature_plot
'''

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pickle



feat_name = ['zcr','energy','energy_entropy','spectral_centroid','spectral_spread','spectral_entropy','spectral_flux','spectral_rolloff',
             'mfcc_1','mfcc_2','mfcc_3','mfcc_4','mfcc_5','mfcc_6','mfcc_7','mfcc_8','mfcc_9','mfcc_10','mfcc_11','mfcc_12','mfcc_13',
             'chroma_1','chroma_2','chroma_3','chroma_4','chroma_5','chroma_6','chroma_7','chroma_8','chroma_9','chroma_10','chroma_11','chroma_12','chroma_std']


class feature_plot_mod(QG.QWidget):
    def __init__(self, parent=None):
        self.tabV = []
        self.tab_id = -1

        super(feature_plot_mod, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.setWindowTitle("feature plot")

        # graph
        self.w_feat_plot = pg.GraphicsWindow()
        self.w_feat_plot.resize(300, 200)
        self.w_feat_plot.setBackground('#FFFFFF00')
        self.p0_feat = self.w_feat_plot.addPlot()
        self.p0_feat.showGrid(x=True, y=True, alpha=0.7)

        self.curve = self.p0_feat.plot()  #
        self.curve.setData([1,2,3], [1,2,3])    #---------

        # wdiget
        self.btn0 = QG.QPushButton('add Plot')
        self.btn0.clicked.connect(self.add_data)

        # tab
        self.tab = QG.QTabWidget()
        self.tab.setFixedHeight(150)

        # layout
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.w_feat_plot)
        self.vbox0.addWidget(self.tab)
        self.vbox0.addWidget(self.btn0)
        self.setLayout(self.vbox0)


    def add_data(self):
        self.tab_id += 1
        id = self.tab_id
        self.tabV.append(w_tab())
        self.tab_new = self.tabV[id]
        self.tab_new.id = id
        self.tab.addTab(self.tab_new, 'Tab--'+str(id))

        # event



class w_tab(QG.QWidget):
   def __init__(self, parent=None):
       super(w_tab, self).__init__(parent)  # superclassのコンストラクタを使用。
       self.color = '#ff0000'

       # widget
       self.btn_scatter = QG.QPushButton('update', self)
       self.btn_color = QG.QPushButton()
       self.btn_color.setFixedWidth(20)
       self.btn_color.setFixedHeight(20)
       self.btn_color.setStyleSheet("background-color: "+self.color)
       self.lbl_scatter0 = QG.QLabel('step')
       self.lbl_scatter0.setFixedWidth(30)
       self.lbl_scatter1 = QG.QLabel('data')
       self.lbl_scatter1.setFixedWidth(30)
       self.le_scatter0 = (QG.QLineEdit(str(100)))
       self.le_scatter0.setFixedWidth(50)
       self.cb_scatter0 = QG.QComboBox()
       self.cb_scatter0.addItems(feat_name)
       self.cb_scatter1 = QG.QComboBox()
       self.cb_scatter1.addItems(feat_name)
       self.cb_scatter2 = QG.QComboBox()

       self.hbox_scatter0 = QG.QHBoxLayout()
       self.hbox_scatter0.addWidget(self.cb_scatter0)
       self.hbox_scatter0.addWidget(self.cb_scatter1)
       self.hbox_scatter1 = QG.QHBoxLayout()
       self.hbox_scatter1.addWidget(self.btn_color)
       self.hbox_scatter1.addWidget(self.lbl_scatter1)
       self.hbox_scatter1.addWidget(self.cb_scatter2)
       self.hbox_scatter1.addWidget(self.lbl_scatter0)
       self.hbox_scatter1.addWidget(self.le_scatter0)
       self.vbox_scatter0 = QG.QVBoxLayout()
       self.vbox_scatter0.addLayout(self.hbox_scatter1)
       self.vbox_scatter0.addLayout(self.hbox_scatter0)
       self.vbox_scatter0.addWidget(self.btn_scatter)
       self.setLayout(self.vbox_scatter0)





def main():
    app = QG.QApplication(sys.argv)

    ui =feature_plot_mod()
    ui.add_data()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
