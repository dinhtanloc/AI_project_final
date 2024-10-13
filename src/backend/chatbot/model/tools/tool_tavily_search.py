from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

# def load_tavily_search_tool(tavily_search_max_results: int):
#     """
#     Hàm này khởi tạo công cụ tìm kiếm Tavily, công cụ thực hiện các tìm kiếm và trả về kết quả
#     dựa trên các truy vấn của người dùng. Tham số `max_results` điều khiển số lượng kết quả tìm kiếm 
#     được trả về cho mỗi truy vấn.

#     Tham số:
#     tavily_search_max_results (int): Số lượng kết quả tìm kiếm tối đa được trả về cho mỗi truy vấn.

#     Trả về:
#     TavilySearchResults: Một thể hiện đã được cấu hình của công cụ tìm kiếm Tavily với `max_results` được chỉ định.
#     """
#     return TavilySearchResults(max_results=tavily_search_max_results)

class CustomTavilySearchTool(TavilySearchResults):
    """
    CustomTavilySearchTool là một lớp mở rộng từ lớp TavilySearchResults trong thư viện langchain_community.
    
    Lớp này được thiết kế để thực hiện các truy vấn tìm kiếm dựa trên các vector embeddings từ mô hình Tavily. 
    Nó cho phép truy xuất số lượng kết quả tìm kiếm tối đa dựa trên truy vấn người dùng, với khả năng cấu hình 
    thêm một thuộc tính `name` để mô tả và nhận dạng công cụ tìm kiếm này. 
    
    Các thuộc tính:
    ---------------
    name (str): Tên của công cụ tìm kiếm (mặc định là "Tavily Search Tool").
                Thuộc tính này cho phép bạn nhận dạng và mô tả công cụ trong hệ thống.
    
    max_results (int): Số lượng kết quả tìm kiếm tối đa mà công cụ sẽ trả về cho mỗi truy vấn tìm kiếm.
                       Giá trị này được truyền vào khi khởi tạo lớp và được sử dụng để giới hạn kết quả trả về.

    Phương thức:
    ---------------
    __init__(max_results: int, name: str = "Tavily Search Tool"):
        Khởi tạo một thể hiện của lớp CustomTavilySearchTool với số lượng kết quả tìm kiếm tối đa `max_results` 
        và tên `name` để nhận dạng công cụ.

        Tham số:
        ---------
        max_results (int): Số lượng kết quả tối đa sẽ được trả về từ mỗi truy vấn.
                           Đây là một tham số bắt buộc và được truyền vào khi khởi tạo lớp.
        
        name (str, tùy chọn): Tên của công cụ tìm kiếm. Mặc định là "Tavily Search Tool". 
                              Bạn có thể truyền một tên khác nếu muốn nhận diện công cụ với tên khác.
        
        Ví dụ:
        ---------
        >>> tool = CustomTavilySearchTool(max_results=10, name="Custom Search Tool")
        >>> print(tool.name)
        Custom Search Tool
    """
    def __init__(self, max_results: int):
        super().__init__(max_results=max_results)
        self.name = "Tavily_Search_Tool"  # Đặt tên cho công cụ

# @tool
def load_tavily_search_tool(tavily_search_max_results: int):
    """
    Hàm này tạo và trả về một thể hiện của công cụ tìm kiếm Tavily tùy chỉnh, với số lượng kết quả tối đa 
    được cấu hình bởi tham số `tavily_search_max_results`. Hàm này sử dụng lớp `CustomTavilySearchTool`, 
    một lớp mở rộng từ TavilySearchResults, để thực hiện các truy vấn tìm kiếm và trả về các kết quả phù hợp.

    Tham số:
    ---------------
    tavily_search_max_results (int): Số lượng kết quả tìm kiếm tối đa mà công cụ sẽ trả về cho mỗi truy vấn.
                                     Đây là giá trị để cấu hình số lượng kết quả trả về khi thực hiện tìm kiếm.

    Trả về:
    ---------------
    CustomTavilySearchTool: Trả về một thể hiện của lớp `CustomTavilySearchTool`, đã được cấu hình với giá trị 
                            `max_results` là `tavily_search_max_results`. Thể hiện này có thể được sử dụng để thực hiện 
                            các truy vấn tìm kiếm thông qua mô hình Tavily và nhận về số kết quả tìm kiếm phù hợp 
                            nhất theo truy vấn.

    Ví dụ:
    ---------------
    >>> search_tool = load_tavily_search_tool(tavily_search_max_results=5)
    >>> print(search_tool.name)
    Tavily Search Tool

    Trong ví dụ này, hàm `load_tavily_search_tool` khởi tạo một thể hiện của `CustomTavilySearchTool` với số lượng kết quả 
    tìm kiếm tối đa là 5, và tên mặc định là "Tavily Search Tool". Sau đó, chúng ta in ra tên của công cụ tìm kiếm để xác nhận.
    """
    return CustomTavilySearchTool(max_results=tavily_search_max_results)

#python -m doctest -v tenfile

print(load_tavily_search_tool(tavily_search_max_results=2).name)