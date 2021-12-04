import Adafruit_DHT
import sqlite3
import time
import os
from datetime import datetime

DB_FILE = 'guacamole.db'
DB_TABLE = 'temperature'
DHT_PIN = 'P8_10'
DHT_SENSOR = Adafruit_DHT.DHT11

class TempLogger:
    def __init__(self):
        self.db = sqlite3.connect(DB_FILE)
        self.__init_db()

    def __init_db(self):
        c = self.db.cursor()

        init_sql = "CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL, date TEXT)".format(DB_TABLE)

        c.execute(init_sql)

        self.db.commit()
        c.close()

    def read_temp(self):
        return Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    def read_all(self):
        c = self.db.cursor()

        statement = 'SELECT * FROM {} ORDER BY id'.format(DB_TABLE)

        for row in c.execute(statement):
            print(row)

        c.close()

    def write_to_db(self, temp):
        current_date = datetime.now().isoformat()
        statement = 'INSERT INTO {}(value,date) VALUES ({}, "{}")'.format(
                DB_TABLE, temp, current_date)

        print(statement)

        c = self.db.cursor()
        c.execute(statement)
        self.db.commit()
        c.close()

    def collect(self, iterations=5):
        for _ in range(0, iterations):
            min_val = 0
            max_val = 0
            sum_val = 0
            for i in range(0, 18):
                _, t = self.read_temp()
                print('read temp: {}'.format(t))

                if i == 0:
                    min_val, max_val = t, t

                if t < min_val:
                    min_val = t
                elif t > max_val:
                    max_val = t

                sum_val += t

            result = (sum_val - min_val - max_val) / 16

            print('writing {}'.format(result))
            self.write_to_db(result)

    def collect_uart(self, iterations=5):
        import Adafruit_BBIO.UART as UART
        import serial

        UART.setup("UART1")

        ser = serial.Serial(port="/dev/ttyO1", baudrate=9600)
        ser.close()
        ser.open()

        for _ in range(0, iterations):
            min_val = 0
            max_val = 0
            sum_val = 0

            result = float(ser.readline().decode().strip())
            print('writing {}'.format(result))
            self.write_to_db(result)

if __name__ == '__main__':
    t = TempLogger()

    if os.environ.get('SHOW') is not None:
        t.read_all()
    else:
        if os.environ.get('UART'):
            print('uart')
            t.collect_uart()
        else:
            t.collect()
        t.read_all()
