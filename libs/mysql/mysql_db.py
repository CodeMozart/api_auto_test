# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
import logging


class MySQLBase:
    error_msg = ''
    """mysql 基础操作封装"""

    def __init__(self, host='localhost', user='wanplus', password='', database='', port=3306, charset=None):
        """init mysql connect"""
        try:
            self.__conn = mysql.connector.connect(host=host, user=user, password=password, database=database, port=port)
            self.__cursor = self.__conn.cursor()
            if charset:
                if len(charset) > 1:
                    self.__conn.set_charset_collation(charset[0], charset[1])
                else:
                    self.__conn.set_charset_collation(charset[0])
        except mysql.connector.Error as err:
            self.error_msg = "MySQL error, msg: {}".format(err)

    def ready(self):
        return hasattr(self, '_MySQLBase__cursor')

    def fetch_more(self, table='', fields='*', where='', order='', limit=0, size=0):
        """
        查询sql语句
        table - 表名
        fields - 查询的字段，默认 * 或 fields,name,...
        where - 查询条件语句
        order - 排序
        limit - 条数
        Returns 多条记录.
        """
        sql = self.build_sql(table, fields, where, order, limit, size)
        result = self.query(fields, sql)

        # print result
        if type(result) is int:
            self.error_msg = "MySQL error, fetch_more is fail, sql:%s" % sql
            return -100
        return result

    def fetch_one(self, table='', fields='', where='', order=''):
        """
        获取单行记录
        data - 查询的字段，默认 * 或 id,name,email,...
        table - 表名
        where - 查询条件语句
        order - 排序
        Returns 单独记录 or None.
        """
        sql = self.build_sql(table, fields, where, order, 1)
        result = self.query(fields, sql)
        if type(result) is int:
            self.error_msg = "MySQL error, fetch_one is fail, sql:%s" % sql
            return -101
        return result[0] if result else None

    def count(self, table, where):
        """根据条件统计行数"""
        sql = self.build_sql(table, 'COUNT(*)', where, '', 1)
        if not self.__execute(sql):
            self.error_msg = "MySQL error, count is fail, sql:%s" % sql
            return -102
        result = self.__cursor.fetchone()
        return result[0] if result else 0

    def insert(self, table, data):
        """
        新增一条数据
        data - 数据集合 {field:value...}
        table - 表名
        Returns insert__id
        """
        fields = ','.join(data.keys())  # 字符
        inputs = ','.join(("%s", ) * len(data))  # 参数
        values = tuple(data.values())  # value
        sql = "INSERT INTO %s (%s) VALUES (" % (table, fields) + inputs + ")"
        if not self.__execute(sql, values):
            self.error_msg = "insert, msg:%s" % self.error_msg
            return -103
        insert__id = self.__cursor.lastrowid
        self.__conn.commit()
        return insert__id

    def multi_insert(self, table, data):
        """
        新增多条数据
        data - 数据列表 [{field:value...}...]
        table - 表名
        Returns rowcount 影响到行数
        """
        fields = ','.join(data[0].keys())
        inputs = ','.join(("%s", ) * len(data[0]))
        values = []
        [values.append(tuple(item.values())) for item in data]

        sql = "INSERT INTO %s (%s) VALUES (" % (table, fields) + inputs + ")"
        self.__cursor.executemany(sql, values)
        self.__conn.commit()
        return self.__cursor.rowcount

    def update(self, table, data, where):
        """
        修改数据
        data - 数据集合 {field:value...}
        table - 表名
        where - 条件
        Returns rowcount 影响到行数
        """
        fields = (",".join(map(lambda k: k + "=%s", data.keys())))
        values = tuple(data.values())
        sql = "UPDATE %s SET " % table + fields + " WHERE " + where
        if not self.__execute(sql, values):
            self.error_msg = "MySQL error, execute is fail, sql:" + sql
            return -105
        self.__conn.commit()
        return self.__cursor.rowcount

    def delete(self, table, where):
        """
        删除记录
        :param table: 表名
        :param where: 条件
        :return: 影响行数
        """
        where = ' WHERE ' + where if where else ''
        sql = 'DELETE FROM ' + table + where
        if not self.__execute(sql):
            self.error_msg = "MySQL error, execute is fail,sql:" + sql
            return -106
        self.__conn.commit()
        return self.__cursor.rowcount


    def close(self):
        """关闭游标和连接"""
        if not hasattr(self, '_MySQLBase__cursor'):
            self.error_msg = "MySQL error, __cursor is None"
            return -100
        self.__cursor.close()
        self.__conn.close()

    @staticmethod
    def build_sql(table='', fields='', where='', order='', limit=0, size=0):
        """构造sql语句"""
        where = ' WHERE ' + where if where else ''
        limit = ' LIMIT ' + str(limit) if limit else ''
        limit += ',' + str(size) if limit and size else (' LIMIT ' + str(size) if size else '')
        order = ' ORDER BY ' + order if order else ''
        fields = fields if fields else '*'
        sql = 'SELECT ' + fields + ' FROM ' + table + where + order + limit

        return sql

    def query(self, fields, sql):
        """执行sql并返回结果集"""
        if type(self.__execute(sql)) == int:
            self.error_msg = "MySQL error, execute is fail, sql:" + sql
            return -109
        result = []
        column_names = self.__cursor.column_names if not fields or fields == '*' else tuple(fields.split(','))
        [result.append(dict(zip(column_names, item))) for item in self.__cursor]

        return result

    def __execute(self, sql, values=None):
        """执行sql并返回结果集"""
        try:
            if not hasattr(self, '_MySQLBase__cursor'):
                return -110

            if values:
                self.__cursor.execute(sql, values)
            else:
                self.__cursor.execute(sql)
            return True
        except mysql.connector.Error as err:
            self.error_msg = "MySQL __execute error, msg: {}, sql: {}".format(err, sql)
            logging.error(self.error_msg)
            return err.errno  # error number

    def get_error_msg(self):
        return self.error_msg
