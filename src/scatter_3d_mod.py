'''
scater_3d_mod.py
'''

import sys
import numpy as np
import PyQt4.QtGui as QG
import PyQt4.QtCore as QC
import pyqtgraph as pg
import pyqtgraph.opengl as gl
pg.setConfigOption('antialias', True)


class scatter_3d_mod(QG.QWidget):
    def __init__(self, parent=None):
        self.tabV = []
        self.tab_id = -1

        super(scatter_3d_mod, self).__init__(parent)

        # graph
        self.w_scatter_3d = gl.GLViewWidget()
        self.w_scatter_3d.addItem((gl.GLGridItem()))
        self.w_scatter_3d.addItem((gl.GLAxisItem()))
        # self.w_scatter_3d.show()

        # widget
        self.btn0 = QG.QPushButton('add Plot')
        self.btn0.clicked.connect(self.add_Data)
        self.btn0.clicked.connect(self.update_scatter_3d_cb)
        # self.btn0.mouseReleaseEvent()
        self.w_vbox0 = QG.QWidget()

        # tab
        self.tab = QG.QTabWidget()
        self.tab.setFixedHeight(150)

        # layout
        # self.vbox0 = QG.QVBoxLayout()
        # self.vbox0.addWidget(self.w_scatter)
        # self.vbox0.addWidget(self.tab)
        # self.vbox0.addWidget(self.btn0)
        # self.setLayout(self.vbox0)

        # layout
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addWidget(self.tab)
        self.vbox0.addWidget(self.btn0)
        self.w_vbox0.setLayout(self.vbox0)
        self.hsplitter0 = QG.QSplitter(QC.Qt.Vertical)
        self.hsplitter0.addWidget(self.w_scatter_3d)
        self.hsplitter0.addWidget(self.w_vbox0)
        self.hsplitter0.setSizes([400, 10])
        self.vbox1 = QG.QVBoxLayout()
        self.vbox1.addWidget(self.hsplitter0)
        self.setLayout(self.vbox1)

        self.show()

    def add_Data(self):
        self.tab_id += 1
        id = self.tab_id
        self.tabV.append(w_tab())
        self.tab_new = self.tabV[id]
        self.tab_new.id = id
        self.tab.addTab(self.tab_new, 'Tab--'+str(id))

        # event
        self.tab_new.cb_feat0.currentIndexChanged.connect(self.scatter_3d_setting_update)
        self.tab_new.cb_feat1.currentIndexChanged.connect(self.scatter_3d_setting_update)
        self.tab_new.cb_feat2.currentIndexChanged.connect(self.scatter_3d_setting_update)
        self.tab_new.cb2.currentIndexChanged.connect(self.scatter_3d_setting_update)
        self.tab_new.btn.clicked.connect(self.scatter_3d_setting_update)
        self.tab_new.le0.editingFinished.connect(self.scatter_3d_setting_update)
        self.tab_new.le_point_size.editingFinished.connect(self.scatter_3d_setting_update)
        self.tab_new.btn_color.clicked.connect(self.scatter_3d_change_color)
        self.tab_new.btn_color.clicked.connect(self.scatter_3d_setting_update)
        self.tab_new.check.stateChanged.connect(self.scatter_3d_setting_update)

        # plotitem
        self.tab_new.scatter_3d_plot_item = gl.GLScatterPlotItem()
        self.w_scatter_3d.addItem(self.tab_new.scatter_3d_plot_item)

        # self.tab_new.plot_scatter_3d = self.p0_scatter_3d.plot()

        # update comnobox
        self.update_scatter_3d_cb()

    def scatter_3d_setting_update(self):
        pass

    def scatter_3d_change_color(self):
        pass

    def update_scatter_3d_cb(self):
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
        self.lbl_point_size = QG.QLabel('size')
        self.lbl_point_size.setFixedWidth(30)
        self.le0 = QG.QLineEdit(str(100))
        self.le0.setFixedWidth(50)
        self.le_point_size = QG.QLineEdit(str(10))
        self.le_point_size.setFixedWidth(50)
        self.cb_feat0 = QG.QComboBox()
        self.cb_feat0.setSizePolicy(QG.QSizePolicy.Expanding, 20)
        self.cb_feat1 = QG.QComboBox()
        self.cb_feat1.setSizePolicy(QG.QSizePolicy.Expanding, 20)
        self.cb_feat2 = QG.QComboBox()
        self.cb_feat2.setSizePolicy(QG.QSizePolicy.Expanding, 20)
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
        self.hbox2.addWidget(self.cb_feat0)
        self.hbox2.addWidget(self.cb_feat1)
        self.hbox2.addWidget(self.cb_feat2)
        self.hbox3 = QG.QHBoxLayout()
        self.hbox3.addWidget(self.lbl_point_size)
        self.hbox3.addWidget(self.le_point_size)
        self.hbox3.addWidget(self.btn)
        self.vbox0 = QG.QVBoxLayout()
        self.vbox0.addLayout(self.hbox1)
        self.vbox0.addLayout(self.hbox2)
        self.vbox0.addLayout(self.hbox3)
        self.setLayout(self.vbox0)


def main():
    app = QG.QApplication(sys.argv)

    ui = scatter_3d_mod()
    ui.show()

    sys.exit(app.exec_())

if  __name__== '__main__':
    main()
