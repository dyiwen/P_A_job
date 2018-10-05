#!/usr/bin/env python
#-*-coding:utf-8 -*-

import DAL


def insert_info_mysql():


	msl = DAL.Mysql('host','port','user','pwd','databases')
	sql = 'select * from id_info;'
	rowcount,result = msl.execute(sql)
	print result
	msl.close()




insert_info_mysql()
