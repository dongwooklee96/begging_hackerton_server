import io

from PIL import Image


async def binary_to_image(file):
    return Image.open(io.BytesIO(await file.read()))


def save_binary_to_file(binary_data, file_path):
    with open(file_path, "wb") as file:
        return file.write(binary_data)
