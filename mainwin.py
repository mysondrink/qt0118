"""
@Description：主界面
@Author：mysondrink@163.com
@Time：2024/1/18 11:45
"""
# -- coding: utf-8 --
from PySide2.QtCore import Qt, QSize, QDir
from PySide2.QtWidgets import QWidget, QPushButton, QVBoxLayout, QTableView, QHBoxLayout, QFileDialog
from PySide2.QtGui import QStandardItemModel, QStandardItem
import numpy as np
import pandas as pd


class MyMainWin(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        self.setObjectName("MainWin")
        w_size = QSize(800, 600)
        self.setMinimumSize(w_size)
        layout = QVBoxLayout()
        self.setLayout(layout)
        btnOpen = QPushButton()
        btnOpen.setObjectName("btnOpen")
        btnOpen.setText("打开文件")
        btnOpen.clicked.connect(self.fileOpen)
        layout.addWidget(btnOpen)
        self.tableView = QTableView()
        self.tableView.setObjectName("tableView")
        layout.addWidget(self.tableView)
        #
        layout_1 = QHBoxLayout()
        layout.addLayout(layout_1)
        btnModify = QPushButton()
        btnModify.setObjectName("btnModify")
        btnModify.setText("修改")
        btnDump = QPushButton()
        btnDump.setObjectName("btnDump")
        btnDump.setText("保存")
        layout_1.addWidget(btnModify)
        layout_1.addWidget(btnDump)
        btnModify.hide()

    def fileOpen(self):
        path, _ = QFileDialog.getOpenFileNames(self, "open csv", QDir.currentPath(), "Data_*.csv")
        if not path:
            return
        input_table = pd.read_csv(path[0], encoding='utf-8-sig')
        input_table_rows = input_table.shape[0]
        input_table_columns = input_table.shape[1]
        input_table_header = input_table.columns.values.tolist()
        model = QStandardItemModel(input_table_rows, input_table_columns)

        for i in range(len(input_table_header)):
            model.setHeaderData(i, Qt.Horizontal, input_table_header[i])

        for j in range(input_table_rows):
            input_table_rows_values = input_table.iloc[[j]]
            input_table_rows_values_array = np.arrary(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            for k in range(input_table_columns):
                input_table_items_list = input_table_rows_values_list[k]
                item = QStandardItem(str(input_table_items_list))
                item.setTextAlignment(j, k, item)
        self.tableView.setModel(model)