import eel
import sqlite3
import datetime

con = sqlite3.connect("sqlite.db")
cursor = con.cursor()

eel.init('static')

# Nomenclature
@eel.expose
def nomencl_output():
    resp = cursor.execute("""SELECT * FROM nomenclature""").fetchall()
    # titles = cursor.execute("""PRAGMA table_info('nomenclature') """).fetchall()
    data = {"titles": [["Id", "id", "none", "number"],
                       ["Article", "article", "6", "text"],
                       ["Name", "name", "50", "text"],
                       ["Type Of Names", "type_of_names", "none", "select"],
                       ["Used", "used", "none", "checkbox"],
                       ["Date Of Start", "date_of_start", "none", "date"],
                       ["Date Of Finish", "date_of_finish", "none", "date"]],
            "values": []}
    for i in resp:
        data["values"].append([*i])
    return data


@eel.expose
def nomencl_delete(id):
    cursor.execute("""DELETE FROM nomenclature WHERE id =?""", (id,))
    con.commit()

@eel.expose
def nomencl_append(data):
    cursor.execute("""INSERT INTO nomenclature VALUES (?, ?, ?, ?, ?, ?, ?)""", (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    con.commit()

@eel.expose
def nomencl_update(id, article, name, type_of_name, used):
    cursor.execute("""UPDATE nomenclature SET 
                    article=?, name=?, type_of_names=?,
                    used=?,date_of_start=?,date_of_finish=?
                    WHERE id=?""", (article, name, type_of_name, used, id))
    con.commit()


# Stations
@eel.expose
def stations_output():
    resp = cursor.execute("""SELECT * FROM stations""").fetchall()
    data = {"titles": [["Id", "id", "none", "number"],
                       ["Number", "number", "4", "text"],
                       ["Name", "name", "50", "text"],
                       ["Address", "address", "50", "text"],
                       ["Index", "index", '6', "number"],
                       ["Latitude", "latitude", "none", "text"],
                       ["Longitude", "longitude", "none", "text"]],
            "values": []}
    for i in resp:
        data["values"].append([*i])
    return data

@eel.expose
def stations_append(data):
    cursor.execute("""INSERT INTO stations VALUES (?, ?, ?, ?, ?, ?, ?)""", (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    con.commit()

@eel.expose
def stations_delete(id):
    cursor.execute("""DELETE FROM stations WHERE id =?""", (id,))
    con.commit()

@eel.expose
def satations_update(id, number, name, adress, index, width, longitude):
    cursor.execute("""UPDATE stations set
                   number=?, name=?, adress=?, index=?, 
                   width=?, longitude=? where id=?""",
                   (number, name, adress, index, width, longitude, id))
    con.commit()

# Users
@eel.expose
def users_output():
    resp = cursor.execute("""SELECT * FROM users""").fetchall()
    data = {"titles": [["Id", "id", "none", "number"],
                       ["Surname", "surname", "50", "text"],
                       ["Name", "name", "none", "text"],
                       ["Middle Name", "Middle Name", "none", "text"],
                       ["Telephone", "telephone", '18', "tel"],
                       ["E-mail", "latitude", "50", "text"],
                       ["Date of birth", "Date of birth", "none", "text"],
                       ["Status", "Status", "none", "select"]],
            "values": []}
    for i in resp:
        data["values"].append([*i])
    return data

@eel.expose
def users_append(data):
    cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
    con.commit()

@eel.expose
def users_delete(id):
    cursor.execute("""DELETE FROM users WHERE id =?""", (id,))
    con.commit()

@eel.expose
def users_update(data):
    cursor.execute("""UPDATE users set
                   surname=?, name=?, middle_name=?, telephone=?,
                   e-mail=?, date_of_birth=?, status=? where id=?""",
                   (data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[0]))
    con.commit()


# Price
@eel.expose
def prices_output():
    resp = cursor.execute("""SELECT * FROM prices""").fetchall()
    data = {"titles": [["Id", "id", "none", "number"],
                       ["Last Change", "Last Change", "none", "hidden"],
                       ["Type Of Names", "Type Of Names", "none", "select"],
                       ["Price", "Price", "none", "number"]],
            "values": []}
    for i in resp:
        data["values"].append([*i])
    return data

@eel.expose
def prices_delete(id):
    cursor.execute("""DELETE FROM prices WHERE id =?""", (id,))
    con.commit()

@eel.expose
def prices_append(data):
    cursor.execute("""INSERT INTO prices
                        values (?, ?, ?, ?)""",
                   (data[0], str(datetime.date.today().strftime('%d-%m-%Y')), data[1], data[2]))
    con.commit()

@eel.expose
def change_of_price(type_of_names, new_price):
    last_price = cursor.execute("""SELECT last_change FROM prices where type_of_names = ?""", (type_of_names,)).fetchone()
    print(last_price[0])
    if last_price[0].split("-")[0] == datetime.date.today().day and last_price[0].split("-")[1] == datetime.date.today().month and last_price[0].split("-")[2] == datetime.date.today().year:
        cursor.execute("""INSERT INTO story_of_changes(date_of_change, type_of_names, price)
                        values (?, ?, ?)""",
                    (str(datetime.date.today().strftime('%d-%m-%Y')), type_of_names, new_price))
        cursor.execute("""UPDATE prices set last_change=?, price=? where type_of_names=?""",
                    (str(datetime.date.today().strftime('%d-%m-%Y')), new_price, type_of_names))
        con.commit()
    else:
        eel.alert_prices()


# Statuses
@eel.expose
def statuses_output():
    resp = cursor.execute("""SELECT * FROM statuses""").fetchall()
    return resp

# Type of names
@eel.expose
def names_for_change():  # выпадающий список для изменения цены
    res = cursor.execute("""SELECT type_of_names FROM nomenclature""").fetchall()
    data = []
    for i in res:
        data.append(i[0])
    return data

# End Expl
@eel.expose
def end_expl(id):
    cursor.execute("""UPDATE nomenclature set used = 'No',
                    date_of_finish = ? where id = ?""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), id))
    cursor.execute("""INSERT INTO end_of_exploitation(date, product)
                        VALUES(?, ?)""",
                   (str(datetime.date.today().strftime('%d-%m-%Y')), id))

# Story Output
@eel.expose
def changes_output():
    resp = cursor.execute("""SELECT * FROM story_of_changes""").fetchall()
    data = {"titles": [["Id", "id", "none", "none"],
                       ["Date Of Change", "Date Of Change", "none", "none"],
                       ["Type Of Names", "Type Of Names", "none", "none"],
                       ["Price", "Price", "none", "none"]],
            "values": []}
    for i in resp:
        data["values"].append([*i])
    return data


# Payment
@eel.expose
def users_list(): # выпадающий список для оплаты
    users = cursor.execute("""SELECT id from users""").fetchall()
    data = []
    for i in users:
        data.append(i[0])
    return data

@eel.expose
def products_list(): # выпадающий список для оплаты
    products = cursor.execute("""SELECT article from nomenclature""").fetchall()
    data = []
    for i in products:
        data.append(i[0])
    return data

@eel.expose
def payment(user, article, date_of_start): # User ID, 
    sale = cursor.execute("""SELECT sale from statuses where name =( SELECT status from users where id = ?)""",
                          (user,)).fetchone()
    price_per_min = cursor.execute("""SELECT prices.price FROM prices
                            where type_of_names=
                            (SELECT type_of_names FROM nomenclature where article = ?)""",
                                   (article,)).fetchone()
    time = int((datetime.datetime.now() - datetime.datetime.strptime(date_of_start, "%H:%M %d:%m:%Y")).total_seconds() / 60)
    return int((1-(sale[0]/100))*(time * price_per_min[0]))


eel.start('index.html', port=8000, mode="default")