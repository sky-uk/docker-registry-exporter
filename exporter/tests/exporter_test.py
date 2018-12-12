import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from exporter import RegistryCollector


class RegistryCollectorTest(unittest.TestCase):
    def test_repository_with_no_tags(self):
        collector = RegistryCollector('any_path')
        collector._find_repositories = MagicMock(return_value=['repo-0'])
        collector._scrape_tags = MagicMock(return_value=[])
        collector._scrape_revisions = MagicMock(return_value=[])
        collector._scrape_manifest = MagicMock(return_value={'layers': []})

        metric_families = []
        for metric_family in collector.collect():
            metric_families.append(metric_family.name)
            if metric_family.name == 'repository_tags_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_revisions_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_tag_layers_total':
                self.assertEqual(metric_family.samples, [])
            if metric_family.name == 'repository_tag_size_bytes':
                self.assertEqual(metric_family.samples, [])

        collector._find_repositories.assert_called()
        collector._scrape_tags.assert_called_with('repo-0')
        collector._scrape_manifest.assert_not_called()
        self.assertEqual(metric_families, ['repository_tags_total', 'repository_revisions_total',
                                           'repository_tag_layers_total', 'repository_tag_size_bytes'])

    def test_repository_with_tag_but_no_layers(self):
        collector = RegistryCollector('any_path')
        collector._find_repositories = MagicMock(return_value=['repo-0'])
        collector._scrape_tags = MagicMock(return_value=['latest'])
        collector._scrape_revisions = MagicMock(return_value=[])
        collector._scrape_manifest = MagicMock(return_value={'layers': []})

        metric_families = []
        for metric_family in collector.collect():
            metric_families.append(metric_family.name)
            if metric_family.name == 'repository_tags_total':
                self.assertEqual(metric_family.samples[0].value, 1)
            if metric_family.name == 'repository_revisions_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_tag_layers_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_tag_size_bytes':
                self.assertEqual(metric_family.samples[0].value, 0)

        collector._find_repositories.assert_called()
        collector._scrape_tags.assert_called_with('repo-0')
        collector._scrape_manifest.assert_called_with('repo-0', 'latest')
        self.assertEqual(metric_families, ['repository_tags_total', 'repository_revisions_total',
                                           'repository_tag_layers_total', 'repository_tag_size_bytes'])

    def test_repository_with_tag_and_layers(self):
        collector = RegistryCollector('any_path')
        collector._find_repositories = MagicMock(return_value=['repo-0'])
        collector._scrape_tags = MagicMock(return_value=['latest'])
        collector._scrape_revisions = MagicMock(return_value=[])
        collector._scrape_manifest = MagicMock(return_value={'layers': [{'size': 10}, {'size': 5}]})

        metric_families = []
        for metric_family in collector.collect():
            metric_families.append(metric_family.name)
            if metric_family.name == 'repository_tags_total':
                self.assertEqual(metric_family.samples[0].value, 1)
            if metric_family.name == 'repository_revisions_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_tag_layers_total':
                self.assertEqual(metric_family.samples[0].value, 2)
            if metric_family.name == 'repository_tag_size_bytes':
                self.assertEqual(metric_family.samples[0].value, 15)

        collector._find_repositories.assert_called()
        collector._scrape_tags.assert_called_with('repo-0')
        collector._scrape_manifest.assert_called_with('repo-0', 'latest')
        self.assertEqual(metric_families, ['repository_tags_total', 'repository_revisions_total',
                                           'repository_tag_layers_total', 'repository_tag_size_bytes'])

    def test_repository_with_tag_and_layers_with_no_size(self):
        collector = RegistryCollector('any_path')
        collector._find_repositories = MagicMock(return_value=['repo-0'])
        collector._scrape_tags = MagicMock(return_value=['latest'])
        collector._scrape_revisions = MagicMock(return_value=[])
        collector._scrape_manifest = MagicMock(return_value={'layers': [{'size': 10}, {}]})

        metric_families = []
        for metric_family in collector.collect():
            metric_families.append(metric_family.name)
            if metric_family.name == 'repository_tags_total':
                self.assertEqual(metric_family.samples[0].value, 1)
            if metric_family.name == 'repository_revisions_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_tag_layers_total':
                self.assertEqual(metric_family.samples[0].value, 2)
            if metric_family.name == 'repository_tag_size_bytes':
                self.assertEqual(metric_family.samples[0].value, 10)

        collector._find_repositories.assert_called()
        collector._scrape_tags.assert_called_with('repo-0')
        collector._scrape_manifest.assert_called_with('repo-0', 'latest')
        self.assertEqual(metric_families, ['repository_tags_total', 'repository_revisions_total',
                                           'repository_tag_layers_total', 'repository_tag_size_bytes'])

    def test_repository_with_no_tags_but_revisions(self):
        collector = RegistryCollector('any_path')
        collector._find_repositories = MagicMock(return_value=['repo-0'])
        collector._scrape_tags = MagicMock(return_value=[])
        collector._scrape_revisions = MagicMock(return_value=['00000'])
        collector._scrape_manifest = MagicMock(return_value={'layers': []})

        metric_families = []
        for metric_family in collector.collect():
            metric_families.append(metric_family.name)
            if metric_family.name == 'repository_tags_total':
                self.assertEqual(metric_family.samples[0].value, 0)
            if metric_family.name == 'repository_revisions_total':
                self.assertEqual(metric_family.samples[0].value, 1)
            if metric_family.name == 'repository_tag_layers_total':
                self.assertEqual(metric_family.samples, [])
            if metric_family.name == 'repository_tag_size_bytes':
                self.assertEqual(metric_family.samples, [])

        collector._find_repositories.assert_called()
        collector._scrape_tags.assert_called_with('repo-0')
        collector._scrape_manifest.assert_not_called()
        self.assertEqual(metric_families, ['repository_tags_total', 'repository_revisions_total',
                                           'repository_tag_layers_total', 'repository_tag_size_bytes'])

    @patch("os.listdir")
    @patch("os.path.join")
    def test_scrape_tags_lists_directories(self, join_mock, listdir_mock):
        collector = RegistryCollector('any-path')
        join_mock.return_value = 'some-directory'
        listdir_mock.return_value = ['latest']

        self.assertEqual(collector._scrape_tags('some-repo'), ['latest'])

        join_mock.assert_called_with('any-path', 'repositories', 'some-repo', '_manifests', 'tags')
        listdir_mock.assert_called_with('some-directory')

    @patch("os.listdir")
    @patch("os.path.join")
    def test_scrape_revisions_lists_directories(self, join_mock, listdir_mock):
        collector = RegistryCollector('any-path')
        join_mock.return_value = 'some-directory'
        listdir_mock.return_value = ['0123456789']

        self.assertEqual(collector._scrape_revisions('some-repo'), ['0123456789'])

        join_mock.assert_called_with('any-path', 'repositories', 'some-repo', '_manifests', 'revisions', 'sha256')
        listdir_mock.assert_called_with('some-directory')

    @patch("os.walk")
    @patch("os.path.join")
    def test_find_repositories_traverses_directories(self, join_mock, walk_mock):
        collector = RegistryCollector('any-path')
        join_mock.return_value = 'some-directory'
        walk_mock.return_value = [('some-directory/repository', ['sub-repo'], []),
                                  ('some-directory/repository/sub-repo', ['_manifests', '_layers', '_uploads'], [])]

        self.assertEqual(collector._find_repositories(), ['repository/sub-repo'])

        walk_mock.assert_called_with('some-directory')
