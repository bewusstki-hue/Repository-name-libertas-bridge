"""Tests für MeshSync — Persistenz, Suche, Broadcast."""

import sys
import os
import json
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from libertas_shield.mesh_sync import MeshSync


class TestMeshSync(unittest.TestCase):
    def setUp(self):
        # Isoliertes temporäres Verzeichnis für jeden Test
        self.tmpdir = tempfile.mkdtemp()
        self._orig_dir = os.getcwd()
        os.chdir(self.tmpdir)
        self.mesh = MeshSync()

    def tearDown(self):
        os.chdir(self._orig_dir)

    def test_add_and_list(self):
        self.mesh.add_knowledge("Python", "Eine Programmiersprache")
        topics = self.mesh.list_topics()
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0][1], "Python")

    def test_persistence(self):
        self.mesh.add_knowledge("Test", "Inhalt")
        mesh2 = MeshSync()
        topics = mesh2.list_topics()
        self.assertEqual(len(topics), 1)

    def test_search_by_topic(self):
        self.mesh.add_knowledge("Datenschutz", "DSGVO Grundlagen")
        results = self.mesh.get_knowledge("datenschutz")
        self.assertEqual(len(results), 1)

    def test_search_by_content(self):
        self.mesh.add_knowledge("Recht", "DSGVO ist wichtig")
        results = self.mesh.get_knowledge("DSGVO")
        self.assertEqual(len(results), 1)

    def test_search_no_match(self):
        self.mesh.add_knowledge("Python", "Programmiersprache")
        results = self.mesh.get_knowledge("Java")
        self.assertEqual(len(results), 0)

    def test_remove_knowledge(self):
        eid = self.mesh.add_knowledge("Zu löschen", "Inhalt")
        removed = self.mesh.remove_knowledge(eid)
        self.assertTrue(removed)
        self.assertEqual(len(self.mesh.knowledge_base), 0)

    def test_remove_nonexistent(self):
        removed = self.mesh.remove_knowledge("nonexistent")
        self.assertFalse(removed)

    def test_broadcast_creates_file(self):
        self.mesh.add_knowledge("Test", "Broadcast")
        export_file = self.mesh.broadcast_knowledge()
        self.assertIsNotNone(export_file)
        self.assertTrue(os.path.exists(export_file))
        with open(export_file) as f:
            data = json.load(f)
        self.assertIn("entries", data)
        self.assertIn("node", data)

    def test_broadcast_empty_returns_none(self):
        result = self.mesh.broadcast_knowledge()
        self.assertIsNone(result)

    def test_import_broadcast(self):
        self.mesh.add_knowledge("Import-Test", "Inhalt")
        export_file = self.mesh.broadcast_knowledge()
        export_file_abs = os.path.abspath(export_file)

        # Neues, leeres Mesh in separatem Verzeichnis
        tmpdir2 = tempfile.mkdtemp()
        os.chdir(tmpdir2)
        mesh2 = MeshSync()
        imported = mesh2.import_broadcast(export_file_abs)
        os.chdir(self.tmpdir)
        self.assertEqual(imported, 1)
        self.assertEqual(len(mesh2.knowledge_base), 1)

    def test_import_no_duplicates(self):
        self.mesh.add_knowledge("Doppelt", "Inhalt")
        export_file = self.mesh.broadcast_knowledge()
        imported = self.mesh.import_broadcast(export_file)
        self.assertEqual(imported, 0)

    def test_node_id_is_string(self):
        self.assertIsInstance(self.mesh.node_id, str)
        self.assertEqual(len(self.mesh.node_id), 8)


if __name__ == "__main__":
    unittest.main()
