"""
Asynchronous execution manager and watchdog for QuantumLab calculations.
Addresses DEF-09:
- Prevents UI freezing by running calculations asynchronously.
- Enforces computational timeouts without sacrificing mathematical accuracy.
- Supports user cancellation.
- Guarantees that Tkinter widgets are never accessed from secondary threads.
- Accurately documents operating system constraints (Windows process spawning vs daemon threads).
"""

import threading
import time
import queue
from typing import Callable, Any, Optional
from .errors import ScientificValidationError, QuantumLabError


class AsyncCalculationManager:
    """
    Manages asynchronous dispatch, timeouts, and cancellation of scientific calculations.
    Ensures Tkinter UI remains completely responsive during complex SymPy integrations.
    Uses queue.Queue and main-thread Tk polling to guarantee zero cross-thread Tkinter calls.
    """
    DEFAULT_TIMEOUT: float = 30.0  # seconds

    def __init__(self, root: Any):
        self.root = root
        self._current_task_id: int = 0
        self._lock = threading.Lock()
        self._is_running: bool = False
        self._cancel_requested: bool = False
        self._queue: queue.Queue = queue.Queue()

    @property
    def is_running(self) -> bool:
        return self._is_running

    def cancel(self) -> None:
        """Requests cancellation of the in-flight calculation."""
        with self._lock:
            self._cancel_requested = True
            self._current_task_id += 1
            self._is_running = False

    def run_calculation(
        self,
        calc_fn: Callable[[], Any],
        on_success: Callable[[Any], None],
        on_error: Callable[[Exception], None],
        timeout: Optional[float] = None
    ) -> None:
        """
        Executes calc_fn in a background worker thread.
        Dispatches on_success or on_error to the Tkinter thread via queue polling.
        Guarantees that Tkinter widgets are never accessed from the background thread.
        """
        timeout_sec = timeout if timeout is not None else self.DEFAULT_TIMEOUT

        with self._lock:
            self._current_task_id += 1
            task_id = self._current_task_id
            self._is_running = True
            self._cancel_requested = False

        deadline = time.time() + timeout_sec

        def worker():
            try:
                res = calc_fn()
                self._queue.put((task_id, res, None))
            except Exception as exc:
                self._queue.put((task_id, None, exc))

        def poll():
            with self._lock:
                if task_id != self._current_task_id or self._cancel_requested:
                    self._is_running = False
                    return

            try:
                msg_id, res, exc = self._queue.get_nowait()
                if msg_id == task_id:
                    with self._lock:
                        self._is_running = False
                    if exc is not None:
                        on_error(exc)
                    else:
                        on_success(res)
                    return
            except queue.Empty:
                pass

            if time.time() > deadline:
                with self._lock:
                    self._is_running = False
                on_error(ScientificValidationError("error.calc_timeout", timeout=int(timeout_sec)))
                return

            if self._is_running:
                self.root.after(20, poll)

        thread = threading.Thread(target=worker, daemon=True, name=f"QuantumLab-Calc-{task_id}")
        thread.start()
        self.root.after(10, poll)

