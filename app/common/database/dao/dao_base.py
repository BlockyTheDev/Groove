# coding:utf-8
from typing import List

from common.singleton import Singleton
from PyQt5.QtSql import QSqlDatabase, QSqlRecord

from ..entity import Entity
from .sql_query import SqlQuery


class DaoBase:
    """ 数据库访问操作抽象类 """

    table = ''
    fields = ['id']

    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.query = SqlQuery(db) if db else SqlQuery()
        self.query.setForwardOnly(True)

    def createTable(self):
        """ 创建表格 """
        raise NotImplementedError

    def selectBy(self, **condition) -> Entity:
        """ 查询一条符合条件的记录

        Parameters
        ----------
        condition: dict
            查询条件

        Returns
        -------
        entity: Entity
            实体类对象，没有查询到则为 None
        """
        self._prepareSelectBy(condition)

        if not (self.query.exec() and self.query.first()):
            return None

        return self.loadFromRecord(self.query.record())

    def listBy(self, **condition) -> List[Entity]:
        """ 查询所有符合条件的记录

        Parameters
        ----------
        condition: dict
            查询条件

        Returns
        -------
        entities: List[Entity]
            实体类对象列表，没有查询到则为空列表
        """
        self._prepareSelectBy(condition)

        if not self.query.exec():
            return []

        return self.iterRecords()

    def _prepareSelectBy(self, condition: dict):
        """ 通过条件预编译查询指令

        Parameters
        ----------
        table: str
            表名

        condition: dict
            查询条件
        """
        if not condition:
            raise ValueError("必须传入至少一个条件")

        placeholders = [f'{k} = ?' for k in condition.keys()]
        sql = f"SELECT * FROM {self.table} WHERE {' AND '.join(placeholders)}"
        self.query.prepare(sql)
        for v in condition.values():
            self.query.addBindValue(v)

    def listAll(self) -> List[Entity]:
        """ 查询所有记录 """
        sql = f"SELECT * from {self.table}"
        if not self.query.exec(sql):
            return []

        return self.iterRecords()

    def listByIds(self, ids: list) -> List[Entity]:
        """ 查询所有在主键列表中的记录 """
        if not ids:
            return []

        placeHolders = ','.join(['?']*len(ids))
        sql = f"SELECT * FROM {self.table} WHERE {self.fields[0]} IN ({placeHolders})"
        self.query.prepare(sql)

        for id in ids:
            self.query.addBindValue(id)

        if not self.query.exec():
            return []

        return self.iterRecords()

    def iterRecords(self) -> List[Entity]:
        """ 迭代所有查询到的记录 """
        entities = []

        while self.query.next():
            entity = self.loadFromRecord(self.query.record())
            entities.append(entity)

        return entities

    def update(self, id, field: str, value) -> bool:
        """ 更新一条记录中某个字段的值

        Parameters
        ----------
        id:
            主键值

        filed: str
            字段名

        value:
            字段值

        Returns
        -------
        success: bool
            更新是否成功
        """
        sql = f"UPDATE {self.table} SET {field} = ? WHERE {self.fields[0]} = ?"
        self.query.prepare(sql)
        self.query.addBindValue(value)
        self.query.addBindValue(id)
        return self.query.exec()

    def updateById(self, entity: Entity) -> bool:
        """ 更新一条记录

        Parameters
        ----------
        entity: Entity
            实体类对象

        Returns
        -------
        success: bool
            更新是否成功
        """
        if len(self.fields) <= 1:
            return False

        id_ = self.fields[0]
        values = ','.join([f'{i} = :{i}' for i in self.fields[1:]])
        sql = f"UPDATE {self.table} SET {values} WHERE {id_} = :{id_}"

        self.query.prepare(sql)
        self.bindEntityToQuery(entity)

        return self.query.exec()

    def updateByIds(self, entities: List[Entity]) -> bool:
        """ 更新多条记录

        Parameters
        ----------
        entities: List[Entity]
            实体类对象

        Returns
        -------
        success: bool
            更新是否成功
        """
        if not entities:
            return True

        if len(self.fields) <= 1:
            return False

        QSqlDatabase.database().transaction()

        id_ = self.fields[0]
        values = ','.join([f'{i} = :{i}' for i in self.fields[1:]])
        sql = f"UPDATE {self.table} SET {values} WHERE {id_} = :{id_}"

        self.query.prepare(sql)

        for entity in entities:
            self.bindEntityToQuery(entity)
            self.query.exec()

        success = QSqlDatabase.database().commit()
        return success

    def insert(self, entity: Entity) -> bool:
        """ 插入一条记录

        Parameters
        ----------
        entity: Entity
            实体类对象

        Returns
        -------
        success: bool
            更新是否成功
        """
        values = ','.join([f':{i}' for i in self.fields])
        sql = f"INSERT INTO {self.table} VALUES ({values})"
        self.query.prepare(sql)
        self.bindEntityToQuery(entity)
        return self.query.exec()

    def insertBatch(self, entities: List[Entity]) -> bool:
        """ 插入多条记录

        Parameters
        ----------
        entities: List[Entity]
            实体类对象列表

        Returns
        -------
        success: bool
            更新是否成功
        """
        if not entities:
            return True

        QSqlDatabase.database().transaction()

        values = ','.join([f':{i}' for i in self.fields])
        sql = f"INSERT INTO {self.table} VALUES ({values})"
        self.query.prepare(sql)

        for entity in entities:
            self.bindEntityToQuery(entity)
            self.query.exec()

        success = QSqlDatabase.database().commit()
        return success

    def deleteById(self, id) -> bool:
        """ 移除一条记录

        Parameters
        ----------
        id:
            主键值

        Returns
        -------
        success: bool
            更新是否成功
        """
        sql = f"DELETE FROM {self.table} WHERE {self.fields[0]} = ?"
        self.query.prepare(sql)
        self.query.addBindValue(id)
        return self.query.exec()

    def deleteByIds(self, ids: list) -> bool:
        """ 移除多条记录

        Parameters
        ----------
        ids: list
            主键值列表

        Returns
        -------
        success: bool
            移除是否成功
        """
        if not ids:
            return True

        placeHolders = ','.join(['?']*len(ids))
        sql = f"DELETE FROM {self.table} WHERE {self.fields[0]} IN ({placeHolders})"
        self.query.prepare(sql)

        for id in ids:
            self.query.addBindValue(id)

        return self.query.exec()

    def clearTable(self):
        """ 清空表格数据 """
        return self.query.exec(f"DELETE FROM {self.table}")

    @staticmethod
    def loadFromRecord(record: QSqlRecord) -> Entity:
        """ 根据一条记录创建一个实体类对象

        Parameters
        ----------
        record: QSqlRecord
            记录

        Returns
        -------
        entity: Entity
            实体类对象
        """
        raise NotImplementedError

    def adjustText(self, text: str):
        """ 处理字符串中的单引号问题 """
        return text.replace("'", "''")

    def bindEntityToQuery(self, entity: Entity):
        """ 将实体类的值绑定到 query 对象上 """
        for field in self.fields:
            value = entity[field]
            self.query.bindValue(f':{field}', value)

    def setDatabase(self, db: QSqlDatabase):
        """ 使用指定的数据库 """
        self.query = SqlQuery(db)
        self.query.setForwardOnly(True)