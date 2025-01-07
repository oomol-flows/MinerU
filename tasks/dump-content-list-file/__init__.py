from shared.converter import Generator

def main(params: dict):
  generator: Generator = params["generator"]
  name: str | None = params["name"]
  file_path: str = generator.dump_content_list(name)

  return { 
    "file_path": file_path,
    "images_path": generator.output_image_path,
  }