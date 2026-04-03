from mcp.server.fastmcp import FastMCP
from random import choice

mcp = FastMCP("Get Travel Tips")

@mcp.tool()
def get_travel_tip() -> str:
    """
    Returns a random travel tip when the user asks about travelling.
    """
    travel_tips = [
        "Keep digital copies of important documents.",
        "Pack light and leave space for souvenirs.",
        "Always carry a reusable water bottle.",
        "Check local customs before you travel.",
        "Keep emergency contacts saved offline.",
        "Arrive at the airport early for international flights."
    ]

    return choice(travel_tips)

if __name__ == "__main__":
    mcp.run()
