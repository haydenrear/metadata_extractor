from unittest import TestCase

from dotenv import load_dotenv
from drools_py.inject.injector_provider import InjectionContext

from metadata_extractor.delegating_metadata_extractor import MultiStringClassifier


class TestProdMetadataExtractorModules(TestCase):
    def test_injector(self):
        load_dotenv()
        InjectionContext.do_initialize()
        assert isinstance(InjectionContext.environment.get_property('classifiers'), list) != 0
        classifier = InjectionContext.get_injector('test').get(MultiStringClassifier)
        out = classifier.classify_item('When I went on the trip to San Diego it was a great place to go.')
        print(out)

