import os

from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from oocana import Context

def main(params: dict, context: Context):
  config_path: str = params["config_path"]
  pdf_path: str = params["pdf_path"]
  pdf_file_name = os.path.basename(pdf_path)
  name_without_suff = pdf_file_name.split(".")[0]

  # prepare env
  local_md_dir = context.session_dir
  local_image_dir = os.path.join(local_md_dir, "images")
  image_dir = str(os.path.basename(local_image_dir))

  os.makedirs(local_image_dir, exist_ok=True)

  image_writer, md_writer = FileBasedDataWriter(local_image_dir), FileBasedDataWriter(
      local_md_dir
  )
  image_dir = str(os.path.basename(local_image_dir))

  # read bytes
  reader1 = FileBasedDataReader("")
  pdf_bytes = reader1.read(pdf_path)  # read the pdf content

  # proc
  ## Create Dataset Instance
  ds = PymuDocDataset(pdf_bytes)

  ## inference
  if ds.classify() == SupportedPdfParseMethod.OCR:
      infer_result = ds.apply(doc_analyze, ocr=True)

      ## pipeline
      pipe_result = infer_result.pipe_ocr_mode(image_writer)

  else:
      infer_result = ds.apply(doc_analyze, ocr=False)

      ## pipeline
      pipe_result = infer_result.pipe_txt_mode(image_writer)

  ### draw model result on each page
  infer_result.draw_model(os.path.join(local_md_dir, f"{name_without_suff}_model.pdf"))

  ### draw layout result on each page
  pipe_result.draw_layout(os.path.join(local_md_dir, f"{name_without_suff}_layout.pdf"))

  ### draw spans result on each page
  pipe_result.draw_span(os.path.join(local_md_dir, f"{name_without_suff}_spans.pdf"))

  ### dump markdown
  pipe_result.dump_md(md_writer, f"{name_without_suff}.md", image_dir)

  ### dump content list
  pipe_result.dump_content_list(md_writer, f"{name_without_suff}_content_list.json", image_dir)
