import sqlite3
import pandas as pd


conn = sqlite3.connect('auto.db')
cursor = conn.cursor()




def csv2sql(filePath):
	df = pd.read_csv(filePath, encoding='utf-8', header=None, 
		names=['title', 'price', 'descr', 'transmission', 'body_type', 'drive_type', 'color', 'year', 'mileage' ])

	df.to_sql('auto_00', con = conn, if_exists='replace')


def createAuto():

	cursor.execute('''
		create table if not exists auto(
			id integer primary key autoincrement,
			auto_key varchar(128),
			title varchar(128),
			price varchar(128),
			descr varchar(128),
			transmission varchar(128),
			body_type varchar(128),
			drive_type varchar(128),
			color varchar(128),
			year varchar(128),
			mileage varchar(128),
			start_dttm datetime default current_timestamp,
			end_dttm datetime default (datetime('2999-12-31 23:59:59'))
		);
	''')



def readAndClearData():
	csv2sql('result.csv')
	cursor.execute('''
		drop table if exists auto_01;
		''')


	cursor.execute('''
		create table if not exists auto_01 as 
			select 
				substr(descr, 1, instr(descr, '/')-1) as engine_capacity,
				substr(substr(descr, instr(descr, '/')+1), 
					   1, 
					   instr(substr(descr, instr(descr, '/')+1), '/')-1
					   ) as power,

				substr(substr(descr, instr(descr, '/')+1), 
					   instr(substr(descr, instr(descr, '/')+1), '/')+1
					   ) as engine_type,
				title, 
				price, 
				transmission, 
				body_type, 
				drive_type, 
				color, 
				year, 
				mileage 

			from (
				select
					title, 
					price, 
					transmission, 
					body_type, 
					drive_type, 
					color, 
					year, 
					mileage ,
					replace(descr ,'\u2009/\u2009', '/')  as descr
				from auto_00
			) t1;
		''')


def createTableNewRows():
	cursor.execute('''
		create table newRows as 
		select 
			t1.*
		from auto_00 t1
		left join auto t2
		on t1.key = t2.key
		where t2.key is null
	''')

def createTableUpdateRows():
	cursor.execute('''
		create table updateRows as 
		select 
			t1.*
		from auto_01 t1
		iner join auto t2
		on t1.key = t2.key
		and (
			   t1.title        <> t2.title
			or t1.price        <> t2.price
			or t1.descr        <> t2.descr
			or t1.transmission <> t2.transmission
			or t1.body_type    <> t2.body_type
			or t1.drive_type   <> t2.drive_type
			or t1.color        <> t2.color
			or t1.year         <> t2.year
			or t1.mileage      <> t2.mileage
		) ;
	''')

def createTableDeleteRows():
	cursor.execute('''
		create table deleteRows as 
		select 
			t1.*
		from auto t1
		left join auto_01 t2
		on t1.key = t2.key
		where t2.key is null
		) ;
	''')




createAuto()
