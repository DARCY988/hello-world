"""
MySQL database manipulation class.
"""
from fii_ai_api.utils.utility import log
from DBUtils.PooledDB import PooledDB
import pymysql
import datetime
import pandas as pd
import numpy as np
import re


class BasicMySQL(object):
    def __init__(self, username='root', password='Genius', hostname='10.167.219.250', db_name='demo', **kwargs):
        # DB Login info
        self.username = username
        self.password = password
        self.db_name = db_name
        self.hostname = hostname

        # Restore BackEnd execution history log
        self.log = log

        # Create multi-thread services
        self.pool = PooledDB(
            creator=pymysql,
            mincached=0,
            maxcached=6,
            maxshared=3,
            # maxconnections=6,
            blocking=True,
            ping=0,
            maxusage=None,
            host=self.hostname,
            user=self.username,
            passwd=self.password,
            db=self.db_name,
            port=3306,
        )

    def manipulate_db(self, sql, dtype=dict, data_list=None, data_kw={}):
        ''' Could do CURD operations.
        Parameters
        --------------
        sql: str
            Your MySQL Querry.

        dtype: {list, dict, pandas.DataFrame}
            Set your return data type.

            * [Data Engineer]TODO: Could add new data type.

        data_list: list
            Enable ``PyMySQL`` function `executemany(operation, seq_of_params)`:
            This method prepares a database operation (query or command)
            and executes it against all parameter sequences or mappings
            found in the sequence `seq_of_params`.

            Note: `data_list` is equal to `seq_of_params`

            Example.
            ```
                data_list = [
                    ('Jane', date(2005, 2, 12)),
                    ('Joe', date(2006, 5, 23)),
                    ('John', date(2010, 10, 3)),
                ]

                sql = 'INSERT INTO employees (first_name, hire_date) VALUES (%s, %s)'
                self.manipulate_db(sql, data_list)
            ```

        data_kw: dict
            Execute sql with specify variables using %s or %(name)s parameter style.
            Example.
            ```
                sql = 'SELECT * FROM employees WHERE emp_no = %(emp_no)s'
                self.manipulate_db(sql, {'emp_no': 2})
            ```

        Return
        --------------
        CASE I. `cursor.fetchall()`: {list, dict, pandas.DataFrame}
            Only for `SELECT` Querry, read DB data

        CASE II. `db.commit()`: bool
            Executed the `UPDATE/INSERT/DELETE` Querry, Database doesn't save the change,
            need to commit the change from DB.
        '''
        db = None
        cursor = None
        dtype = dtype()

        try:
            # self.db = pymysql.connect(self.hostname, self.username, self.password, self.db_name)
            db = self.pool.connection()

            # Set data type
            if isinstance(dtype, pd.DataFrame):
                return pd.read_sql(sql, con=db)
            elif isinstance(dtype, dict):
                cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
            elif isinstance(dtype, list):
                cursor = db.cursor()

            if data_list:
                cursor.executemany(sql, data_list)
            elif data_kw:
                cursor.excute(sql, data_kw)
            else:
                cursor.execute(sql)
            if re.match('select|SELECT', sql.lstrip().split(' ')[0]) is not None:
                return cursor.fetchall()
            else:
                # select does not need commit(), only update/insert/delete need it
                db.commit()

        except Exception as e:
            self.log('[{}] meet error'.format(sql.strip()))
            self.log(e)
            if re.match('select|SELECT', sql.lstrip().split(' ')[0]) is None:
                # select does not need rollback
                db.rollback()
            return ()

        finally:
            if cursor:
                cursor.close()
            if db:
                db.close()

        return True


class MySQL(BasicMySQL):
    def __init__(self, debug=False, db_tables={}, **login_info):
        self._debug = True if debug == 'test/' else False
        super().__init__(**login_info)

        # Set mapping table to process.
        # `db_tables`: directly set the mapping tables(you can customize of your own table).
        # `debug` flag: Lazy flag to set this SQL class as debug mode or not.
        if db_tables:
            self.db_tables = db_tables
        elif self._debug is True:
            if 'test_table' not in login_info:
                raise KeyError(
                    "Your dictionary lacks key '%s\'. Please provide "
                    "it, because it is required to determine whether "
                    "string is singular or plural." % 'test_table'
                )
            else:
                self.db_tables = login_info['test_table']
        else:
            if 'prod_table' not in login_info:
                raise KeyError(
                    "Your dictionary lacks key '%s\'. Please provide "
                    "it, because it is required to determine whether "
                    "string is singular or plural." % 'prod_table'
                )
            else:
                self.db_tables = login_info['prod_table']

    @property
    def get_db_tables(self):
        '''Get DataBase working table'''
        return self.db_tables.copy()

    @property
    def _if_debug(self):
        '''Check if the api mode is in debug mode'''
        return self._debug
