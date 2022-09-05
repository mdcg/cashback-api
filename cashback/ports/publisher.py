from abc import ABC


class MessagePublisherPort(ABC):
    def enqueue(payload: str):
        pass
