import os
from pyprojroot import here


def create_directory(directory_path: str) -> None:
    """
    Tạo một thư mục nếu nó chưa tồn tại.

    Tham số:
        directory_path (str): Đường dẫn của thư mục sẽ được tạo.

    Ví dụ:
    ```python
    create_directory("/path/to/new/directory")
    ```

    """
    if not os.path.exists(here(directory_path)):
        os.makedirs(here(directory_path))
