import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame,Series
import json
import time
import Against_Reptilia_solve

url="https://fe-api.zhaopin.com/c/i/sou"
params={   #参数
    'start': '90',
    'pageSize': '90',
    'cityId': '489',
    'workExperience': '-1',
    'education': '-1',
    'companyType': '-1',
    'employmentType': '-1',
    'jobWelfareTag': '-1',
    'kw': 'python',
    'kt': '3',
}

#https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=489&salary=0,0
# &workExperience=-1&education=-1&companyType=-1&employmentType=-1&
# jobWelfareTag=-1&kw=%E7%88%AC%E8%99%AB%E5%B7%A5%E7%A8%8B%E5%B8%88&kt=3
# &=0&_v=0.92900097&x-zp-page-request-id=72c651aaaeee49bcbf84dfe62e889dbc-1555569844583-403134

headers_choice = Against_Reptilia_solve.get_user_agent()
headers={ #头部信息
    'User-Agent':headers_choice
}
url1="https://jobs.zhaopin.com/%s.htm"


class Spider():
    def __init__(self,selection_list):
        self.word=selection_list[0]
        self.page=selection_list[1]
        #self.word='python'
        #page=2
        params['kw']=self.word   #更改请求的关键词
        self.df=DataFrame()   #创建一个DataFrame对象
        self.columns=['职位名称','工资','更新时间','地点','公司名称','需求人数','学历','工作经验','职责']   #列名
        for i in range(0,int(self.page)*90,90):
            print(i)
            params['start']=i   #更改开始页的页数
            try:
                self.r=requests.get(url,params=params,headers=headers,timeout=10)   #请求数据，加上try except防止请求失败程序停止
                # 使用代理IP
                #user_proxy = get_proxy()
                #res = requests.get(url,headers=headers,proxies=get_proxy)
            except:
                continue
            self.r.encoding='utf-8'  #更改编码格式
            time.sleep(0.5) #设置延迟防止IP被封
            print(time.time()) #显示当前时间，估测程序进度

    #启动爬虫
    def run_1(self):
        #print('run_1执行',self.r.text)
        return self.get_data(self.r.text)  #调用函数，函数是爬去数据，上面的所有都是用来请求的，这个函数才是解析请求返回来的数据的

    #薪资处理函数
    def salary_solve(self,salary):
        now_salary_list = []
        if '薪资面议' in salary:
            pass  # 对面薪资面议的情况忽略
        else:
            #去掉'-'，剩下k，['1k','2k']
            salary_heng = salary.split('-')
            for salary_k in salary_heng:
                #去掉'k'
                salary_fin = salary_k.split('k')
                #当前列表为['1','k']
                now_salary_list.append(salary_fin[0])
        return now_salary_list
            
    def get_data(self,text):
        js=json.loads(text)
        print(js)
        #薪资存储列表
        salary_list = []
        for i in js['data']['results']:
            idd=i['number']     #id
            title=i['jobName']  #职位名称
            #print(title)
            salary=i['salary']  #工资
            print(salary)
            #获得薪资后调用薪资存储处理函数
            every_avg_salary=self.salary_solve(salary)
            for sl in every_avg_salary:
                if sl != '-':
                    salary_list.append(sl)  #当前结果为str，['1','2',..]
            # print(salary_list)
            updateDate=i['updateDate']  #更新时间
            place=i['city']['display']   #工作地点
            company=i['company']['name']   #公司名称
            recruitCount=i['recruitCount']   #需求人数
            eduLevel=i['eduLevel']['name']   #学历
            workingExp=i['workingExp']['name']   #工作经验
            u1=url1%idd   #更改详情页的url，
            #获取二级子界面
            zhize=self.get_zhize(u1)  #调用这个函数是为了爬取详情页页面的职责的
            data=[title,salary,updateDate,place,company,recruitCount,eduLevel,workingExp,zhize]  #所有的字段都整理成一个列表
            self.df=self.df.append(Series(data,index=self.columns),ignore_index=True)   #添加进入dataframe的数据结构中
            #打印以验证代码
            # print(title)
            self.df.to_excel("%s.xlsx" % self.word)#保存数据
        # print(type(salary_list))
        return salary_list

            
    def get_zhize(self,link):
        try:
            r=requests.get(link,headers=headers,timeout=10)  #请求详情页
        except:
            return "暂无"
        r.encoding='utf-8'   #更改编码
        soup=BeautifulSoup(r.text,'lxml')  #解析数据
        # with open('soup_test.html','w') as f:
        #     f.write('soup')
        # print(soup)
        text=soup.select('div.describtion__detail-content')[0].text.strip()   #职责
        return text
    
    
    
if __name__=="__main__":
    Spider()
