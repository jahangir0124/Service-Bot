
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import sqlite3


#Add user to db
def createUser(data):
    conn = sqlite3.connect('baza.db')
    userId = data.id
    fname = data.first_name
    uname = data.username
    cursor = conn.cursor()
    sql = f"select * from Users where user_id = '{userId}'"
    user = cursor.execute(sql).fetchall()
    if not user:
        sql = f"INSERT INTO Users (user_id, username, first_name) VALUES ('{userId}', '{uname}', '{fname}')"
        cursor.execute(sql)
        
    



#Create Category Buttons
def createCatBtn():
    conn = sqlite3.connect('baza.db')
    catBtn = ReplyKeyboardBuilder()
    cursor = conn.cursor()
    categories = cursor.execute("SELECT name FROM Category").fetchall()
    for i in categories:
        for j in i:
            catBtn.add(KeyboardButton(text=j))
    catBtn.adjust(2)
    return catBtn

#Create service buttons
def createServcieBtn(text):
    conn = sqlite3.connect('baza.db')
    serBtn = ReplyKeyboardBuilder()
    cursor = conn.cursor()
    catId = cursor.execute(f"select id from Category where name='{text}'").fetchall()[0][0]
    sql = f"select name from Services where cat_id='{catId}'"
    services = cursor.execute(sql).fetchall()
    if services:
        for i in services:
            for j in i:
                serBtn.add(KeyboardButton(text=j))
                
        serBtn.adjust(2)
        return serBtn
        
    else:
        return False
            

        
    


            
            

   
