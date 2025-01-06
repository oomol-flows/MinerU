import os
import requests
import zipfile
import tempfile
import shutil


def main():
  zip_url = "https://codeload.github.com/opendatalab/MinerU/zip/refs/tags/magic_pdf-0.10.6-released"
  zip_folder_name = "MinerU-magic_pdf-0.10.6-released"
  dist_path = "/tmp/mineru"

  with tempfile.TemporaryDirectory() as temp_dir:
    zip_path = os.path.join(temp_dir, "mineru.zip")
    with requests.get(zip_url, stream=True) as r:
      r.raise_for_status()
      with open(zip_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
          f.write(chunk)
      with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(temp_dir)

      shutil.move(
        src=os.path.join(temp_dir, zip_folder_name),
        dst=dist_path,
      )

if __name__ == "__main__":
  main()