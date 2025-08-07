try:
    from rich.console import Console
    console = Console()

    def info(msg): console.print(f"[INFO] {msg}", style="cyan")
    def warn(msg): console.print(f"[WARN] {msg}", style="yellow")
    def error(msg): console.print(f"[ERROR] {msg}", style="bold red")
    def success(msg): console.print(f"[SUCCESS] {msg}", style="green")

except ImportError:
    def info(msg): print(f"[INFO] {msg}")
    def warn(msg): print(f"[WARN] {msg}")
    def error(msg): print(f"[ERROR] {msg}")
    def success(msg): print(f"[SUCCESS] {msg}")