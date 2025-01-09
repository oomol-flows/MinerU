import os

from typing import Any
from threading import Lock


class Generator:
  def __init__(
      self, 
      pipe_result: Any, 
      md_writer: Any,
      proto_name: str,
      output_path: str,
      image_folder: str,
    ) -> None:

    self._proto_name: str = proto_name
    self._pipe_result: Any = pipe_result
    self._md_writer: Any = md_writer
    self._output_path: str = output_path
    self._image_folder: str = image_folder
    self._lock: Lock = Lock()

  def output_image_path(self, absolute_image_path: bool) -> str:
    if absolute_image_path:
      return os.path.join(self._output_path, self._image_folder)
    else:
      return os.path.join(".", self._image_folder)

  def draw_layout(self, name: str | None) -> str:
    output_path = self._to_output_path(name, "_layout.pdf")
    with self._lock:
      self._pipe_result.draw_layout(output_path)
    return output_path

  def draw_span(self, name: str | None) -> str:
    output_path = self._to_output_path(name, "_spans.pdf")
    with self._lock:
      self._pipe_result.draw_span(output_path)
    return output_path

  def dump_md(self, name: str | None, absolute_image_path: bool) -> str:
    output_path = self._to_output_path(name, ".md")
    with self._lock:
      self._pipe_result.dump_md(
        self._md_writer,
        output_path,
        self.output_image_path(absolute_image_path),
      )
    return output_path

  def dump_content_list(self, name: str | None, absolute_image_path: bool) -> str:
    output_path = self._to_output_path(name, "_content_json.json")
    with self._lock:
      self._pipe_result.dump_content_list(
        self._md_writer,
        output_path,
        self.output_image_path(absolute_image_path),
      )
    return output_path

  def _to_output_path(self, name: str | None, sufix: str) -> str:
    if name is None:
      name = f"{self._proto_name}{sufix}"
    return os.path.join(self._output_path, name)