import json
import os.path
from unittest import TestCase

from messaging.reflectable_media_component import serialize_media_component, MediaComponent, \
    deserialize_media_component, ReflectableComponent


class TestSerializeMediaComponent(TestCase):
    def test_serialize_media_component(self):
        resources = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'test_resources')
        json_file = os.path.join(resources, 'test_out.json')
        assert os.path.exists(json_file)
        stripped = self.read_lines_stripped(json_file)
        in_value: ReflectableComponent = serialize_media_component(stripped)
        assert len(in_value.components) == 1
        key = None
        for key in in_value.components.keys():
            pass
        assert key
        in_value_items: list[MediaComponent] = in_value.components[key]
        in_value_item = in_value_items[0]

        assert len(in_value_item.values) == 1
        assert in_value_item.date
        assert in_value_item.id == "https://google.com"

        assert in_value_item.values[0].key == key
        assert in_value_item.values[0].mime_type == "text/html"
        assert in_value_item.values[0].file_extension == "TEXT"
        assert in_value_item.values[0].metadata.metadata_path
        assert in_value_item.values[0].metadata.file_path

        out = deserialize_media_component(in_value)
        with open(os.path.join(resources, 'test_in.json'), 'w') as out_file:
            out_file.write(out.strip())

    def read_lines_stripped(self, json_file):
        with open(json_file) as j:
            line = j.readlines()
            line = map(lambda x: x.strip(), line)
            return ''.join(line)
