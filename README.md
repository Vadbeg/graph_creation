# graph_creation

This is a project for creating graphs from json
files with raw data about images

## Getting started

To download project:

```
git clone 
```

## Installing
To use this project you need to install
[pyvis](https://pyvis.readthedocs.io/en/latest/) library

To install it, print:

```
pip install pyvis
```

## Requirements

- python >= 3.6
- pyvis

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

You need to add them into <span style="color:red">data</span> directory

## Build With

* [pyvis](https://pyvis.readthedocs.io/en/latest/) - interactive network visualizations

## Authors

* **Vadim Titko** aka *Vadbeg* - [GitHub](https://github.com/Vadbeg/PythonHomework/commits?author=Vadbeg)