import cocotb
from cocotb.binary import BinaryValue
from cocotb.queue import Queue
from PyQt5.QtCore import QObject, pyqtSignal
from typing import Awaitable, TypeVar, Callable, Generic

V = TypeVar('V')
O = TypeVar('O')

class ProducerMonitor(QObject, Generic[V, O]):
    """
    Reusable monitor of one-way streaming data interface when an awaiter value changes.

    Generics
        V: type of value to stream
        O: type of object to monitor
    Args
        signal: named handle to be sampled when data changes
        value_resolver: function accepting handle of monitored value, returning value to place in monitor queue
        awaiter: async function defining wait criteria before fetching value and queueing
    """

    value = pyqtSignal(BinaryValue)

    def __init__(self, signal: O, value_resolver: Callable[[O], V], awaiter: Awaitable[O]):
        super(ProducerMonitor, self).__init__()
        self._signal = signal
        self._coro = None
        self._value_resolver = value_resolver
        self._awaiter = awaiter

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

    async def _run(self) -> None:
        while True:
            await self._awaiter(self._signal)
            val = self._value_resolver(self._signal)
            # cocotb.log.info(f"producer value: {val}")
            self.value.emit(val)
