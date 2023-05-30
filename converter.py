import yaml
import re
import os

pattern = r'\$\{(?P<var>\w+)\}'


class Converter:
    def convert(self, source, target):
        man = None
        with open(source, 'r') as input:
            man = yaml.safe_load(input)
        with self.open(f'{target}/values.yaml', 'w') as output:
            params = {}
            for param in man['parameters']:
                params[param['name'].lower()] = param['value']
            yaml.safe_dump(params, output, default_style=None, default_flow_style=False)
        converted = self._convert(man.copy())
        for obj in converted['objects']:
            t = obj['kind']
            with self.open(f'{target}/{t}.yaml', 'w+') as output:
                yaml.safe_dump(obj, output, default_flow_style=False, indent=2)

    def _convert(self, manifest: [list | dict]):
        for k, v in enumerate(manifest) if isinstance(manifest, list) else manifest.items():
            if isinstance(v, dict) or isinstance(v, list):
                manifest[k] = self._convert(v)
            else:
                # print(v, type(v))
                if isinstance(v, str) and re.search(pattern, v):
                    manifest[k] = re.sub(pattern, self.change_var_template, v)
        return manifest

    @staticmethod
    def change_var_template(match_obj):
        template = '{{{{ .Values.{0} }}}}'
        return template.format(match_obj.group()[2:-1].lower())

    @staticmethod
    def open(path, *args, **kwargs):
        pardir = os.path.dirname(path)
        if not os.path.exists(pardir):
            os.mkdir(pardir)
        return open(path, *args, **kwargs)

