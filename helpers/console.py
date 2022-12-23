from pydub import AudioSegment
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


def print_step(text, style="bold red"):
    """Prints a rich info message."""
    panel = Panel(Text(text, justify="left"))
    console.print(panel, style=style)


def print_substep(text, style="green"):
    """Prints a rich info message without the panelling."""
    console.print(text, style=style)
