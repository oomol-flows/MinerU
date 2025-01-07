import os
import platform
import json

from typing import Literal
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from oocana import Context

def main(params: dict, context: Context):
  if platform.machine() != "x86_64":
    raise Exception(f"This task only supports x86_64 architecture (your architecture is {platform.machine()})")

  pdf_path: str = params["pdf_path"]
  output_path: str | None = params["output_path"]

  if output_path is None:
    output_path = os.path.join(context.session_dir, f"MinerUConvert_{context.job_id}")

  _apply_config(params)
  _convert_pdf(pdf_path, output_path)

  return { "output_path": output_path }

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

def _convert_pdf(pdf_path: str, output_path: str):
  pdf_file_name = os.path.basename(pdf_path)
  name_without_suff = pdf_file_name.split(".")[0]
  output_image_path = os.path.join(output_path, "images")
  image_dir = str(os.path.basename(output_image_path))

  os.makedirs(output_image_path, exist_ok=True)

  image_writer, md_writer = FileBasedDataWriter(output_image_path), FileBasedDataWriter(
    output_path
  )
  image_dir = str(os.path.basename(output_image_path))
  reader1 = FileBasedDataReader("")
  pdf_bytes = reader1.read(pdf_path)  # read the pdf content

  ds = PymuDocDataset(pdf_bytes)

  if ds.classify() == SupportedPdfParseMethod.OCR:
    infer_result = ds.apply(doc_analyze, ocr=True)
    pipe_result = infer_result.pipe_ocr_mode(image_writer)

  else:
    infer_result = ds.apply(doc_analyze, ocr=False)
    pipe_result = infer_result.pipe_txt_mode(image_writer)

  infer_result.draw_model(os.path.join(output_path, f"{name_without_suff}_model.pdf"))
  pipe_result.draw_layout(os.path.join(output_path, f"{name_without_suff}_layout.pdf"))
  pipe_result.draw_span(os.path.join(output_path, f"{name_without_suff}_spans.pdf"))
  pipe_result.dump_md(md_writer, f"{name_without_suff}.md", image_dir)
  pipe_result.dump_content_list(md_writer, f"{name_without_suff}_content_list.json", image_dir)
