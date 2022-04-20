from typing import List, Type

from .config import engine, MetaData
from .model import BaseDBModel
from .session_context import SessionContext


class SchemaLoader:
    type_aliases = {
        'VARCHAR': 'CHARACTER VARYING',
        'INT8': 'BIGINT',
        'SERIAL8': 'BIGSERIAL',
        'VARBIT': 'BIT VARYING',
        'BOOL': 'BOOLEAN',
        'CHAR': 'CHARACTER',
        'FLOAT8': 'DOUBLE PRECISION',
        'INT': 'INTEGER',
        'INT4': 'INTEGER',
        'DECIMAL': 'NUMERIC',
        'FLOAT4': 'REAL',
        'INT2': 'SMALLINT',
        'SERIAL2': 'SMALLSERIAL',
        'SERIAL4': 'SERIAL',
        'TIMETZ': 'TIME WITH TIME ZONE',
        'TIMESTAMPTZ': 'TIMESTAMP WITH TIME ZONE',
    }

    def __init__(self, model: Type[BaseDBModel]):
        self.model = model
        self.session = SessionContext

    def _get_pgsql_columns_by_table(self, table: str):
        with self.session() as session:
            return session.execute(
                '''
                select column_name, data_type
                from information_schema.columns
                where table_name = '{table}'
                and table_schema = 'public'
                '''.format(table=table)
            ).all()

    def _remove_columns(self, table: str, columns: List[List[str]]):
        drop_column_statements = ', '.join([f'DROP COLUMN {c}' for c, _ in columns])
        alter_table_statement = f'ALTER TABLE {table} {drop_column_statements};'
        with self.session() as session:
            session.execute(alter_table_statement)

    def _create_columns(self, table: str, columns: List[List[str]]):
        add_column_statements = ', '.join([f'ADD COLUMN {n} {c}' for n, c in columns])
        alter_table_statement = f'ALTER TABLE {table} {add_column_statements}'
        with self.session() as session:
            session.execute(alter_table_statement)

    def load(self):
        MetaData.create_all(bind=engine)
        table = self.model.__tablename__
        model_columns_map = self.model.get_columns()
        model_columns: List[List[str]] = \
            [[n, c.type.compile(dialect=engine.dialect)] for n, c in model_columns_map.items()]
        pgsql_columns: List[List[str]] = [[n, t.upper()] for n, t in self._get_pgsql_columns_by_table(table)]

        for i, (n, t) in enumerate(model_columns):
            if t in self.type_aliases:
                model_columns[i][1] = self.type_aliases[t]

        columns_to_remove = [c for c in pgsql_columns if c not in model_columns]
        columns_to_create = [c for c in model_columns if c not in pgsql_columns]

        if columns_to_remove:
            self._remove_columns(table, columns_to_remove)
        if columns_to_create:
            self._create_columns(table, columns_to_create)