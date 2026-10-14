"""MCP SERVER minh hoạ — công bố tool `get_weather` qua giao thức MCP.

Khác với function calling: tool nằm ở một server ĐỘC LẬP. Server tự "khai
báo" tool của mình; bất kỳ MCP client nào (Claude Code, Claude Desktop,
Cursor, hoặc weather_client.py) cũng cắm vào dùng được mà không cần biết
code bên trong.

Schema của tool được TỰ ĐỘNG sinh ra từ type hints + docstring.

Chạy trực tiếp:
    pip install -r ../requirements.txt
    python weather_server.py

Đăng ký với Claude Code (làm 1 lần, dùng mãi):
    claude mcp add weather -- python /đường/dẫn/tới/weather_server.py
"""

from datetime import date, timedelta

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather")

_MOCK_DB = {
    "Hanoi": "29°C, trời mưa",
    "Haiphong": "33°C, mưa rào",
    "Danang": "30°C, nhiều mây",
}


@mcp.tool()
def get_weather(city: str) -> str:
    """Lấy thời tiết hiện tại của một thành phố."""
    return f"{city}: {_MOCK_DB.get(city, '28°C, không có dữ liệu chi tiết')}"


_MOCK_FORECAST_DB = {
    "Hanoi": ["25-30°C, mưa rào", "24-29°C, nhiều mây", "26-32°C, nắng nhẹ"],
    "Haiphong": ["26-33°C, mưa dông", "26-32°C, mưa rào", "27-33°C, nắng gián đoạn"],
    "Danang": ["25-31°C, nhiều mây", "25-30°C, mưa nhẹ", "26-32°C, nắng"],
}


@mcp.tool()
def get_forecast(city: str) -> str:
    """Lấy dự báo thời tiết 3 ngày tới của một thành phố."""
    days = _MOCK_FORECAST_DB.get(city, ["28°C, không có dữ liệu chi tiết"] * 3)
    today = date.today()
    lines = [
        f"{(today + timedelta(days=i)).isoformat()}: {day}"
        for i, day in enumerate(days, start=1)
    ]
    return f"Dự báo 3 ngày tới tại {city}:\n" + "\n".join(lines)


if __name__ == "__main__":
    mcp.run()  # mặc định chạy qua stdio
