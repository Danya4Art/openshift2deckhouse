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
            print(f'File values created {target}/values.yaml')
        with self.open(f'{target}/Chart.yaml', 'w') as output:
            chart = {
                'name': man['metadata']['name'],
                'version': '0.1.0'
            }
            annotations_keys = ['description', 'tags']
            annotations = man['metadata']['annotations']
            for k in annotations_keys:
                if k in annotations:
                    chart[k] = annotations[k]
            yaml.safe_dump(chart, output, default_style=None, default_flow_style=False)
            print(f'File values created {target}/Chart.yaml')
        for obj in man['objects']:
            t = obj['kind']
            n = obj['metadata']['name']
            converted = self._convert(obj)
            with self.open(f'{target}/templates/{t}.yaml', 'w+') as output:
                output.write(converted)
                print(f'Converted manifest to helm chart {target}/templates/{t}.yaml')

    def _convert(self, manifest: [list | dict]):
        manifest['apiVersion'] = 'v1'
        if manifest['kind'] == 'DeploymentConfig':
            manifest['kind'] = 'Deployment'
        converted = re.sub(pattern, self.change_var_template, yaml.safe_dump(manifest))
        return converted

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


if __name__ == '__main__':
    c = Converter()
    c.convert(
        '/home/daniil/PycharmProjects/ModuleOKD/openshift2deckhouse/example/nginx-template.yaml',
        '/home/daniil/PycharmProjects/ModuleOKD/examples'
    )
