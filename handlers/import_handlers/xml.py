import logging
import re

from lxml import etree
from hacks import noexcept
from ..base import ImportHandler

from util import read_input


log = logging.getLogger(__name__)

def _text(node, name):
    try:
        return node.find(name).text
    except AttributeError:
        return None

class XMLImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        parser = etree.XMLParser(huge_tree=True)
        schedule = etree.fromstring(read_input(self.config['path']), parser)

        for day in schedule.iter('day'):
            # iterate all rooms
            for room in day.iter('room'):
                # iterate events on that day in this room
                for event in room.iter('event'):
                    # aggregate names of the persons holding this talk
                    person_names = []
                    if event.find('persons') is not None:
                        for person in event.find('persons').iter('person'):
                            person_name = re.sub('\s+', ' ', person.text).strip()
                            person_names.append(person_name)

                    event_id = int(event.get('id'))
                    title = _text(event, 'title')

                    print(event_id, title)

                    # if event.find('subtitle') is not None and event.find('subtitle').text is not None:
                    #     subtitle = re.sub('\s+', ' ', event.find('subtitle').text).strip()
                    # else:
                    #     subtitle = ''
                    #
                    # # yield a tupel with the event-id, event-title and person-names
                    # yield {
                    #     'id': id,
                    #     'title': title,
                    #     'subtitle': subtitle,
                    #     'persons': person_names,
                    #     'person_names': ', '.join(person_names),
                    #     'room': room.attrib['name'],
                    #     'track': event.find('track').text
                    # }