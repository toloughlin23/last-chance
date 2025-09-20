from __future__ import annotations

import queue
import threading
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

MessageHandler = Callable[[object], None]


@dataclass
class ChannelConfig:
    name: str
    maxsize: int = 1000


class Hub:
    """In-memory pub/sub hub with bounded queues and backpressure.

    - No mocks; delivers real messages between producer (controller) and consumers (future services).
    - Thread-safe publish/subscribe.
    """

    def __init__(self) -> None:
        self._channels: Dict[str, queue.Queue] = {}
        self._handlers: Dict[str, List[MessageHandler]] = {}
        self._locks: Dict[str, threading.Lock] = {}

    def ensure_channel(self, name: str, maxsize: int = 1000) -> None:
        if name not in self._channels:
            self._channels[name] = queue.Queue(maxsize=maxsize)
            self._handlers[name] = []
            self._locks[name] = threading.Lock()

    def subscribe(self, channel: str, handler: MessageHandler) -> None:
        self.ensure_channel(channel)
        with self._locks[channel]:
            self._handlers[channel].append(handler)

    def publish(self, channel: str, message: object, block: bool = True, timeout: Optional[float] = None) -> None:
        self.ensure_channel(channel)
        q = self._channels[channel]
        # Put message with backpressure
        q.put(message, block=block, timeout=timeout)
        # Fan-out to handlers synchronously (handlers must be fast)
        for handler in list(self._handlers.get(channel, [])):
            try:
                handler(message)
            except Exception:
                # Non-fatal: continue delivering to other handlers
                continue
