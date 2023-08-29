from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
import sys
sys.dont_write_bytecode = True


def test_get_element():
    reader = KaistReader()
    element = reader.get_element()
    print(element)
    assert isinstance(element, Element)


# def test_get_element(no_data_element, expected_data_element):
#     reader = KaistReader()
#     result_element = reader.get_element(no_data_element)
#     assert result_element is expected_data_element
