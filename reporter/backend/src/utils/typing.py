from typing import (
    List,
    Union,
)

from sqlalchemy.engine import Row
from sqlalchemy.sql import Subquery

QUERY_OR_SUBQUERY = Union[Subquery, List[Row]]
