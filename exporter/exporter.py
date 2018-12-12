import argparse
import json
import logging
import os

from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client.twisted import MetricsResource
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

logger = logging.getLogger(__name__)

SHA256_PREFIX_LENGTH = len('sha256:')


class RegistryCollector:
    def __init__(self, base_path):
        self._base_path = base_path

    def _find_repositories(self):
        repositories = []
        for dirname, dirnames, filenames in os.walk(os.path.join(self._base_path, 'repositories')):
            if '_manifests' in dirnames:
                repositories.append(dirname.replace(os.path.join(self._base_path, 'repositories'), '')[1:])

            # Don't need to recurse any further
            for terminaldirname in ['_manifests', '_layers', '_uploads']:
                if terminaldirname in dirnames:
                    dirnames.remove(terminaldirname)

        return repositories

    def _scrape_tags(self, repository):
        tags_path = os.path.join(self._base_path, 'repositories', repository, '_manifests', 'tags')
        return os.listdir(tags_path)

    def _scrape_revisions(self, repository):
        tags_path = os.path.join(self._base_path, 'repositories', repository, '_manifests', 'revisions', 'sha256')
        return os.listdir(tags_path)

    def _scrape_manifest(self, repository, tag):
        tags_path = os.path.join(self._base_path, 'repositories', repository, '_manifests', 'tags')

        with open(os.path.join(tags_path, tag, 'current', 'link'), 'r') as link_file:
            manifest_id = link_file.readline()[SHA256_PREFIX_LENGTH:].replace('\n', '')
        with open(os.path.join(self._base_path, 'blobs', 'sha256', manifest_id[0:2], manifest_id, 'data'),
                  'r') as manifest_file:
            return json.load(manifest_file)

    def collect(self):
        repository_tags_total = GaugeMetricFamily('repository_tags_total', 'Number of tags for each repo',
                                                  labels=['repository'])
        repository_revisions_total = GaugeMetricFamily('repository_revisions_total',
                                                       'Number of revisions for each repo', labels=['repository'])
        repository_tag_layers_total = GaugeMetricFamily('repository_tag_layers_total', 'Number of layers in each tag',
                                                        labels=['repository', 'tag'])
        repository_tag_size_bytes = GaugeMetricFamily('repository_tag_size_bytes', 'Size of each tag',
                                                      labels=['repository', 'tag'])

        repositories = self._find_repositories()

        logger.debug('Found %s repositories: %s', len(repositories), repositories)

        for repository in repositories:
            logger.debug('Scanning %s for tags', repository)
            tags = self._scrape_tags(repository)
            repository_tags_total.add_metric([repository], len(tags))
            revisions = self._scrape_revisions(repository)
            repository_revisions_total.add_metric([repository], len(revisions))
            for tag in tags:
                manifest = self._scrape_manifest(repository, tag)
                repository_tag_layers_total.add_metric([repository, tag], len(manifest['layers']))
                size = 0
                for layer in manifest['layers']:
                    size += layer['size'] if 'size' in layer else 0
                repository_tag_size_bytes.add_metric([repository, tag], size)

        yield repository_tags_total
        yield repository_revisions_total
        yield repository_tag_layers_total
        yield repository_tag_size_bytes


def run_metrics_server():
    root = Resource()
    root.putChild(b'metrics', MetricsResource())

    factory = Site(root)
    reactor.listenTCP(8080, factory)
    reactor.run()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Exports statistics from a private Docker registry')
    parser.add_argument('path', help='File path to root of registry disk (eg. /var/lib/registry/docker/registry/v2/).' +
                        ' This directory should contain subdirectories "repositories" and "blobs"')
    args = parser.parse_args()

    collector = RegistryCollector(args.path)
    REGISTRY.register(collector)

    run_metrics_server()
