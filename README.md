# Graph creation

This is a project for creating graphs from json
files with raw data about images. 

In this project you can:
1. Show graphs from VisualGenome json files using pyvis library
2. Transform this graph into OSTIS .gwf graph

## Download project

```
git clone https://github.com/Vadbeg/graph_creation.git
```

## Installing

To install all requirements, print (in main directory):

```
pip install -e .
```

## Files which you need:

- relationships.json

File should be with just one image, so it will look like:

```
{"relationships": [
  {"predicate": "ON", "object": {"h": 290, "object_id": 1058534, "merged_object_ids": [5046], "synsets": ["sidewalk.n.01"], "w": 722, "y": 308, "x": 78, "names": ["sidewalk"]}, "relationship_id": 15927, "synsets": ["along.r.01"], "subject": {"name": "shade", "h": 192, "synsets": ["shade.n.01"], "object_id": 5045, "w": 274, "y": 338, "x": 119}},
  {"predicate": "near", "object": {"name": "tree", "h": 360, "synsets": ["tree.n.01"], "object_id": 1058545, "w": 176, "y": 0, "x": 249}, "relationship_id": 3186260, "synsets": ["about.r.07"], "subject": {"name": "bikes", "h": 35, "synsets": ["bicycle.n.01"], "object_id": 1058544, "w": 40, "y": 319, "x": 321}}
  "image_id": 1}
```

- attributes.json

And the same, file should be with just one image:

```
{"image_id": 1,
  "image_url": "https://cs.stanford.edu/people/rak248/VG_100K_2/1.jpg",
  "attributes": [
    {"synsets": ["clock.n.01"], "h": 339, "object_id": 1058498, "names": ["clock"], "w": 79, "attributes": ["green", "tall"], "y": 91, "x": 421},
    {"synsets": ["street.n.01"], "h": 262, "object_id": 5046, "names": ["street"], "w": 714, "attributes": ["sidewalk"], "y": 328, "x": 77},
    {"synsets": ["shade.n.01"], "h": 192, "object_id": 5045, "names": ["shade"], "w": 274, "y": 338, "x": 119}
  ]}
```

You need to add them into <i>data</i> directory

## Transform <i>json</i> to <i>html</i>

To run script you need to print this command in CL (in <i>pyvis_graph</i> directory):

```
>> python GraphCreation.py
```

After command execution, file <i>graph.html</i> will appear in <i>pyvis_graph</i> directory.
 
 ## Transform <i>json</i> to <i>gwf</i>
 
To run script you need to print this command in CL (in <i>gwf_graph</i> directory):

```
>> python json2gwf.py
```
After command execution, file <i>res.gwf</i> will appear in <i>gwf_graph/gwf_examples</i> directory.
 
## Build With

* [pyvis](https://pyvis.readthedocs.io/en/latest/) - interactive network visualizations
* [lxml](https://lxml.de) - xml parser used

## Authors

* **Vadim Titko** aka *Vadbeg* - [GitHub](https://github.com/Vadbeg/PythonHomework/commits?author=Vadbeg)
| [LinkedIn](https://www.linkedin.com/in/vadim-titko-89ab16149/)
