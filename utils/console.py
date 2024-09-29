from enum import Enum
from rich import print as rprint
from rich.console import Console
from rich.style import Style
from rich.progress import Progress

CONSOLE = Console()

# Define the message types
class MessageType(Enum):
    SUCCESS = "success"
    WARN = "warn"
    FATAL = "fatal"
    INFO = "info"

# Define the styles with emojis
styles = {
    MessageType.SUCCESS: Style(color="green", bold=False),
    MessageType.WARN: Style(color="yellow", bold=False),
    MessageType.FATAL: Style(color="red", bold=False, underline=True),
    MessageType.INFO: Style(color="blue", bold=False),
}

# Define the emojis
emojis = {
    MessageType.SUCCESS: ":white_check_mark:",  # ✅
    MessageType.WARN: ":warning:",              # ⚠️
    MessageType.FATAL: ":x:",                   # ❌
    MessageType.INFO: ":information_source:",   # ℹ️
}

# Helper function for standard formatting
def pretty_print(
        message: str,
        message_type: MessageType = MessageType.INFO,
        json: bool = False,
        progress: Progress = None
):
    console = CONSOLE
    if progress:
        console = progress.console

    if message_type in styles and message_type in emojis:
        emoji = emojis[message_type]
        if not json:
            console.print(
                f"{emoji} {message}",
                style=styles[message_type]
            )
        else:
            console.print_json(
                f"{message}"
            )
    else:
        console.print(message)