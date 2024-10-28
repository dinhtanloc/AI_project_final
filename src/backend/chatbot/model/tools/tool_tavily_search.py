from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults

# @tool('load_tavily_search_tool')
def load_tavily_search_tool(tavily_search_max_results: int):
    """
    Hàm này khởi tạo công cụ tìm kiếm Tavily, công cụ thực hiện các tìm kiếm và trả về kết quả
    dựa trên các truy vấn của người dùng. Tham số `max_results` điều khiển số lượng kết quả tìm kiếm 
    được trả về cho mỗi truy vấn. Chỉ sử dụng công cụ này nếu chatbot không tìm thấy câu trả lời từ cơ sở dữ liệu, tài liệu được lưu trữ hay đào tạo trước đó

    Tham số:
    tavily_search_max_results (int): Số lượng kết quả tìm kiếm tối đa được trả về cho mỗi truy vấn.

    Trả về:
    TavilySearchResults: Một thể hiện đã được cấu hình của công cụ tìm kiếm Tavily với `max_results` được chỉ định.
    """
    return TavilySearchResults(max_results=tavily_search_max_results)



#python -m doctest -v tenfile

