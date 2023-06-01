from kubernetes import client, config
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

    def install_helm_chart(self, path, ns):
        exec(f"helm install {path}/ --values {path}/values.yaml --namespace {ns}")
