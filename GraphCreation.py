"""
Script for creating graph which describe given image


@by Vadbeg
"""


import json
import os

from pyvis.network import Network


directory = 'data'

filepath_relationship = os.path.join(directory, 'relationships.json')
filepath_attributes = os.path.join(directory, 'attributes.json')

with open(filepath_relationship, 'rb') as file:
    relationships = json.load(file)

with open(filepath_attributes, 'rb') as file:
    attributes = json.load(file)

image_url = attributes['image_url']


def have_predicate(relationships, name):
    """
    Check if subject have more than one predicate
    to the same object

    :param relationships: predicates and objects for subject
    :param name: name of object which we like to add
    :return: bool
    """

    for relationship in relationships:
        if name == relationship[1]:
            return True

    return False


def create_graph_structure(relationships):
    """
    Creates graph structure from raw relationships file


    :param relationships: raw dict of relationships
    :return: processed relationships
    """

    result = dict()

    for relationship in (relationships['relationships']):
        predicate = relationship['predicate']
        object_info = relationship['object']
        subject_info = relationship['subject']

        if 'names' in object_info.keys():
            object_name = object_info['names'][0]
        elif 'name' in object_info.keys():
            object_name = object_info['name']
        else:
            object_name = ''

        if 'names' in subject_info.keys():
            subject_name = subject_info['names'][0]
        elif 'name' in subject_info.keys():
            subject_name = subject_info['name']
        else:
            subject_name = ''

        result.setdefault(subject_name, set())

        if have_predicate(result[subject_name], object_name):
            continue

        result[subject_name].add((predicate, object_name))

    return result


def create_graph(graph_structure, filepath):
    """
    Creates and save graph from given processed relationships

    :param graph_structure: processed relationships
    :param filepath: path in which we like to save file
    :return: None
    """

    graph = Network(directed=True, height='800px', width='800px')

    for el1, connected_elements in graph_structure.items():
        if el1 not in graph.nodes:
            graph.add_node(el1)

        for connected_element in connected_elements:
            el2 = connected_element[1]
            predicate = connected_element[0]

            if el2 not in graph.nodes:
                graph.add_node(el2)

            graph.add_edge(el1, el2, title=predicate, label=predicate)

    graph.save_graph(filepath)


def add_image(filepath, image_src):
    """
    Adds image into created html file

    :param filepath: path to html file
    :param image_src: source of image
    :return: None
    """

    image_div = f"""
    <div align="left" style="float:right; width: 500px; height: 500px; margin=10px">
        <img src="{image_src}" width="500px" height="500px">
    </div>
    """

    with open(filepath, 'r') as file:
        html = file.readlines()

    body_close_index = 0

    for index, line in enumerate(html):
        if line.strip() == '</body>':
            body_close_index = index

    res_html = html[:body_close_index] + [image_div] + html[body_close_index:]

    with open(filepath, 'w') as file:
        file.write(''.join(res_html))


filepath = 'graph.html'

graph_structure = create_graph_structure(relationships)
create_graph(graph_structure, filepath)
add_image(filepath=filepath, image_src=image_url)
