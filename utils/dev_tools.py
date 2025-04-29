import time
import functools
import rich

def compiling_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        rich.print(f"File [bold green]{args[0]}[/bold green] took [italic green]{elapsed:.4f} seconds[/italic green] to compile")
        return result

    return wrapper
