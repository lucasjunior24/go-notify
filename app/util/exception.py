from dataclasses import dataclass


@dataclass
class ExceptionAPI(Exception):
  data: str | None = None
  message: str = "Error"
  status: str = "failed"
  status_code: str = 500



