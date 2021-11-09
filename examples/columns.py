"""
This example shows how to display content in columns.

The data is pulled from https://randomuser.me
"""

import json
from urllib.request import urlopen

from quo.console import Console
from quo.columns import Columns
from quo.panel import Panel


def get_content(user):
    """Extract text from user dict."""
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"
    return f"[b]{name}[/b]\n[yellow]{country}"


console = Console()


users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
console.echo(users, overflow="ignore", crop=False)
user_renderables = [Panel(get_content(user), expand=True) for user in users]
console.echo(Columns(user_renderables))
