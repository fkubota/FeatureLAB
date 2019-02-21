'''
scatter_mod
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


class scatter_mod(QG.QWidget):
    def __init__(self, parent=None):
        self.tabV = []
        self.tab_id = -1
        ###
        self.lastClicked = []

        super(scatter_mod, self).__init__(parent)  # superclassのコンストラクタを使用。
        # self.resize(100, 200)
        # self.mdi.addSubWindow(self.w_scatter)

        # graph
        self.w_plot_scatter = pg.GraphicsWindow()
        self.w_plot_scatter.resize(300, 200)
        self.w_plot_scatter.setBackground('#FFFFFF00')
        self.p0_scatter = self.w_plot_scatter.addPlot()
        self.p0_scatter.showGrid(x=True, y=True, alpha=0.7)

        # widget
        self.btn0 = QG.QPushButton('add Plot')
        self.btn0.clicked.connect(self.add_data)
        self.btn0.clicked.connect(self.update_scatter_cb)
        # self.btn0.mouseReleaseEvent()
        self.w_vbox0 = QG.QWidget()

        # tab
        self.tab = QG.QTabWidget()
        self.tab.setFixedHeight(150)

        # layout
        # self.vbox0 = QG.QVBoxLayout()
        # self.vbox0.addWidget(self.w_plot_scatter)
        # self.vbox0.addWidget(self.tab)
        # self.vbox0.addWidget(self.btn0)
        # self.setLayout(self.vbox0)

        # layout
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.tab)
        self.vbox0.addWidget(self.btn0)
        self.w_vbox0.setLayout(self.vbox0)
        self.hsplitter0 = QG.QSplitter(QC.Qt.Vertical)
        self.hsplitter0.addWidget(self.w_plot_scatter)
        self.hsplitter0.addWidget(self.w_vbox0)
        self.hsplitter0.setSizes([400, 10])
        self.vbox1 = QG.QVBoxLayout()
        self.vbox1.addWidget(self.hsplitter0)
        self.setLayout(self.vbox1)

        self.show()

    def add_data(self):
        self.tab_id += 1
        id = self.tab_id
        self.tabV.append(w_tab())
        self.tab_new = self.tabV[id]
        self.tab_new.id = id
        self.tab.addTab(self.tab_new, 'Tab--'+str(id))
        # self.cb_group.addButton(self.btn0, id)

        # event
        self.tab_new.cb_scatter0.currentIndexChanged.connect(self.setting_update)
        self.tab_new.cb_scatter1.currentIndexChanged.connect(self.setting_update)
        self.tab_new.cb_scatter2.currentIndexChanged.connect(self.setting_update)
        self.tab_new.btn_scatter.clicked.connect(self.setting_update)
        self.tab_new.le_scatter0.editingFinished.connect(self.setting_update)
        self.tab_new.btn_color.clicked.connect(self.change_color)
        self.tab_new.btn_color.clicked.connect(self.setting_update)
        self.tab_new.check.stateChanged.connect(self.setting_update)

        # plotitem
        self.tab_new.plot_scatter = pg.ScatterPlotItem(pen=(None), brush=(225,0, 0, 40), name="tab : " + str(id))
        self.p0_scatter.addItem(self.tab_new.plot_scatter, name='hello')
        self.textitem = pg.TextItem('', color='b')
        self.p0_scatter.addItem(self.textitem)
        self.tab_new.plot_scatter.sigClicked.connect(self.point_clicked)
        self.p0_scatter.hasTab = self.tab_new

        # update combobox
        self.update_scatter_cb()

    def point_clicked(self, plot, points):
        pass
        # # print(plot.getViewWidget())
        # # print(plot.getViewWidget().parent())
        # # print(plot.getViewWidget().parent().parent())
        # p0_scatter = plot.getViewWidget().parent().parent().p0_scatter
        # tab = p0_scatter.hasTab
        # data_idx = tab.cb_scatter2.currentIndex()
        # pos = points[0].pos()
        # textitem = plot.getViewWidget().parent().parent().textitem
        #
        #
        #
        #
        # # print(textitem)
        # # text = pg.TextItem(str(pos), color='b')#, pos=(pos[0], pos[1]))
        # textitem.setPos(pos[0], pos[1])
        # textitem.setText(str(pos))
        # textitem.setVisible(True)
        # # w_plot_scatter.addItem(textitem)
        # # print(points[0].parent())
        # # print(points[0].parent())
        # for p in self.lastClicked:
        #     p.resetPen()
        # for p in points:
        #     if p == points[0]:
        #         p.setPen('b', width=2)
        # self.lastClicked = points

    def setting_update(self):
        pass

    def change_color(self):
        pass

    def update_scatter_cb(self):
        pass






class w_tab(QG.QWidget):
    def __init__(self, parent=None):
        super(w_tab, self).__init__(parent)  # superclassのコンストラクタを使用。
        self.color = '#ff0000'

        # widget
        self.btn_scatter = QG.QPushButton('update', self)
        self.btn_color = QG.QPushButton()
        self.btn_color.setFixedWidth(20)
        self.btn_color.setFixedHeight(20)
        # self.btn_color.setFixedHeight(20)
        self.btn_color.setStyleSheet("background-color: "+self.color)
        self.lbl_scatter0 = QG.QLabel('step')
        self.lbl_scatter0.setFixedWidth(30)
        self.lbl_scatter1 = QG.QLabel('data')
        self.lbl_scatter1.setFixedWidth(30)
        self.le_scatter0 = (QG.QLineEdit(str(100)))
        self.le_scatter0.setFixedWidth(50)
        self.cb_scatter0 = QG.QComboBox()
        # self.cb_scatter0.addItems(feat_name)
        self.cb_scatter1 = QG.QComboBox()
        # self.cb_scatter1.addItems(feat_name)
        self.cb_scatter2 = QG.QComboBox()
        self.cb_scatter2.setSizePolicy(QG.QSizePolicy.Expanding, 20)
        self.check = QG.QCheckBox()
        self.check.setChecked(True)

        self.hbox_scatter0 = QG.QHBoxLayout()
        self.hbox_scatter0.addWidget(self.btn_color)
        self.hbox_scatter0.addWidget(self.cb_scatter0)
        self.hbox_scatter0.addWidget(self.cb_scatter1)
        self.hbox_scatter1 = QG.QHBoxLayout()
        self.hbox_scatter1.addWidget(self.check)
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

    ui =scatter_mod()
    ui.add_data()
    # ui = w_tab()
    ui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()