import cocotb
from cocotb.queue import Queue

from typing import Awaitable, TypeVar, Callable, Generic

V = TypeVar('V')
O = TypeVar('O')

class ConsumerMonitor(Generic[V, O]):
  """
  Reusable monitor of one-way streaming data interface when a queue value become available.

  Generics
    V: type of value to get from queue
    O: target object to set newly arrived values
  Args
    target: object to be set when queued value received
    setter: function accepting target and new value from queue to set
    queue: queue to await values
  """

  def __init__(self, target: O, setter: Callable[[O, V], None]):#, queue: Queue[V]):
    self._coro = None
    self._setter = setter
    self._queue = Queue[V]()
    self._target = target

  def start(self) -> None:
    """Start monitor"""
    if self._coro is not None:
      raise RuntimeError("Monitor already started")
    self._coro = cocotb.start_soon(self._run())

  def stop(self) -> None:
    """Stop monitor"""
    if self._coro is None:
      raise RuntimeError("Monitor never started")
    self._coro.kill()
    self._coro = None

  def put_nowait(self, v : V) -> None:
    self._queue.put_nowait(v)
  
  async def _run(self) -> None:
    while True:
      value = await self._queue.get()
      # cocotb.log.info(f"consumer value: {value}")
      self._setter(self._target, value)
