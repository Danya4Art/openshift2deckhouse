import yaml
import re

pattern = r'\$\{(?P<var>\w+)\}'


class Converter:

    # def __init__(self, config_path=None):
    #     urllib3.disable_warnings()
    #     if config_path is None:
    #         config_path = '~/.kube/config'
    #     self.client = openshift.dynamic.DynamicClient(kubernetes.config.new_client_from_config(config_path))

    def convert(self, source, target):
        man = None
        with open(source, 'r') as input:
            man = yaml.safe_load(input)
        converted = self._convert(man)
        with open(f'{target}/values', 'w') as output:
            output


    def _convert(self, manifest: dict):
        changes = set()
        manifest = dict()
        for v in manifest.values():
            if isinstance(v, dict):
                res = self._convert(v)
                changes = changes.union(res['changes'])
                manifest = res['manifest']
            elif match := re.findall(pattern, v):
                v = re.sub(pattern, self.change_var_template, v)


        return {'changes': changes, 'manifest': manifest}

    @staticmethod
    def change_var_template(match_obj):
        return '{{ .Values.' + match_obj.group()[2:-1].lower() + ' }}'
