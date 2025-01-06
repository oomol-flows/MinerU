import subprocess
import shutil

from oocana import Context

def main(params: dict, context: Context):
  config_path: str = params["config_path"]
  pdf_path: str = params["pdf_path"]
  command = ["magic-pdf", "-p", pdf_path, "-o", context.session_dir, "-m", "auto"]
  
  shutil.copy(config_path, "/root/magic-pdf.json")
  result = subprocess.run(
    command, 
    shell=True, 
    capture_output=True, 
    text=True,
  )
  print(result.stdout)
  print(result.stderr)
  print(context.session_dir)
