from typing import Callable, Optional, List, Any, Type

from sqlalchemy.engine import Engine

from pgsql_repository.model.model import BaseModel
from pgsql_repository.filtering import BaseFilterable
from pgsql_repository.extensions.pagination import Pageable, PagedResult
from pgsql_repository.core import Metadata
from pgsql_repository.repository.sessions import SessionBuilder
from pgsql_repository.repository.schema_loader import SchemaLoader


def session_wrapper(func: Callable):
    """
    Wraps a method of a BaseModelRepository type to inject its session as the first positional argument.
    :type func: object The function to wrap
    """
    ...


class BaseModelRepository:
    connection_string: str
    engine: Engine
    model: Type[BaseModel]
    metadata: Metadata
    session_builder: SessionBuilder
    schema_loader: SchemaLoader
    """
    Base repository containing default CRUD methods
    """

    def __init__(self, connection_string: str, model: Type[BaseModel], metadata: Optional[Metadata] = Metadata):
        """
        Initializes the repository
        :param connection_string: The connection string (i.e. postgresql://postgres:root@localhost:5432/postgres)
        """
        ...

    def _filter_select(self, stmt: Any, filterable: BaseFilterable):
        ...

    def _paginate_select(self, stmt: Any, pageable: Pageable):
        ...

    def get_by_id(self, id: int) -> BaseModel:
        ...
    
    def get_by_id_in_batch(self, ids: List[int]) -> List[BaseModel]:
        ...

    def get_all(self, pageable: Optional[Pageable] = None) -> List[BaseModel] | PagedResult[BaseModel]:
        ...

    def get_all_by_filter(self, filterable: BaseFilterable, pageable: Optional[Pageable] = None) -> List[BaseModel] | PagedResult[BaseModel]:
        ...

    def get_distinct_by_column(self, column_name: str) -> Any:
        ...

    def create(self, model: BaseModel) -> BaseModel:
        """
        Creates an instance of the model in the database
        :param model: The model to create
        :return: The model created
        """
        ...

    def create_in_batch(self, models: List[BaseModel]) -> None:
        ...

    def update(self, model: BaseModel) -> BaseModel:
        ...

    def update_in_batch(self, models: BaseModel) -> None:
        ...

    def delete(self, _id: int) -> None:
        ...

    def delete_in_batch(self, ids: List[int]) -> None:
        ...
