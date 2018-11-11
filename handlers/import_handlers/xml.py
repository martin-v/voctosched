import logging

from lxml import etree
from hacks import noexcept
from ..base import ImportHandler

from util import read_input


log = logging.getLogger(__name__)


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
                    personnames = []
                    if event.find('persons') is not None:
                        for person in event.find('persons').iter('person'):
                            personname = re.sub('\s+', ' ', person.text).strip()
                            personnames.append(personname)

                    id = int(event.get('id'))

                    if id in titlemap:
                        title = titlemap[id]
                    elif event.find('title') is not None and event.find('title').text is not None:
                        title = re.sub('\s+', ' ', event.find('title').text).strip()
                    else:
                        title = ''

                    if event.find('subtitle') is not None and event.find('subtitle').text is not None:
                        subtitle = re.sub('\s+', ' ', event.find('subtitle').text).strip()
                    else:
                        subtitle = ''

                    # yield a tupel with the event-id, event-title and person-names
                    yield {
                        'id': id,
                        'title': title,
                        'subtitle': subtitle,
                        'persons': personnames,
                        'personnames': ', '.join(personnames),
                        'room': room.attrib['name'],
                        'track': event.find('track').text
                    }