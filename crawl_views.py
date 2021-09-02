import tkinter as tk
from tkinter import *
import crawl_ZL
import data_views

class TK_Scrapy(object):
    def __init__(self):
        pass

    #将str中的'K'字符去除，将str转换为float
    def data_finally(self,Scrapy_start):
        str_salary_list = []    # 接收纯数字的字符串列表['10','15',...]
        str_toInt_list = []     # 将字符串转换为浮点型数值
        avg_count = 0           # 计数器，用于统计个数,注意结果再除2，智联薪资为区间
        salary_count = 0        # 统计薪资总和
        for str_salist in Scrapy_start:
            # 去除字符'K'（大写）
            str_empty = str_salist.split('K')  # ['10',''],['15','']
            # 取出列表中的非空字符
            for delete_empty in str_empty:
                if delete_empty != '':
                    str_salary_list.append(delete_empty)
        # 字符串转为浮点型
        for str_toInt in str_salary_list:
            toInt = float(str_toInt)
            # print(type(toInt), toInt)
            str_toInt_list.append(toInt)
            # print(type(str_toInt_list), str_toInt_list)

        max_salary = max(str_toInt_list) * 1000
        min_salary = min(str_toInt_list) * 1000
        # 获取平均值
        for now_salary in str_toInt_list:
            salary_count += now_salary
            avg_count += 1
        avg_salary = (salary_count / avg_count) * 1000
        # 保留2为小数
        avg_salary_round = round(avg_salary, 2)
        finally_salary = [max_salary, min_salary,avg_salary_round]
        return finally_salary


    #主函数，生成图形界面
    def TK_mian(self):
        #定义画布名称及大小
        window = tk.Tk()
        window.title('智联招聘爬虫')
        window.geometry('700x500')
        #定义画布背景信息
        canvans = tk.Canvas(window,height=500,width=700)
        image_file = tk.PhotoImage(file='爬虫_gif.gif')
        image = canvans.create_image(0,0,anchor='nw',image=image_file)
        canvans.pack()
        #文本框设置
        tk.Label(window,text="关键字：").place(x=50,y=150)
        tk.Label(window,text='页数：').place(x=50,y=190)
        #设置默认值
        var_kwords = tk.StringVar()
        var_kwords.set('python')
        var_pumber = tk.StringVar()
        var_pumber.set('1')
        #设置输入框
        entry_kwords = tk.Entry(window,textvariable=var_kwords)
        entry_kwords.place(x=160,y=150)
        entry_pnumber = tk.Entry(window,textvariable=var_pumber)
        entry_pnumber.place(x=160,y=190)


        # 与爬虫.py数据交互
        def usr_selection():
            print('按下开始')
            selection_kwords = var_kwords.get()
            selection_pnumber = var_pumber.get()
            #检查输入框文本内容是否导入成功
            selection_list=[selection_kwords,selection_pnumber]
            # 调用爬虫.py
            print('开始爬虫')
            Scrapy_start_1 = crawl_ZL.Spider(selection_list) #启动爬虫.py并返回工资列表
            Scrapy_start = Scrapy_start_1.run_1()
            print('爬虫结束')
            print(type(Scrapy_start),Scrapy_start)
            # 设置文本框，默认值为爬虫程序return的结果,并以列表接收return的结果，
            # salary_list = ['10000', '4000', '7000']
            # #不调用函数做测试
            salary_list = self.data_finally(Scrapy_start)
            tk.Label(window, text="最高薪资：").place(x=50, y=230)
            tk.Label(window, text='最低薪资：').place(x=50, y=270)
            tk.Label(window, text='平均薪资：').place(x=50, y=310)
            # 定义字符
            var_max_salary = tk.StringVar()
            var_min_salary = tk.StringVar()
            var_avg_salary = tk.StringVar()
            # 设置默认值
            var_max_salary.set(salary_list[0])
            var_min_salary.set(salary_list[1])
            var_avg_salary.set(salary_list[2])
            # 设置文本框位置
            entry_max_salary = tk.Entry(window, textvariable=var_max_salary)
            entry_max_salary.place(x=160, y=230)
            entry_min_salary = tk.Entry(window, textvariable=var_min_salary)
            entry_min_salary.place(x=160, y=270)
            entry_avg_salary = tk.Entry(window, textvariable=var_avg_salary)
            entry_avg_salary.place(x=160, y=310)
        #定义查询按钮的位置以及按下时调用的函数
        btn_selection = tk.Button(window, text="查询", command=usr_selection)
        btn_selection.place(x=400, y=150)


        def views_database():
            print('开始生成视图')
            xlsx_name = var_kwords.get()
            data_views_start = data_views.data_to_view(xlsx_name)

        #查询按钮的位置及对应的函数调用
        btn_selection = tk.Button(window, text="生成可视化图", command=views_database)
        btn_selection.place(x=400, y=190)

        window.mainloop()


if __name__ == '__main__':
    Tserver = TK_Scrapy()
    Tserver.TK_mian()


