import json
import os
import sqlite3
import tkinter
from tkinter import filedialog

###SQLite to Json copy from : https://github.com/Austyns/sqlite-to-json-python

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# connect to the SQlite databases
def openConnection(pathToSqliteDb):
    connection = sqlite3.connect(pathToSqliteDb)
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    return connection, cursor


def getAllRecordsInTable(table_name, pathToSqliteDb):
    conn, curs = openConnection(pathToSqliteDb)
    conn.row_factory = dict_factory
    curs.execute("SELECT * FROM {} ".format(table_name))
    # fetchall as result
    results = curs.fetchall()
    # close connection
    conn.close()
    return json.dumps(results)


def sqliteToJson(pathToSqliteDb):
    connection, cursor = openConnection(pathToSqliteDb)
    # select all the tables from the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    # for each of the tables , select all the records from the table
    for table_name in tables:
        # Get the records in table
        results = getAllRecordsInTable(table_name['name'], pathToSqliteDb)

        # generate and save JSON files with the table name for each of the database tables and save in results folder
        with open(table_name['name']+'.json', 'w') as the_file:
            the_file.write(results)
    # close connection
    connection.close()

###

root = tkinter.Tk()
root.withdraw()

print("Please select the 'meta' file.")
print("By default, the file path is ", end = "")
print("%userprofile%\\AppData\\LocalLow\\Cygames\\umamusume\\meta")
meta = filedialog.askopenfilename()
sqliteToJson(meta)
print("File read successfully, start parsing...")

with open('a.json', 'r') as f:
    data = f.read()


json_data = json.loads(data)
print("Please select the 'dat' folder.")
print("By default, the folder path is ", end = "")
print("%userprofile%\\AppData\\LocalLow\\Cygames\\umamusume\\dat")
root = filedialog.askdirectory()
if not os.path.exists('manifest'):
    os.mkdir('manifest')

with open('nothing.txt', 'w') as no:

    for i in json_data:
        print(i['n'])
        raw_path = i['h']
        path_head = raw_path[0:2]
        path = root + '/' + path_head + '/' + raw_path
        road = i['n']
        if os.path.exists(path):
            with open(path, 'rb') as f:
                f_data = f.read()
            if road.startswith('//'):
                with open('manifest/'+road[2:], 'wb') as f:
                    f.write(f_data)
            elif '/' not in road:
                with open('manifest/'+road, 'wb') as f:
                    f.write(f_data)
            else:
                #print(road)
                temp = road.rsplit('/', 1)
                if not os.path.exists(temp[0]):
                    os.makedirs(temp[0])
                with open(road, 'wb') as f:
                    f.write(f_data)        
        else:
            print(i['n'])
            no.write(str(i)+'\n')

print("Completed.")
input()
