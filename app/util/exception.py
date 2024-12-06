from pydantic import BaseModel


class ExceptionAPI(Exception):
  data: str | None = None
  message: str
  status = "failed"