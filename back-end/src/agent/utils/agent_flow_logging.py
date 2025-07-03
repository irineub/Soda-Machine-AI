import shutil
import pprint
import json

class FlowLogger:
    COLORS = {
        "info": "\033[94m",     # blue
        "warn": "\033[93m",     # yellow
        "error": "\033[91m",    # red
        "success": "\033[92m",  # green
        "debug": "\033[95m",    # magenta
        "reset": "\033[0m"
    }

    def __init__(self, width_limit: int = 100):
        self.width_limit = width_limit

    def _stringify_extra(self, extra):
        if isinstance(extra, str):
            return extra
        try:
            return json.dumps(extra, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            return pprint.pformat(extra, indent=2, width=80)

    def print(self, title: str, level: str = "info", extra=None):
        color = self.COLORS.get(level, self.COLORS["info"])
        reset = self.COLORS["reset"]
        
        term_width = shutil.get_terminal_size((80, 20)).columns
        box_width = min(self.width_limit, term_width - 4)
        border = "+" + "-" * (box_width - 2) + "+"

        def wrap_lines(msg, width):
            lines = []
            for line in msg.split('\n'):
                while len(line) > width:
                    lines.append(line[:width])
                    line = line[width:]
                lines.append(line)
            return lines

        lines = wrap_lines(title.strip(), box_width - 4)
        if extra is not None:
            extra_str = self._stringify_extra(extra)
            lines += wrap_lines(extra_str.strip(), box_width - 4)

        print(color + border)
        for line in lines:
            print("| " + line.ljust(box_width - 4) + " |")
        print(border + reset)

    def info(self, title: str, extra=None):
        self.print(title, "info", extra)

    def warn(self, title: str, extra=None):
        self.print(title, "warn", extra)

    def error(self, title: str, extra=None):
        self.print(title, "error", extra)

    def success(self, title: str, extra=None):
        self.print(title, "success", extra)

    def debug(self, title: str, extra=None):
        self.print(title, "debug", extra)
