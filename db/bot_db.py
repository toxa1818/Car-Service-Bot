import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('auto_service.db')
    cur = base.cursor()
    if base:
        print('Data base connected!')
    base.execute('CREATE TABLE IF NOT EXISTS services(name TEXT PRIMARY KEY, price TEXT, duration TEXT)')


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO services VALUES(?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for service in cur.execute('SELECT * FROM services').fetchall():
        await bot.send_message(message.from_user.id, f"{service[0]}\nPrice: {service[1]}\nDuration: {service[2]}")


async def sql_read2():
    return cur.execute('SELECT * FROM services').fetchall()


async def sql_delete(data):
    cur.execute('DELETE FROM services WHERE name == ?', (data,))
    base.commit()
        