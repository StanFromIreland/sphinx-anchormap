"""Tests for the anchor_redirects extension."""

import sys
import tempfile
import unittest
from pathlib import Path

from sphinx.application import Sphinx

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

CONF = "extensions = ['anchor_redirects']\n"

INDEX = """\
Index
=====

.. toctree::

   old

.. _new-home:

New home
--------

Content lives here now.
"""

OLD = """\
Old page
========

.. anchormap::

   removed-anchor: :ref:`new-home`

Some content.
"""


class AnchorRedirectsTest(unittest.TestCase):
    def build(self, tmp):
        srcdir = Path(tmp, "src")
        outdir = Path(tmp, "out")
        srcdir.mkdir()
        (srcdir / "conf.py").write_text(CONF)
        (srcdir / "index.rst").write_text(INDEX)
        (srcdir / "old.rst").write_text(OLD)

        app = Sphinx(srcdir, srcdir, outdir, outdir / ".doctrees", "html", status=None)
        app.build()
        return outdir

    def test_js_is_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = self.build(tmp)

            old_page = (outdir / "old.html").read_text()
            self.assertIn(
                '<script id="python-docs-anchor-redirects"'
                ' type="application/json">'
                '{"removed-anchor": "index.html#new-home"}</script>',
                old_page,
            )
            self.assertIn('src="_static/anchor_redirects.js"', old_page)
            self.assertTrue((outdir / "_static" / "anchor_redirects.js").is_file())

            # Pages without an anchormap should not get the scripts.
            self.assertNotIn("anchor_redirects", (outdir / "index.html").read_text())


if __name__ == "__main__":
    unittest.main()
