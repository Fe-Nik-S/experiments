
from enum import Enum


class QueryTypes(Enum):
    SELECT = 0
    UPDATE = 1


class QueryBuilder(object):

    def select(self, table_name, fields):
        raise NotImplementedError()

    def where(self, field, value, operator="="):
        raise NotImplementedError()

    def limit(self, count=10, offset=0):
        raise NotImplementedError()

    @property
    def query(self):
        raise NotImplementedError()


class MySQLQueryBuilder(QueryBuilder):
    _query = None
    _type = None
    _where = []
    _limit = None

    def reset(self):
        self._query = None
        self._type = None
        self._where = []
        self._limit = None

    def select(self, table_name, fields):
        self.reset()
        self._query = "SELECT {} FROM {}".\
            format(", ".join(fields), table_name)
        self._type = QueryTypes.SELECT
        return self

    def where(self, field, value, operator="="):
        if self._type not in [QueryTypes.SELECT, QueryTypes.UPDATE]:
            raise Exception("WHERE can only be added to SELECT OR UPDATE")

        self._where += ["{} {} {}".format(field, operator, value)]
        return self

    def limit(self, count=10, offset=0):
        if self._type not in [QueryTypes.SELECT, QueryTypes.UPDATE]:
            raise Exception("LIMIT can only be added to SELECT OR UPDATE")

        self._limit = " LIMIT {}, {}".format(count, offset)
        return self

    @property
    def query(self):
        result = self._query
        if self._where:
            result += " WHERE {}".format(" AND ".join(self._where))
        if self._limit:
            result += self._limit
        result += ";"
        return result


class PostgreSQLBuilder(MySQLQueryBuilder):

    def limit(self, count=10, offset=0):
        if self._type not in [QueryTypes.SELECT, QueryTypes.UPDATE]:
            raise Exception("LIMIT can only be added to SELECT OR UPDATE")

        self._limit = " LIMIT {} OFFSET {}".format(count, offset)
        return self


class Director(object):
    __builder = None

    def set_builder(self, builder):
        self.__builder = builder

    def client_query(self):
        query = self.__builder.\
            select("employees", ["id, name, salary"]).\
            where("age", '20', ">").where("age", "40", "<").\
            limit("50").query
        return query


if __name__ == "__main__":
    director = Director()

    print("Testing MySql query builder:")
    director.set_builder(MySQLQueryBuilder())
    print(director.client_query())

    print("\nTesting PosgreSQL query builder:")
    director.set_builder(PostgreSQLBuilder())
    print(director.client_query())

### OUTPUT ###
# Testing MySql query builder:
# SELECT id, name, salary FROM employees WHERE age > 20 AND age < 40 LIMIT 50, 0;
#
# Testing PosgreSQL query builder:
# SELECT id, name, salary FROM employees WHERE age > 20 AND age < 40 LIMIT 50 OFFSET 0;
