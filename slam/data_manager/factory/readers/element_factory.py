from dataclasses import dataclass


@dataclass
class Element:
    time: int
    measurement: dict
    # measurement["sensor"] = str()
    # measurement["data"] = list()
    location: dict
    # location["file"]: Path()
    # location["position"]: int()


# class ElementFactory():
#     def __init__(self):
#         self.elements = [Element]

#     def row_to_elements(self, row: dict) -> None:
#         full_row = next(reader)
#         used_row = {x: full_row[x] for x in self.__used_topic_names}
#         element = element(used_row)
