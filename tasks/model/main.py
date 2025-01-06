# copy & update from https://raw.githubusercontent.com/opendatalab/MinerU/master/scripts/download_models_hf.py
import json
import os
import requests

from oocana import Context
from huggingface_hub import snapshot_download


def get_dir_path(params: dict) -> str:
  dir_path: str | None = params["dir_path"]
  if dir_path is not None and \
    (not os.path.exists(dir_path) or not os.path.isdir(dir_path)):
    dir_path = None
  if dir_path is None:
    dir_path = os.path.abspath("~/.cache/huggingface")
  return dir_path

def download_json(url):
  # 下载JSON文件
  response = requests.get(url)
  response.raise_for_status()  # 检查请求是否成功
  return response.json()

def download_and_modify_json(url, local_filename, modifications):
  if os.path.exists(local_filename):
    data = json.load(open(local_filename))
    config_version = data.get("config_version", "0.0.0")
    if config_version < "1.0.0":
      data = download_json(url)
  else:
    data = download_json(url)

  # 修改内容
  for key, value in modifications.items():
    data[key] = value

  # 保存修改后的内容
  with open(local_filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

def main(params: dict, context: Context):
  dir_path = get_dir_path(params)
  config_file = os.path.join(dir_path, "magic-pdf.json")

  if os.path.exists(config_file):
    return { "config_path": config_file }

  mineru_patterns = [
    "models/Layout/LayoutLMv3/*",
    "models/Layout/YOLO/*",
    "models/MFD/YOLO/*",
    "models/MFR/unimernet_small/*",
    "models/TabRec/TableMaster/*",
    "models/TabRec/StructEqTable/*",
  ]
  model_dir = snapshot_download(
    repo_id="opendatalab/PDF-Extract-Kit-1.0",
    cache_dir=dir_path,
    allow_patterns=mineru_patterns,
  )
  layoutreader_pattern = [
    "*.json",
    "*.safetensors",
  ]
  layoutreader_model_dir = snapshot_download(
    repo_id="hantian/layoutreader",
    cache_dir=dir_path,
    allow_patterns=layoutreader_pattern,
  )
  model_dir = model_dir + "/models"
  print(f"model_dir is: {model_dir}")
  print(f"layoutreader_model_dir is: {layoutreader_model_dir}")

  json_url = "https://github.com/opendatalab/MinerU/raw/master/magic-pdf.template.json"

  json_mods = {
    "models-dir": model_dir,
    "layoutreader-model-dir": layoutreader_model_dir,
  }
  download_and_modify_json(json_url, config_file, json_mods)
  print(f"The configuration file has been configured successfully, the path is: {config_file}")

  return { "config_path": config_file }
