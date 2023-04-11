import yaml
import re

pattern = r'\$\{(?P<var>\w+)\}'


class Converter:

    def convert_template(self, source, target):
        with open(source, 'r') as input_file:
            template = yaml.safe_load(input_file)
        params = template.pop('parameters')
        new_params = list(map(lambda d: {d['name'].lower(): d['value']}, params))
        with open(f'{target}/values.yaml', 'w') as output_file:
            yaml.safe_dump(new_params, output_file, default_flow_style=False, explicit_start=True, allow_unicode=True)
        converted = self._convert(template['objects'])
        kinds = set(filter(lambda o: o['kind'], converted))
        for kind in kinds:
            with open(f'{target}/templates/{kind}.yaml', 'w') as output_file:
                objects = filter(lambda obj: obj['kind'] == kind, converted)
                yaml.safe_dump(objects, output_file, default_flow_style=False, explicit_start=True, allow_unicode=True)

    def _convert(self, manifest: dict = None):
        if manifest is None:
            manifest = {}
        for k, v in manifest.values():
            if isinstance(v, dict):
                manifest[k] = self._convert(v)
            elif re.search(pattern, v):
                manifest[k] = re.sub(pattern, self.change_var_template, v)
        return manifest

    @staticmethod
    def change_var_template(match_obj):
        return '{{ .Values.' + match_obj.group()[2:-1].lower() + ' }}'
