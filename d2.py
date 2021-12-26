import sqlite3
import datetime
import math
con = sqlite3.connect("sqlite.db")
cursor = con.cursor()


# справочники

# номенклатура


def nomencl_delete(id):
    cursor.execute("""DELETE FROM nomenclature WHERE id =?""", (id,))
    con.commit()


def nomencl_update(id, article, name, type_of_name, used):
    cursor.execute("""UPDATE nomenclature SET 
                    article=?, name=?, type_of_names=?,
                    used=?,date_of_start=?,date_of_finish=?
                    WHERE id=?""", (article, name, type_of_name, used, id))
    con.commit()



# Оплата
def for_payment(): # выпадающий список для оплаты
    users = cursor.execute("""SELECT name from users""").fetchall()
    products = cursor.execute("""SELECT name from nomenclature""").fetchall()
    return users, products

def products_list(): # выпадающий список для оплаты
    products = cursor.execute("""SELECT name, article from nomenclature""").fetchall()
    print(products)
    data = []
    for i in products:
        data.append(i[0])
    return data

def payment(user, date_of_start, article): # User ID, 
    sale = cursor.execute("""SELECT sale from statuses where name =( SELECT status from users where id = ?)""",
                          (user,)).fetchone()
    price_per_min = cursor.execute("""SELECT prices.price FROM prices
                            where type_of_names=
                            (SELECT type_of_names FROM nomenclature where article = ?)""",
                                   (article,)).fetchone()
    time = int((datetime.datetime.now() - datetime.datetime.strptime(date_of_start, "%H:%M %d:%m:%Y")).total_seconds() / 60)
    return int((1-(sale[0]/100))*(time * price_per_min[0]))

# прайс по тарифам
def price_output():
    resp = cursor.execute("""SELECT * FROM prices""").fetchall()
    return resp


def changes_output():
    resp = cursor.execute("""SELECT * FROM story_of_changes""").fetchall()
    return resp


def price_delete(id):
    cursor.execute("""DELETE FROM prices WHERE id =?""", (id,))
    con.commit()
    price_output()


def nomens_for_2_table():  # это данные для выпадающего списка
    resp = cursor.execute("""SELECT nomenclature.type_of_names from nomenclature 
                            left join prices on 
                            prices.type_of_names = nomenclature.type_of_names
                            where prices.type_of_names is null""").fetchall()
    return resp


def price_append(type_of_names, price):
    cursor.execute("""INSERT INTO prices (last_change, type_of_names, price)
                        values (?, ?, ?)""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), type_of_names, price))
    con.commit()
    return price_output()


# станции
def stations_output():
    resp = cursor.execute("""SELECT * FROM stations""").fetchall()
    return resp


def stations_append(number, name, adress, index, width, longitude):
    cursor.execute("""INSERT into stations 
                    (number, name, adress, index, width, longitude)
                    values (?,?,?,?,?,?)""",
                   (number, name, adress, index, width, longitude))
    con.commit()
    return stations_output()


def stations_delete(id):
    cursor.execute("""DELETE FROM stations WHERE id =?""", (id,))
    con.commit()
    stations_output()


def satations_update(id, number, name, adress, index, width, longitude):
    cursor.execute("""UPDATE stations set
                   number=?, name=?, adress=?, index=?, 
                   width=?, longitude=? where id=?""",
                   (number, name, adress, index, width, longitude, id))
    con.commit()
    return stations_output()


# функции


#введение в эксплуатацию
def start_expl(article, name, type_of_name):
    date = str(datetime.date.today().strftime('%d-%m-%Y'))
    cursor.execute("""Insert into nomenclature(article, 
    name, type_of_names, used, date_of_start) values(?,?,?,?,?)""",
                   (article, name, type_of_name, 1, date))
    resp = cursor.execute("""SELECT * FROM nomenclature ORDER BY id DESC LIMIT 1""").fetchone()
    con.commit()
    return date, resp, article, name, type_of_name


#окончание эксплуатации
def names_for_end():  # выпадающий список для окончания эксплуатации
    res = cursor.execute("""SELECT name from nomenclature where used = Yes""").fetchall()
    return res


def end_expl(product):
    cursor.execute("""UPDATE nomenclature set used = 0,
                    date_of_finish = ? where name = ?""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), product))
    cursor.execute("""INSERT INTO end_of_exploitation(date, product)
                        VALUES(?, ?)""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), product))
    res = cursor.execute("""SELECT * FROM end_of_exploitation""").fetchall()
    return res


#Изменение цен
def names_for_change():  # выпадающий список для изменения цены
    res = cursor.execute("""SELECT type_of_names FROM nomenclature""").fetchall()
    return res


def change_of_price(type_of_names, new_price):
    last_price = cursor.execute("""SELECT price FROM prices
     where type_of_names = ?""", (type_of_names)).fetchall()
    cursor.execute("""INSERT into story_of_changes(date, type_of_names, price, new_price)
                    values (?, ?, ?, ?)""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), type_of_names, last_price, new_price))
    cursor.execute("""UPDATE prices set last_change=?, price=? where type_of_names=?""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), new_price, type_of_names))
    con.commit()


def payment(user, article, date_of_start): # User ID, 
    sale = cursor.execute("""SELECT sale from statuses where name =( SELECT status from users where id = ?)""",
                          (user,)).fetchone()
    price_per_min = cursor.execute("""SELECT prices.price FROM prices
                            where type_of_names=
                            (SELECT type_of_names FROM nomenclature where article = ?)""",
                                   (article[0],)).fetchone()
    print(price_per_min)
    time = int((datetime.datetime.now() - datetime.datetime.strptime(date_of_start, "%H:%M %d:%m:%Y")).total_seconds() / 60)
    return int((1-(sale[0]/100))*(time * price_per_min[0]))