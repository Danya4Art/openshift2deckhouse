from kubernetes import client, config
from pyhelm.chartbuilder import ChartBuilder
import urllib3
import os


class OpenshiftClient:

    def __init__(self, config_path=None):
        urllib3.disable_warnings()
        config.load_kube_config('~/.kube/deckhouse.config')
        self.client = client.CoreV1Api()

    def create_namespace(self, name):
        namespaces = [item.metadata.name for item in self.client.list_namespace().items]
        if name not in namespaces:
            self.client.create_namespace(name)

    def apply_helm_chart(self, path, ns):
        for template in os.listdir(os.path.join(path, 'templates')):
            chart = ChartBuilder(template, )
