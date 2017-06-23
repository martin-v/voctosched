from fahrplan.xml import XmlWriter, XmlSerializable
from .event import Event


class Room(XmlSerializable):
    def __init__(self, name: str):
        self.name = name
        self.events = dict()

    def add_event(self, event: Event):
        event.room = self.name
        self.events[event.id] = event

    def get_start(self):
        try:
            return min(event.date for event in self.events.values())
        except ValueError:
            # No events assigned
            return None

    def get_end(self):
        try:
            return max(event.date + event.duration for event in self.events.values())
        except ValueError:
            # No events assigned
            return None

    def append_xml(self, xml: XmlWriter):
        with xml.context("room", name=self.name):
            for event in self.events.values():
                xml.append_object(event)