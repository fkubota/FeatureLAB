'''
sub_plot_mod
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


class sub_plot_mod(QG.QWidget):
    def __init__(self, parent=None):
        self.tabV = []
        self.tab_id = -1

        super(sub_plot_mod, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.setWindowTitle("sub_plot")

        # graph
        self.w_sub_plot = pg.GraphicsWindow()
        self.w_sub_plot.resize(1300, 1000)
        self.w_sub_plot.setBackground('#FFFFFF00')
        self.plots = []
        for idx, feat in enumerate(feat_name):
            self.plots.append(self.w_sub_plot.addPlot(title=feat))
            self.plots[idx].showGrid(x=True, y=True, alpha=0.7)
            if (1+idx)%6 == 0:
                self.w_sub_plot.nextRow()


        # wdiget
        self.btn0 = QG.QPushButton('add Plot')
        self.btn0.clicked.connect(self.add_Data)
        self.btn0.clicked.connect(self.update_sub_cb)
        self.w_vbox0 = QG.QWidget()
        # self.hbox = QG.QHBoxLayout()
        # self.hbox.addWidget(self.w_sub_plot)
        self.scrollArea = QG.QScrollArea()
        self.scrollArea.setWidget(self.w_sub_plot)
        # self.scrollArea.setWidget(self.hbox)

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
        # self.hsplitter0.addWidget(self.w_sub_plot)
        self.hsplitter0.addWidget(self.scrollArea)
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
        # self.tab_new.at_window = self
        self.tab.addTab(self.tab_new, 'Tab--'+str(id))

        # event
        self.tab_new.cb2.currentIndexChanged.connect(self.sub_setting_update)
        self.tab_new.btn.clicked.connect(self.sub_setting_update)
        self.tab_new.le0.editingFinished.connect(self.sub_setting_update)
        self.tab_new.le1.editingFinished.connect(self.sub_setting_update)
        self.tab_new.btn_color.clicked.connect(self.sub_change_color)
        self.tab_new.btn_color.clicked.connect(self.sub_setting_update)
        self.tab_new.check.stateChanged.connect(self.sub_setting_update)
        self.tab_new.btn_doit.clicked.connect(self.sub_doit)
        self.tab_new.btn.clicked.connect(self.zoom_in)

        # plotitem
        self.tab_new.curves = []
        for idx in range(34):
            self.tab_new.curves.append(self.plots[idx].plot())


        # update comnobox
        self.update_sub_cb()

    def zoom_out(self):
        pass

    def zoom_in(self):
        size = self.w_sub_plot.size()
        w = size[0]



    def sub_setting_update(self):
        pass
    def sub_change_color(self):
        pass
    def update_sub_cb(self):
        pass
    def sub_doit(self):
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
        self.btn_doit = QG.QPushButton('Do It')
        self.lbl0 = QG.QLabel('step')
        self.lbl0.setAlignment(QC.Qt.AlignRight)
        self.lbl1 = QG.QLabel('data')
        self.lbl1.setFixedWidth(30)
        self.le0 = QG.QLineEdit(str(100))
        self.le0.setFixedWidth(50)
        self.le1 = QG.QLineEdit(str(20))
        self.le1.setFixedWidth(50)
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
        self.hbox2.addWidget(self.btn_doit)
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addLayout(self.hbox1)
        self.vbox0.addLayout(self.hbox2)
        self.vbox0.addWidget(self.btn)
        self.setLayout(self.vbox0)




def main():
    app = QG.QApplication(sys.argv)

    ui = sub_plot_mod()
    ui.add_Data()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
