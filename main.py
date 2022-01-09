import psycopg2 as psycopg2
import xlrd
import re
from pprint import pprint
import random

conn = psycopg2.connect(host="localhost", database="schoolManage", user="postgres", password="root")
cursor = conn.cursor()
"""wb = xlrd.open_workbook("sinif_listeleri.xls")
sheet = wb.sheet_by_index(0)
for i in range(1,len(sheet.col_values(0))):
    # database.setdefault(sheet.cell_value(i,2), {})
    className = sheet.cell_value(i, 2)
    number = sheet.cell_value(i, 3)
    name = sheet.cell_value(i, 0)
    lastName = sheet.cell_value(i, 1)
    classNumber = re.search("[^\D]+",className).group()
    className = className.split("/ ")[1][0]
    classs = str(classNumber)+"/"+className"""

cursor.execute("""CREATE TEMPORARY TABLE selectedStudents(
	_number varchar,
	_class varchar,
	selected boolean default false
)""")
conn.commit()

db = {}

cursor.execute("""SELECT _number, _class from students where _class like '9%'""")
students = cursor.fetchall()
for i in students[:40]:
    cursor.execute(f"INSERT INTO selectedStudents VALUES('{i[0]}', '{i[1]}')")

conn.commit()

cursor.execute("""SELECT distinct(_class) from selectedStudents""")
classes = cursor.fetchall()
random.shuffle(classes)
try:
    while classes:
        _class = classes.pop()
        manage = []
        for i in range(4):
            temp = []
            for j in range(8):
                if i==0:
                    if j==0:
                        cursor.execute("""SELECT _number,_class FROM selectedStudents where selected = FALSE ORDER BY RANDOM() LIMIT 1""")
                        kisi, sinif = cursor.fetchone()
                        temp.append((kisi, sinif))
                        cursor.execute(f"UPDATE selectedStudents set selected = true where selectedStudents._class = '{kisi}'")
                        conn.commit()
                    else:
                        fark = temp[j-1][1]
                        cursor.execute(f"SELECT _number,_class FROM selectedStudents where selected = False and _class !=  '{fark}' ORDER BY RANDOM() LIMIT 1")
                        kisi, sinif = cursor.fetchone()
                        cursor.execute(f"UPDATE selectedStudents set selected = true where selectedStudents._class = '{kisi}'")
                        conn.commit()
                        temp.append((kisi, sinif))
                elif j==0:
                    fark = (manage[i - 1][j + 1][1], manage[i-1][j][1])
                    cursor.execute(
                        f"SELECT _number,_class FROM selectedStudents where selected = False and _class not in {fark} ORDER BY RANDOM() LIMIT 1")
                    kisi, sinif = cursor.fetchone()
                    cursor.execute(f"UPDATE selectedStudents set selected = true where selectedStudents._class = '{kisi}'")
                    conn.commit()
                    temp.append((kisi, sinif))

                else:
                    if j == 7:
                        fark = (manage[i - 1][j - 1][1], temp[j - 1][1], manage[i-1][j][1])
                        cursor.execute(
                            f"SELECT _number,_class FROM selectedStudents where selected = False and _class not in {fark} ORDER BY RANDOM() LIMIT 1")
                        kisi, sinif = cursor.fetchone()
                        cursor.execute(
                            f"UPDATE selectedStudents set selected = true where selectedStudents._class = '{kisi}'")
                        conn.commit()
                        temp.append((kisi, sinif))
                    else:
                        fark = (manage[i-1][j-1][1], manage[i-1][j+1][1], temp[j-1][1], manage[i-1][j][1])
                        cursor.execute(f"SELECT _number,_class FROM selectedStudents where selected = False and _class not in {fark} ORDER BY RANDOM() LIMIT 1")
                        kisi, sinif = cursor.fetchone()
                        cursor.execute(f"UPDATE selectedStudents set selected = true where selectedStudents._class = '{kisi}'")
                        conn.commit()
                        temp.append((kisi, sinif))
            manage.append(temp)

        db[_class] = manage
except:
    manage.append(temp)
    db[_class] = manage
for i in db:
    for j in db[i]:
        print(j)
    print("\n")


cursor.close()
conn.close()

