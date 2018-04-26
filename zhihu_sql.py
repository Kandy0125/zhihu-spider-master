# !/usr/bin/env python
# -*-coding:utf-8-*-
# 导入相关模块
import MySQLdb
import xlrd
def sql():
    book = xlrd.open_workbook("zhihu.xls")
    sheet = book.sheet_by_name("1")
    # 建立和mysql数据库的连接
    conn = MySQLdb.connect(host='localhost', user='root', passwd='160830', charset="utf8")
    # 获取游标
    curs = conn.cursor()
    # 选择连接哪个数据库
    conn.select_db('mydata')
    # 执行SQL,创建一个表
    curs.execute("create table zhihu(title varchar (1000),url varchar (1000),commitnum varchar (10000))")
    # 插入多条记录
    values = []
    for r in range(0, sheet.nrows):
        title = sheet.cell(r, 0).value
        url = sheet.cell(r, 1).value
        commitnum = sheet.cell(r, 2).value
        values.append((title, url, commitnum))
        print url
    curs.executemany("insert into zhihu values(%s,%s,%s)", values)
    # 提交修改
    conn.commit()
    # 关闭游标连接,释放资源
    curs.close()
    # 关闭连接
    conn.close()
sql()
