import os

from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.config.enums import SupportedPdfParseMethod
from .generator import Generator

def convert(pdf_path: str, output_path: str):
  pdf_file_name = os.path.basename(pdf_path)
  proto_name = pdf_file_name.split(".")[0]
  image_folder: str = "images"
  output_image_path = os.path.join(output_path, image_folder)
  image_writer = FileBasedDataWriter(output_image_path)
  md_writer = FileBasedDataWriter(output_path)
  reader1 = FileBasedDataReader("")
  pdf_bytes = reader1.read(pdf_path)  # read the pdf content
  ds = PymuDocDataset(pdf_bytes)

  if ds.classify() == SupportedPdfParseMethod.OCR:
    infer_result = ds.apply(doc_analyze, ocr=True)
    pipe_result = infer_result.pipe_ocr_mode(image_writer)

  else:
    infer_result = ds.apply(doc_analyze, ocr=False)
    pipe_result = infer_result.pipe_txt_mode(image_writer)

  return Generator(
    pipe_result, md_writer, 
    proto_name, output_path, image_folder,
  )