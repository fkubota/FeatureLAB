'''
scatter_mod
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


class scatter_mod(QG.QWidget):
    def __init__(self, parent=None):
        super(scatter_mod, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.resize(100, 200)
        # self.mdi.addSubWindow(self.w_scatter)


        # graph
        self.w_plot_scatter = pg.GraphicsWindow()
        self.w_plot_scatter.resize(300, 200)
        self.w_plot_scatter.setBackground('#FFFFFF00')
        self.p0_scatter = self.w_plot_scatter.addPlot()
        self.p0_scatter.showGrid(x=True, y=True, alpha=0.7)
        self.plot_scatter = pg.ScatterPlotItem(pen=(None), brush=(225,0, 0, 40))
        self.p0_scatter.addItem(self.plot_scatter)

        # self.w_plot = pg.GraphicsWindow()
        # self.p0 = self.w_plot.addPlot()
        # self.plot_scatter = pg.ScatterPlotItem(pen=(None), brush=(225, 225, 0, 20))
        # self.p0.addItem(self.scatter0)

        # widget
        self.btn_scatter = QG.QPushButton('update', self)
        # self.btn_scatter.clicked.connect(lambda : self.plot_scatter(id))
        self.lbl_scatter0 = QG.QLabel('step')
        self.le_scatter0 = (QG.QLineEdit(str(100)))
        self.cb_scatter0 = QG.QComboBox()
        self.cb_scatter0.addItems(feat_name)
        self.cb_scatter1 = QG.QComboBox()
        self.cb_scatter1.addItems(feat_name)

        # layout
        self.hbox_scatter0 = QG.QHBoxLayout()
        self.hbox_scatter0.addWidget(self.cb_scatter0)
        self.hbox_scatter0.addWidget(self.cb_scatter1)
        self.hbox_scatter1 = QG.QHBoxLayout()
        self.hbox_scatter1.addWidget(self.lbl_scatter0)
        self.hbox_scatter1.addWidget(self.le_scatter0)
        self.vbox_scatter0 = QG.QVBoxLayout()
        self.vbox_scatter0.addWidget(self.w_plot_scatter)
        self.vbox_scatter0.addLayout(self.hbox_scatter0)
        self.vbox_scatter0.addLayout(self.hbox_scatter1)
        self.vbox_scatter0.addWidget(self.btn_scatter)
        self.setLayout(self.vbox_scatter0)
        self.show()











def main():
    app = QG.QApplication(sys.argv)

    ui =scatter_mod()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()