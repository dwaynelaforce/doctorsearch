class AppException(BaseException): ...

class QueryException(AppException): ...

class NotFoundError(QueryException): ...