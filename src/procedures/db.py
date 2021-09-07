import psycopg2
from configparser import ConfigParser
import traceback

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def raw(sql, vals = None, is_fetch = False):
    """ run raw sql query  """
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        # execute raw statement
        if vals and len(vals) > 0:
            cur.execute(sql, vals)
        else:
            cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        
        if is_fetch:
            result = cur.fetchall()
            return result
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
            
def create_table(name, columns):
    """ create table  """
    col_str = ", ".join(columns)
    sql = 'DROP TABLE IF EXISTS %s CASCADE; CREATE TABLE %s (%s);'%(name, name, col_str)
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        print("Table %s created" % (name,))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
            
def build_insert_sql(name, col_values):
    cols = ""
    s = ""
    vals = []
    ind = 0
    length = len(col_values.items())
    for key, value in col_values.items():
        cols += key
        vals.append(value)
        s += '%s'
        ind += 1
        if ind < length:
            cols += ", "
            s += ", " 
        
    sql = 'INSERT INTO ' + name + '(' + cols + ') VALUES(' + s + ') RETURNING id, ' + cols + ';'
    return (sql, tuple(vals))

def select(name, cols, condition = None, vals = None):
    """ select items from a table  """
    col_str = ", ".join(cols)
    sql = 'SELECT ' + col_str + ' FROM ' + name + ((' WHERE ' + condition + ';') if condition else ";")
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        # execute the SELECT statement
        if vals and len(vals) > 0:
            cur.execute(sql, vals)
        else:
            cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        result = cur.fetchall()
        # close communication with the database
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()
            
def insert(name, col_values = {}):
    """ insert item into a table  """
    sql, vals = build_insert_sql(name, col_values)
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, vals)
        # commit the changes to the database
        conn.commit()
        result = cur.fetchone()
        # close communication with the database
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()

def insert_list(name, cols = [], values = ()):
    """ insert multiple items into a table  """
    col_str = ", ".join(cols)
    col_count = len(cols)
    s = ""
    for n in range(col_count):
        s += '%s' + (', ' if n < col_count - 1 else '')
        
    sql = 'INSERT INTO ' + name + '(' + col_str + ') VALUES(' + s + ') RETURNING id, ' + col_str + ";"
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, values)
        # commit the changes to the database
        conn.commit()
        
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()

def build_update_sql(name, columns, conditions):
    key_vals = ""
    col_l = len(columns)
    for i in range(col_l):
        col = columns[i]
        key_vals += (col + " = %s")
        if i < col_l - 1:
            key_vals += ", "
            
    cond = (" WHERE " + conditions) if conditions else " "
        
    sql = 'UPDATE ' + name + ' SET ' + key_vals + cond + ' RETURNING *;'
    return sql
            
def update(name, cols = [], vals = (), conditions = None):
    """ update item into a table  """
    sql = build_update_sql(name, cols, conditions)
    conn = None
    try:
        conn = connect()
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, vals)
        # commit the changes to the database
        conn.commit()
        result = cur.fetchone()
        # close communication with the database
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print (sql)
        print(vals)
        print(error)
        traceback.print_exc()
    finally:
        if conn is not None:
            conn.close()