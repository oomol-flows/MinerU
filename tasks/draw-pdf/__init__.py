from typing import Literal
from shared.converter import Generator

def main(params: dict):
  generator: Generator = params["generator"]
  name: str | None = params["name"]
  kind: Literal["layout", "span"] = params["kind"]

  if kind == "layout":
    file_path = generator.draw_layout(name)
  elif kind == "span":
    file_path = generator.draw_span(name)
  else:
    raise ValueError("Invalid kind. Expected 'layout' or 'span'")

  return { "file_path": file_path }