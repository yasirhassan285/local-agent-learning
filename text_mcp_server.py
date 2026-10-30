from mcp.server import MCPServer


mcp = MCPServer("Local Text Server")


@mcp.tool()
def word_count(text: str) -> int:
    """Count the number of whitespace-separated words in text."""
    return len(text.split())


@mcp.tool()
def uppercase(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


if __name__ == "__main__":
    mcp.run()