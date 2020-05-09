import os
import json
import random
from typing import Tuple, List

from lxml import etree


class GWF:
    def __init__(self):
        self.root = etree.Element('GWF')
        self.root.attrib['version'] = '2.0'

        self.static_sector = etree.SubElement(self.root, 'staticSector')
        self.id_list = set()

    def __str__(self) -> str:
        res = str(etree.tostring(self.root, pretty_print=False))

        return res

    def __get_unique_id__(self) -> int:
        id = random.randint(0, 10**5)

        while id in self.id_list:
            id = random.randint(0, 10 ** 5)

        return id

    @staticmethod
    def __get_random_coord__() -> Tuple[str, str]:
        x = random.randint(0, 1000)
        y = random.randint(0, 1000)

        x = str(x)
        y = str(y)

        return x, y

    def __add_node__(self, name: str, node_type: str = 'node/const/general_node') -> etree.SubElement:
        node = etree.SubElement(self.static_sector, 'node')

        node.attrib['type'] = node_type
        node.attrib['idtf'] = name
        node.attrib['id'] = str(self.__get_unique_id__())
        node.attrib['parent'] = '0'

        x, y = self.__get_random_coord__()  # TODO: think about better way to get coordinates
        node.attrib['x'] = str(x)
        node.attrib['y'] = str(y)

        content = etree.SubElement(node, 'content')
        content.attrib['type'] = '0'
        content.attrib['content_visibility'] = 'false'
        content.attrib['mime_type'] = ''

        return node

    def __add_arc__(self, id1: str, id2: str, arc_type: str = 'arc/const/pos') -> etree.SubElement:
        arc = etree.SubElement(self.static_sector, 'arc')

        arc.attrib['type'] = arc_type
        arc.attrib['idtf'] = ''
        arc.attrib['id'] = str(self.__get_unique_id__())
        arc.attrib['parent'] = '0'

        arc.attrib['id_b'] = str(id1)
        arc.attrib['id_e'] = str(id2)

        arc.attrib['dotBBalance'] = '0.0'
        arc.attrib['dotEBalance'] = '0.0'

        content = etree.SubElement(arc, 'points')

        return arc

    def __add_contour__(self, all_nodes_in_contour: List[etree.SubElement]):
        contour = etree.SubElement(self.static_sector, 'contour')

        contour.attrib['type'] = ''
        contour.attrib['idtf'] = ''
        contour.attrib['id'] = str(self.__get_unique_id__())
        contour.attrib['parent'] = '0'

        content = etree.SubElement(contour, 'points')
        print(dict(zip(('x', 'y'), self.__get_random_coord__())))
        point1 = etree.SubElement(content, 'point', attrib=dict(zip(('x', 'y'), self.__get_random_coord__())))
        point2 = etree.SubElement(content, 'point', attrib=dict(zip(('x', 'y'), self.__get_random_coord__())))
        point3 = etree.SubElement(content, 'point', attrib=dict(zip(('x', 'y'), self.__get_random_coord__())))

        for node in all_nodes_in_contour:
            # print(contour)
            print(node)
            node.attrib['parent'] = contour.attrib['id']

        return contour

    def add_group_node(self, name: str) -> etree.SubElement:
        node = self.__add_node__(name=name, node_type='node/const/group')

        return node

    def add_general_node(self, name: str) -> etree.SubElement:
        node = self.__add_node__(name=name, node_type='node/const/general_node')

        return node

    def add_relation_node(self, name: str) -> etree.SubElement:
        node = self.__add_node__(name=name, node_type='node/const/relation')

        return node

    def add_role_node(self, name: str) -> etree.SubElement:
        node = self.__add_node__(name=name, node_type='node/const/attribute')

        return node

    def add_pos_arc(self, id1: str, id2: str) -> etree.SubElement:
        arc = self.__add_arc__(id1=id1, id2=id2, arc_type='arc/const/pos')

        return arc

    def add_orient_pair(self, id1: str, id2: str) -> etree.SubElement:
        arc = self.__add_arc__(id1=id1, id2=id2, arc_type='pair/const/orient')

        return arc

    def add_contour(self, all_nodes_in_contour: List[etree.SubElement]) -> etree.SubElement:
        contour = self.__add_contour__(all_nodes_in_contour=all_nodes_in_contour)

        return contour

    def save(self, path: str):
        res = etree.tostring(self.root, pretty_print=True)

        with open(path, mode='wb') as file:
            file.write(res)


if __name__ == '__main__':
    gwf = GWF()

    node1 = gwf.add_general_node('gen_node1')
    node2 = gwf.add_general_node('gen_node2')

    node3 = gwf.add_group_node('group1')
    gwf.add_group_node('group2')

    gwf.add_role_node('role1')
    gwf.add_role_node('role2')

    gwf.add_relation_node('relation1')
    gwf.add_relation_node('relation2')

    gwf.add_orient_pair(node1.attrib['id'], node2.attrib['id'])
    gwf.add_pos_arc(node1.attrib['id'], node3.attrib['id'])

    print(gwf)

    path = os.path.join('gwf_examples', 'res.gwf')
    gwf.save(path)
