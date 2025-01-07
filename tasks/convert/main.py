import os
import platform
import json

from typing import Literal
from oocana import Context
from shared.converter import convert

def main(params: dict, context: Context):
  if platform.machine() != "x86_64":
    raise Exception(f"This task only supports x86_64 architecture (your architecture is {platform.machine()})")

  pdf_path: str = params["pdf_path"]
  output_path: str | None = params["output_path"]

  if output_path is None:
    output_path = os.path.join(context.session_dir, f"MinerUConvert_{context.job_id}")

  os.makedirs(output_path, exist_ok=True)
  _apply_config(params)

  return { "generator": convert(pdf_path, output_path) }

def _apply_config(params: dict):
  template_path: str = params["config_path"]
  device: Literal["cpu", "cuda"] = params["device"]

  with open(template_path, "r", encoding="utf-8") as file:
    config_json: dict = json.load(file)
    config_json["device-mode"] = device

  config_path: str = os.path.join(os.path.expanduser("~"), "magic-pdf.json")
  config_path = os.path.abspath(config_path)

  with open(config_path, "w", encoding="utf-8") as file:
    json.dump(config_json, file, ensure_ascii=False, indent=2)