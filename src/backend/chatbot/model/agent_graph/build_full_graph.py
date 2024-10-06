from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
from langchain_openai import ChatOpenAI
# from agent_graph.tool_chinook_sqlagent import query_chinook_sqldb
from model.tools.tool_finance_knowledge import query_stock_logic
from model.tools.tool_rag_pdf import lookup_user_document
from model.tools.tool_tavily_search import load_tavily_search_tool
from model.tools.tool_sqlagent import query_stock_sqldb
from model.tools.load_tools_config import LoadToolsConfig
from agent_graph.agent_backend import State, BasicToolNode, route_tools, plot_agent_schema

TOOLS_CFG = LoadToolsConfig()


def build_graph():
    """
    Xây dựng một đồ thị quyết định của tác nhân bằng cách kết hợp một Mô hình Ngôn ngữ Lớn (LLM) với các công cụ khác nhau và xác định luồng tương tác giữa chúng.

    Hàm này thiết lập một đồ thị trạng thái nơi mà một mô hình ngôn ngữ chính (LLM) tương tác
    với một số công cụ được định nghĩa trước (ví dụ: cơ sở dữ liệu, chức năng tìm kiếm, tra cứu chính sách, v.v.).
    Tác nhân có thể gọi các công cụ dựa trên các điều kiện và sử dụng đầu ra của chúng để thông báo
    các quyết định tiếp theo. Luồng bao gồm việc gọi công cụ có điều kiện, quay lại
    với chatbot sau khi thực hiện công cụ để hướng dẫn bước tiếp theo.

    Các bước:
    1. Khởi tạo mô hình ngôn ngữ chính (LLM) với chức năng liên kết công cụ.
    2. Định nghĩa các nút trong đồ thị, nơi mỗi nút đại diện cho một hành động cụ thể:
    - Nút chatbot: Thực thi LLM với trạng thái và tin nhắn đã cho.
    - Nút công cụ: Chạy các lệnh gọi công cụ dựa trên tin nhắn cuối cùng trong trạng thái đầu vào.
    3. Thực hiện định tuyến có điều kiện giữa chatbot và các công cụ:
    - Nếu cần một công cụ, nó sẽ định tuyến đến nút công cụ.
    - Nếu không, luồng sẽ kết thúc.
    4. Thiết lập các kết nối giữa chatbot và các nút công cụ để tạo thành vòng lặp của tác nhân.
    5. Sử dụng cơ chế tiết kiệm bộ nhớ để theo dõi và lưu các điểm kiểm tra trong đồ thị.

    Trả về:
        graph (StateGraph): Đồ thị trạng thái đã biên dịch đại diện cho quá trình ra quyết định
        của tác nhân, tích hợp chatbot, công cụ và định tuyến có điều kiện.

    Các thành phần:
        - `primary_llm`: Mô hình ngôn ngữ chính chịu trách nhiệm tạo ra các phản hồi.
        - `tools`: Danh sách các công cụ bao gồm truy vấn SQL, chức năng tìm kiếm, tra cứu chính sách, v.v.
        - `tool_node`: Một nút chịu trách nhiệm xử lý việc thực hiện công cụ dựa trên yêu cầu của chatbot.
        - `chatbot`: Một hàm nhận trạng thái làm đầu vào và trả về một thông điệp được tạo ra bởi LLM.
        - `route_tools`: Một hàm có điều kiện để xác định xem chatbot có nên gọi một công cụ hay không.
        - `graph`: Đồ thị hoàn chỉnh với các nút và các cạnh có điều kiện.
    """
    primary_llm = ChatOpenAI(model=TOOLS_CFG.primary_agent_llm,
                             temperature=TOOLS_CFG.primary_agent_llm_temperature)
    graph_builder = StateGraph(State)
    # Load tools with their proper configs
    search_tool = load_tavily_search_tool(TOOLS_CFG.tavily_search_max_results)
    tools = [search_tool,
            lookup_user_document,
            query_stock_logic,
            load_tavily_search_tool
             ]
    # Tell the LLM which tools it can call
    primary_llm_with_tools = primary_llm.bind_tools(tools)

    def chatbot(state: State):
        """Executes the primary language model with tools bound and returns the generated message."""
        return {"messages": [primary_llm_with_tools.invoke(state["messages"])]}

    graph_builder.add_node("chatbot", chatbot)
    tool_node = BasicToolNode(
        tools=[
            search_tool,
            lookup_user_document,
            query_stock_logic,
            load_tavily_search_tool
            # query_chinook_sqldb
        ])
    graph_builder.add_node("tools", tool_node)
    # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "__end__" if
    # it is fine directly responding. This conditional routing defines the main agent loop.
    graph_builder.add_conditional_edges(
        "chatbot",
        route_tools,
        # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
        # It defaults to the identity function, but if you
        # want to use a node named something else apart from "tools",
        # You can update the value of the dictionary to something else
        # e.g., "tools": "my_tools"
        {"tools": "tools", "__end__": "__end__"},
    )

    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    memory = MemorySaver()
    graph = graph_builder.compile(checkpointer=memory)
    plot_agent_schema(graph)
    return graph
