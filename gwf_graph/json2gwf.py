import os
from typing import Tuple, Dict, Set, List

import json
import xml

from pyvis_graph.GraphCreation import create_graph_structure, create_graph_structure_attributes

from gwf_graph.gwf_template import GWF


def add_relation(gwf: GWF, main_node_name: str, relations: Set[Tuple[str, str]]):
    main_node = gwf.add_general_node(main_node_name)

    print(relations)
    for curr_relation in relations:
        print(curr_relation)
        relation_name, sub_node_name = curr_relation

        sub_node = gwf.add_general_node(sub_node_name)

        orient_pair = gwf.add_orient_pair(id1=main_node.attrib['id'], id2=sub_node.attrib['id'])

        relation_node = gwf.add_relation_node(relation_name)
        gwf.add_pos_arc(id1=relation_node.attrib['id'], id2=orient_pair.attrib['id'])


def add_attribute(gwf: GWF, main_node_name: str, attributes: Set[str]):
    main_node = gwf.add_general_node(main_node_name)

    for curr_attribute_name in attributes:
        attr_node = gwf.add_group_node(curr_attribute_name)

        gwf.add_pos_arc(id1=attr_node.attrib['id'], id2=main_node.attrib['id'])


def add_all_relations(gwf: GWF, all_relations: List[Tuple[str, Set[Tuple[str, str]]]]):
    print(all_relations)

    for curr_relation in all_relations:
        node_name = curr_relation[0]
        sub_relation = curr_relation[1]

        add_relation(gwf, main_node_name=node_name, relations=sub_relation)


def add_all_attributes(gwf: GWF, all_attributes: List[Tuple[str, Set[str]]]):
    for curr_attribute in all_attributes:
        node_name = curr_attribute[0]
        sub_attribute = curr_attribute[1]

        add_attribute(gwf, main_node_name=node_name, attributes=sub_attribute)


def transform(gwf: GWF, all_relations: List[Tuple[str, Set[Tuple[str, str]]]],
              all_attributes: List[Tuple[str, Set[str]]], save_path: str):
    # add_all_relations(gwf, all_relations=all_relations)
    add_all_attributes(gwf, all_attributes=all_attributes)

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

    gwf = GWF()

    transform(gwf, all_relations=res_rel, all_attributes=res_attr, save_path='gwf_examples/res.gwf')
