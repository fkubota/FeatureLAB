'''
feature_plot
'''

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
pg.setConfigOption('antialias', True)
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
        self.p0_feat.setLabel('bottom', 'Time', 'hour')
        self.p0_feat.showGrid(x=True, y=True, alpha=0.7)


        # wdiget
        self.btn0 = QG.QPushButton('add Plot')
        self.btn0.clicked.connect(self.add_Data)
        self.btn0.clicked.connect(self.update_feat_cb)
        self.w_vbox0 = QG.QWidget()

        # tab
        self.tab = QG.QTabWidget()
        self.tab.setFixedHeight(150)

        # # layout
        # self.vbox0 = QG.QVBoxLayout()
        # self.vbox0.addWidget(self.w_feat_plot)
        # self.vbox0.addWidget(self.tab)
        # self.vbox0.addWidget(self.btn0)
        # self.setLayout(self.vbox0)

        #layout
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.tab)
        self.vbox0.addWidget(self.btn0)
        self.w_vbox0.setLayout(self.vbox0)
        self.hsplitter0 = QG.QSplitter(QC.Qt.Vertical)
        self.hsplitter0.addWidget(self.w_feat_plot)
        self.hsplitter0.addWidget(self.w_vbox0)
        self.hsplitter0.setSizes([400, 10])
        self.vbox1 = QG.QVBoxLayout()
        self.vbox1.addWidget(self.hsplitter0)
        self.setLayout(self.vbox1)


    def add_Data(self):
        self.tab_id += 1
        id = self.tab_id
        self.tabV.append(w_tab())
        self.tab_new = self.tabV[id]
        self.tab_new.id = id
        self.tab.addTab(self.tab_new, 'Tab--'+str(id))

        # event
        self.tab_new.cb0.currentIndexChanged.connect(self.feat_setting_update)
        self.tab_new.cb2.currentIndexChanged.connect(self.feat_setting_update)
        self.tab_new.btn.clicked.connect(self.feat_setting_update)
        self.tab_new.le0.editingFinished.connect(self.feat_setting_update)
        self.tab_new.btn_color.clicked.connect(self.feat_change_color)
        self.tab_new.btn_color.clicked.connect(self.feat_setting_update)
        self.tab_new.check.stateChanged.connect(self.feat_setting_update)


        # plotitem
        self.tab_new.curve = self.p0_feat.plot()
        self.tab_new.legend = self.p0_feat.addLegend()

        # update comnobox
        self.update_feat_cb()


    def feat_setting_update(self):
        pass
    def feat_change_color(self):
        pass
    def update_feat_cb(self):
        pass


class w_tab(QG.QWidget):
   def __init__(self, parent=None):
       super(w_tab, self).__init__(parent)  # superclassのコンストラクタを使用。
       self.color = '#ff0000'

       # widget
       self.btn = QG.QPushButton('update', self)
       self.btn_color = QG.QPushButton()
       self.btn_color.setFixedWidth(20)
       self.btn_color.setFixedHeight(20)
       self.btn_color.setStyleSheet("background-color: "+self.color)
       self.lbl0 = QG.QLabel('step')
       self.lbl0.setFixedWidth(30)
       self.lbl1 = QG.QLabel('data')
       self.lbl1.setFixedWidth(30)
       self.le0 = (QG.QLineEdit(str(100)))
       self.le0.setFixedWidth(50)
       self.cb0 = QG.QComboBox()
       self.cb0.addItems(feat_name)
       self.cb2 = QG.QComboBox()
       self.cb2.setSizePolicy(QG.QSizePolicy.Expanding, 20)
       self.check = QG.QCheckBox()
       self.check.setChecked(True)

       self.hbox1 = QG.QHBoxLayout()
       self.hbox1.addWidget(self.check)
       self.hbox1.addWidget(self.lbl1)
       self.hbox1.addWidget(self.cb2)
       self.hbox1.addWidget(self.lbl0)
       self.hbox1.addWidget(self.le0)
       self.hbox2 = QG.QHBoxLayout()
       self.hbox2.addWidget(self.btn_color)
       self.hbox2.addWidget(self.cb0)
       self.vbox0 = QG.QVBoxLayout()
       self.vbox0.addLayout(self.hbox1)
       self.vbox0.addLayout(self.hbox2)
       self.vbox0.addWidget(self.btn)
       self.setLayout(self.vbox0)




def main():
    app = QG.QApplication(sys.argv)

    ui = feature_plot_mod()
    ui.add_Data()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
