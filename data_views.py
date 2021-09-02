#最高工资图
import pandas as pd
from pandas import DataFrame,Series
from matplotlib import pyplot as plt

class data_to_view():
    def __init__(self,xlsx_name):
        self.xl_name = xlsx_name
        self.max_salary()
        self.min_salary()
        self.edu_requirements()

    def max_salary(self):
        max_file_name = self.xl_name
        read_name_max = "%s.xlsx"%max_file_name
        df = pd.read_excel(read_name_max)  # excel
        df['工资'][df['工资'].str.findall('-').str.len() != 1] = '0-0'  # 处理数据，把工资一列变成确定的格式
        low = df['工资'].str.replace('K', '').str.split('-').str[1].astype('float')  # 把工资的列转换成float格式
        df['工资'] = low
        df = df.sort_values(by="工资")  # 根据工资进行排序
        low = df['工资']
        people = df['需求人数'].astype('int')  # 把需求人数一列转换成整型
        fig = plt.figure(figsize=(12, 6))  # 定义画布，大小为（12，6）
        axe = fig.add_subplot(1, 1, 1)  # 添加图标
        plt.rcParams['font.sans-serif'] = ['simhei']  # 显示中文
        x = low.tolist()
        y = people.tolist()
        axe.scatter(x, y, marker='.')
        max_title_name = max_file_name+"最高工资人数需求散点图"
        axe.set_title(max_title_name)  # 标题
        axe.set_xlabel("工 资(单位/千)", fontsize=13)  # x轴标签
        axe.set_ylabel("需 要 人 数", fontsize=13)  # y轴标签
        max_svg_name = max_file_name+"最高工资人数需求散点图.svg"
        plt.savefig(max_svg_name)  # 保存

    def min_salary(self):
        min_file_name = self.xl_name
        read_name_min = "%s.xlsx"%min_file_name
        df = pd.read_excel(read_name_min)  # excel
        df['工资'][df['工资'].str.findall('-').str.len() != 1] = '0-0'  # 处理数据，把工资一列变成确定的格式
        low = df['工资'].str.replace('K', '').str.split('-').str[0].astype('float')  # 把工资的列转换成float格式
        df['工资'] = low
        df = df.sort_values(by="工资")  # 根据工资进行排序
        low = df['工资']
        people = df['需求人数'].astype('int')  # 把需求人数一列转换成整型
        fig = plt.figure(figsize=(12, 6))  # 定义画布，大小为（12，6）
        axe = fig.add_subplot(1, 1, 1)  # 添加图标
        plt.rcParams['font.sans-serif'] = ['simhei']  # 显示中文
        x = low.tolist()
        y = people.tolist()
        axe.scatter(x, y, marker='.')
        min_title_name =min_file_name + "最低工资人数需求散点图"
        axe.set_title(min_title_name)  # 标题
        axe.set_xlabel("工 资(单位/千)", fontsize=13)  # x轴标签
        axe.set_ylabel("需 要 人 数", fontsize=13)  # y轴标签
        min_svg_name = min_file_name+'最低工资人数需求散点图.svg'
        plt.savefig(min_svg_name)  # 保存

    def edu_requirements(self):
        cyl_file_name = self.xl_name
        read_name_cyl = "%s.xlsx"%cyl_file_name
        df = pd.read_excel(read_name_cyl)  # excel
        names = df['学历'].value_counts().index.tolist()  # 学历
        x = range(len(names))  # 定义一个列表，用作X轴的位置
        y = df['学历'].value_counts().tolist()  # y轴数据
        plt.rcParams['font.sans-serif'] = ['simhei']  # 显示中文的设置
        fig = plt.figure(figsize=(12, 6))  # 定义一个画布
        axe = fig.add_subplot(1, 1, 1)  # 添加图表
        axe.bar(x, y, tick_label=names)  # 绘制柱状图
        for i in range(len(names)):
            axe.text(x[i] - 0.15, y[i] + 2, y[i])  # 显示柱状图柱子上的数字
        cyl_title_name = read_name_cyl +"学历要求柱状图"
        axe.set_title(cyl_title_name)  # 添加标题
        cyl_svg_name = read_name_cyl +'学历要求柱状图.svg'
        plt.savefig(cyl_svg_name)  # 保存


if __name__ == '__mian__':
    data_to_view()

