"""
Main converter module

@by Vadbeg
"""

import os
from typing import Tuple, Dict, Set, List, Optional

import json

from lxml import etree

from pyvis_graph.GraphCreation import create_graph_structure, create_graph_structure_attributes

from gwf_graph.gwf_template import GWF


def add_class_to_general_node(gwf: GWF, general_node: etree.SubElement) -> List[etree.SubElement]:
    """
    Adds class to general node (every general node need some kind of class)

    :param gwf: gwf template class
    :param general_node: general node
    :return: elements created in this function
    """

    class_node = gwf.add_group_node(name='concept_' + general_node.attrib['idtf'])
    # class_node = gwf.add_group_node(name='')

    pos_arc = gwf.add_pos_arc(id1=class_node.attrib['id'], id2=general_node.attrib['id'])

    contour_els_list = [class_node, pos_arc]

    return contour_els_list


def add_relation(gwf: GWF, main_node_name: str, relations: Set[Tuple[str, str]]) -> List[etree.SubElement]:
    """
    Adds relation between nodes

    :param gwf: gwf template class
    :param main_node_name: name of node from which relation begins
    :param relations: given relations
    :return: elements created in this function
    """

    contour_els_list = list()

    main_node = gwf.add_general_node(main_node_name)
    class_contour_els = add_class_to_general_node(gwf=gwf, general_node=main_node)

    contour_els_list.append(main_node)
    contour_els_list.extend(class_contour_els)

    for curr_relation in relations:
        relation_name, sub_node_name = curr_relation

        sub_node = gwf.add_general_node(sub_node_name)
        class_contour_els_sub = add_class_to_general_node(gwf=gwf, general_node=sub_node)

        contour_els_list.append(sub_node)
        contour_els_list.extend(class_contour_els_sub)

        orient_pair = gwf.add_orient_pair(id1=main_node.attrib['id'], id2=sub_node.attrib['id'])
        contour_els_list.append(orient_pair)

        relation_node = gwf.add_relation_node(relation_name)
        contour_els_list.append(relation_node)

        pos_arc = gwf.add_pos_arc(id1=relation_node.attrib['id'], id2=orient_pair.attrib['id'])
        contour_els_list.append(pos_arc)

    return contour_els_list


def add_attribute(gwf: GWF, main_node_name: str, attributes: Set[str]) -> List[etree.SubElement]:
    """
    Creates attributes from given nodes

    :param gwf: gwf template class
    :param main_node_name: name of node from which relation begins
    :param attributes: give attributes
    :return: elements created in this function
    """

    contour_els_list = list()

    main_node = gwf.add_general_node(main_node_name)
    class_contour_els = add_class_to_general_node(gwf=gwf, general_node=main_node)

    contour_els_list.append(main_node)
    contour_els_list.extend(class_contour_els)

    for curr_attribute_name in attributes:
        attr_node = gwf.add_group_node(curr_attribute_name)

        contour_els_list.append(attr_node)

        arc = gwf.add_pos_arc(id1=attr_node.attrib['id'], id2=main_node.attrib['id'])
        contour_els_list.append(arc)

    return contour_els_list


def add_all_relations(gwf: GWF, all_relations: List[Tuple[str, Set[Tuple[str, str]]]]) -> List[etree.SubElement]:
    """
    Creates all relations

    :param gwf: gwf template class
    :param all_relations: all relations
    :return: elements created in this function
    """

    nodes_list = list()

    for curr_relation in all_relations:
        node_name = curr_relation[0]
        sub_relation = curr_relation[1]

        temp_nodes_list = add_relation(gwf, main_node_name=node_name, relations=sub_relation)
        nodes_list.extend(temp_nodes_list)

    return nodes_list


def add_all_attributes(gwf: GWF, all_attributes: List[Tuple[str, Set[str]]]):
    """
    Creates all attributes

    :param gwf: gwf template object
    :param all_attributes: all attributes
    :return: elements created in this function
    """

    nodes_list = list()

    for curr_attribute in all_attributes:
        node_name = curr_attribute[0]
        sub_attribute = curr_attribute[1]

        temp_nodes_list = add_attribute(gwf, main_node_name=node_name, attributes=sub_attribute)
        nodes_list.extend(temp_nodes_list)

    return nodes_list


def wrap_in_contour(gwf: GWF, all_nodes_in_contour: List[etree.SubElement], contour_name) -> etree.SubElement:
    """
    Creates wrapper around all elements. To make easier access to them in ostis

    :param gwf: gwf template object
    :param all_nodes_in_contour: all nodes which we need to add in contour
    :param contour_name: name of contour
    :return: contour element (etree element)
    """

    contour = gwf.add_contour(all_nodes_in_contour=all_nodes_in_contour)

    name_node = gwf.add_general_node(contour_name)
    gwf.add_pos_arc(id1=name_node.attrib['id'], id2=contour.attrib['id'])

    return contour


def transform(gwf: GWF, all_relations: List[Tuple[str, Set[Tuple[str, str]]]],
              all_attributes: List[Tuple[str, Set[str]]], name: str,
              save_path: str):
    """
    Preforms transform on all data.

    :param gwf: gwf template object
    :param all_relations: all relations from data
    :param all_attributes: all attributes from data
    :param name: name of conour
    :param save_path: path to which we want to save them
    """

    nodes = list()

    nodes_list_relations = add_all_relations(gwf, all_relations=all_relations)
    nodes_list_attributes = add_all_attributes(gwf, all_attributes=all_attributes)

    nodes.extend(nodes_list_relations)
    nodes.extend(nodes_list_attributes)

    contour = wrap_in_contour(gwf, all_nodes_in_contour=nodes, contour_name=name)

    gwf.save(save_path)


if __name__ == '__main__':
    directory = '../data'
    print(os.listdir(directory))

    filepath_relationship = os.path.join(directory, 'relationships.json')
    filepath_attributes = os.path.join(directory, 'attributes.json')

    with open(filepath_relationship, 'rb') as file:
        relationships = json.load(file)

    with open(filepath_attributes, 'rb') as file:
        attributes = json.load(file)

    image_url = attributes['image_url']

    res_rel = create_graph_structure(relationships)
    res_attr = create_graph_structure_attributes(attributes)

    res_rel = list(res_rel.items())
    res_attr = list(res_attr.items())

    print(res_rel)
    print(res_attr)

    gwf = GWF()

    if not os.path.exists('gwf_examples'):
        os.makedirs('gwf_examples')

    transform(gwf, all_relations=res_rel, all_attributes=res_attr,
              save_path='gwf_examples/res.gwf', name='first_image')
