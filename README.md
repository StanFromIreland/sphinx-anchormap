# sphinx-anchormap

A Sphinx extension providing an ``anchormap`` directive for client-side
redirects of removed HTML anchors.

When a section or description is moved or removed, old ``#fragment``
links out in the wild break silently. ``anchormap`` lets you declare
redirect entries next to the content; they are resolved at build time,
embedded in the page as JSON, and a small script redirects visitors
from the stale anchor to its new location.

## Installation

```sh
pip install sphinx-anchormap
```

Then in ``conf.py``:

```python
extensions = [
    "anchor_redirects",
]
```

## Usage

Declare redirects in the document the old anchors used to live on:

```rst
.. anchormap::

   removed-anchor: :ref:`new-target`
```

Each entry is ``old-html-fragment: target``. The directive produces no output;
visiting the page with ``#removed-anchor`` in the URL redirects to the new
target instead.
