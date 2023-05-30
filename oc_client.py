import kubernetes
import openshift.dynamic
import urllib3
import yaml


class OpenshiftClient:

    def __init__(self, config_path=None):
        urllib3.disable_warnings()
        if config_path is None:
            config_path = '~/.kube/config'
        self.client = openshift.dynamic.DynamicClient(kubernetes.config.new_client_from_config(config_path))

    def get_resource(self, kind):
        for res in self.client.resources.search():
            if res.kind == kind:
                return res

    def get_obj(self, kind, ns=None):
        if ns is None:
            return self.client.resources.get(kind=kind)
        res = self.get_resource(kind)
        man = self.client.get(res, namespace=ns)
        return man

    @staticmethod
    def extract_items(manifest):
        man = yaml.safe_load(manifest)
        if 'ResourceInstance' in list(man.keys())[0]:
            man = man[list(man.keys())[0]]['items']
        return man

    def read_and_write(self, kind, ns, target_path, split=True):
        obj = self.get_obj(kind, ns)
        mans = self.extract_items(obj)
        if not split:
            with open(f'{target_path}/{kind}', 'w') as file:
                file.write(yaml.safe_dump(mans))
                return

        for man in mans:
            with open(f'{target_path}/{man["metadata"]["name"]}') as file:
                file.write(yaml.safe_dump(man))


