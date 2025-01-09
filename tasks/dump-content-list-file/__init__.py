from shared.converter import Generator

def main(params: dict):
  generator: Generator = params["generator"]
  name: str | None = params["name"]
  absolute_image_path: bool = params["absolute_image_path"]
  file_path: str = generator.dump_content_list(name, absolute_image_path)

  return { 
    "file_path": file_path,
    "images_path": generator.output_image_path(absolute_image_path),
  }