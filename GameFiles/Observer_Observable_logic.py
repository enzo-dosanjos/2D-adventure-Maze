class Observer:
    def update(self, message, *args):
        """Update the observer with a message."""
        pass

class Observable:
    def __init__(self):
        self.observer = None

    def add_observer(self, observer):
        self.observer = observer

    def notify_observer(self, message, *args):
        self.observer.update(message, *args)