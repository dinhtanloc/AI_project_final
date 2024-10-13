import json
from IPython.display import Image, display
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain_core.messages import ToolMessage
from langgraph.graph.message import add_messages


class State(TypedDict):
    """Đại diện cho cấu trúc trạng thái chứa danh sách tin nhắn.

    Thuộc tính:
        messages (list): Danh sách các tin nhắn, mỗi tin nhắn có thể được xử lý
        bằng cách thêm tin nhắn sử dụng hàm `add_messages`.
    """
    messages: Annotated[list, add_messages]


class BasicToolNode:
    """Một nút thực hiện các công cụ được yêu cầu trong AIMessage cuối cùng.

    Lớp này lấy các cuộc gọi công cụ từ AIMessage gần đây nhất trong đầu vào
    và gọi công cụ tương ứng để tạo ra các phản hồi.

    Thuộc tính:
        tools_by_name (dict): Một từ điển ánh xạ tên công cụ đến các thể hiện công cụ.
    """

    def __init__(self, tools: list) -> None:
        """Khởi tạo BasicToolNode với các công cụ có sẵn.

        Tham số:
            tools (list): Danh sách các đối tượng công cụ, mỗi công cụ có thuộc tính `name`.
        """
        # self.tools_by_name = {tool.name: tool for tool in tools}
        self.tools_by_name = {'query_stock_sqldb', 'ocr_and_lookup', 'query_stock_logic', 'load_tavily_search_tool'}

    def __call__(self, inputs: dict):
        """Thực thi các công cụ dựa trên các cuộc gọi công cụ trong tin nhắn cuối cùng.

        Tham số:
            inputs (dict): Một từ điển chứa trạng thái đầu vào với các tin nhắn.

        Trả về:
            dict: Một từ điển với danh sách các đầu ra `ToolMessage`.

        Raises:
            ValueError: Nếu không tìm thấy tin nhắn nào trong đầu vào.
        """
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            print(self.tools_by_name[tool_call["name"]])
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}


def route_tools(
    state: State,
) -> Literal["tools", "__end__"]:
    """Xác định xem có chuyển đến ToolNode hay kết thúc luồng hay không.

    Hàm này được sử dụng trong conditional_edge và kiểm tra tin nhắn cuối cùng trong trạng thái cho các cuộc gọi công cụ. 
    Nếu có các cuộc gọi công cụ, nó sẽ chuyển đến nút 'tools'; nếu không thì sẽ chuyển đến kết thúc.

    Tham số:
        state (State): Trạng thái đầu vào chứa danh sách các tin nhắn.

    Trả về:
        Literal["tools", "__end__"]: Trả về 'tools' nếu có cuộc gọi công cụ;
        '__end__' nếu không có.

    Raises:
        ValueError: Nếu không tìm thấy tin nhắn nào trong trạng thái đầu vào.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(
            f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"


def plot_agent_schema(graph):
    """Vẽ sơ đồ tác nhân sử dụng một đối tượng đồ thị, nếu có thể.

    Cố gắng hiển thị một biểu diễn hình ảnh của sơ đồ đồ thị của tác nhân
    bằng định dạng Mermaid và khả năng hiển thị của IPython. Nếu các
    phụ thuộc cần thiết bị thiếu, nó sẽ bắt ngoại lệ và in ra một thông báo
    thay thế.

    Tham số:
        graph: Một đối tượng đồ thị có phương thức `get_graph`, trả về một cấu trúc đồ thị
        hỗ trợ việc tạo biểu đồ Mermaid.

    Trả về:
        None
    """
    try:
        display(Image(graph.get_graph().draw_mermaid_png()))
    except Exception:
        # This requires some extra dependencies and is optional
        return print("Graph could not be displayed.")
