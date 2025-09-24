from collections.abc import Iterable

from moduslam.frontend_manager.main_graph.graph import Graph, GraphElement


def add_elements_to_graph(
    graph: Graph, new_elements: GraphElement | Iterable[GraphElement]
) -> None:
    """Adds new element(s) to the graph.

    Args:
        graph: a graph to which the element(s) will be added.
        new_elements: new element(s) to be added.
    """
    if isinstance(new_elements, Iterable):
        for element in new_elements:
            graph.add_element(element)
    else:
        graph.add_element(new_elements)


def expand_elements(elements: list[GraphElement], item: GraphElement | list[GraphElement]) -> None:
    """Expands elements with a new item.

    Args:
        elements: a list to expand.

        item: a new item or a list of new items.
    """
    if isinstance(item, Iterable):
        for element in item:
            elements.append(element)
    else:
        elements.append(item)
