"""Timeout utilities using threading or signals."""
import signal
import threading
from functools import wraps
from typing import Any, Callable, Optional, TypeVar

T = TypeVar('T')

class TimeoutError(Exception):
    """Raised when a function call times out."""
    pass

def timeout(seconds: int) -> Callable:
    """
    Decorator that enforces a timeout on function execution.
    
    On Unix systems, uses signal.SIGALRM.
    On other systems, falls back to threading.Timer.
    
    Args:
        seconds: Maximum execution time in seconds.
    
    Returns:
        Decorated function that will raise TimeoutError if execution exceeds the limit.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if hasattr(signal, 'SIGALRM'):  # Unix systems
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                def handler(signum: int, frame: Optional[Any]) -> None:
                    raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
                
                # Set the timeout handler and alarm
                old_handler = signal.signal(signal.SIGALRM, handler)
                signal.alarm(seconds)
                
                try:
                    result = func(*args, **kwargs)
                finally:
                    # Restore the old handler and cancel the alarm
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, old_handler)
                return result
            
        else:  # Non-Unix systems (using threading)
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> T:
                result = []
                error = []
                
                def worker():
                    try:
                        result.append(func(*args, **kwargs))
                    except Exception as e:
                        error.append(e)
                
                thread = threading.Thread(target=worker)
                thread.daemon = True
                thread.start()
                thread.join(seconds)
                
                if thread.is_alive():
                    thread.join(0)  # Clean up the thread
                    raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
                if error:
                    raise error[0]
                return result[0]
        
        return wrapper
    return decorator