import MySQLdb as md
import tushare as ts
import pandas as pd



def get_tushare_data(code, start_date, end_date):
    return ts.get_h_data(code, start = start_date, end = end_date, autype=None)


def open_db(user,passwd,dbname):
    cxn = md.connect(db=dbname, user=user, passwd=passwd)
    return cxn



def save_to_sql(conn, tablename, df):
    df.to_sql(con=conn, name=tablename, if_exists='replace', flavor='mysql')



def read_sql(conn,tablename):
    sql = 'select * from {}'.format(tablename)
    return pd.read_sql(sql,conn)



if __name__ == "__main__":
    conn = open_db('root','root','ts_db')
    #save_to_sql(conn,'ts_table',get_tushare_data('601601','2010-03-10','2016-03-10'))
    print read_sql(conn,'ts_table')
