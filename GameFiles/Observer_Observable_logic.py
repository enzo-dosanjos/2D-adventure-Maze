class Observer:
    """ Observer pattern """
    __slots__ = []
    def update(self, message, *args):
        """
        Handle updates received from an observable.

        Args:
            message (str): An identifier for an event
            *args: additional information needed by the observer
        """
        pass

class Observable:
    """ a class that notifies observer automatically of any state changes."""

    __slots__ = ['observer']

    def __init__(self):
        """ Initialize the Observable class with no observers """
        self.observer = None

    def add_observer(self, observer):
        """
        add an observer to the observable.

        Args:
            observer (Observer): The observer object that will receive notifications
        """
        self.observer = observer

    def notify_observer(self, message, *args):
        """
        Notify the attached observer of a particular event

        Args:
            message (str): event  to notify the observer about
            *args: Additional parameters needed by the observer
        """
        self.observer.update_observer(message, *args)