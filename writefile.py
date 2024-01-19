"""
@Description：覆盖文件线程类
@Author：mysondrink@163.com
@Time：2024/1/19 9:24
"""
from PySide2.QtCore import QThread, Signal
import pandas as pd
import os


class WriteNewFile(QThread):
    def __init__(self, data):
        super().__init__()
        self.csv_data = data

    def run(self) -> None:
        save_path = './new_data.xlsx'
        dataone = pd.DataFrame(self.csv_data)
        head = ["序号", "图片名称", "时间", "样本条码", "医生", "类别",
                "阵列", "病人名", "病人性别", "病人年龄", "数据"]
        if os.path.exists(save_path):
            # 追加
            with pd.ExcelWriter(save_path, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                dataone.to_excel(writer, sheet_name="Sheet2", startrow=writer.sheets["Sheet1"].max_row,
                                 index=False, header=False)
        else:
            # 新建
            with pd.ExcelWriter(save_path, mode="w", engine="openpyxl") as writer:
                dataone.to_excel(writer, sheet_name="Sheet2", header=head, index=False)
