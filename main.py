from oc_client import OpenshiftClient
from d8_client import DeckhouseClient
from converter import Converter
import os
import datetime

exceptions = ['kube', 'openshift']
kinds = ['Template', 'BuilderConfig', 'Builder']

if __name__ == '__main__':
    oc = OpenshiftClient()
    converter = Converter()
    d8 = DeckhouseClient()
    namespaces = [ns.metadata.name for ns in oc.get_obj('Namespace').get().items]
    for exception in exceptions:
        namespaces = list(filter(lambda ns: not(ns.startswith(exception)), namespaces))
    timestamp = f'oc2dh_{datetime.datetime.now()}'
    os.mkdir(timestamp)
    for namespace in namespaces:
        os.mkdir(f'{timestamp}/{namespace}')
        d8.create_namespace(namespace)
        for kind in kinds:
            os.mkdir(f'{timestamp}/{namespace}/{kind}')
            oc.read_and_write(kind, ns=namespace, target_path=f'{timestamp}/{namespace}/{kind}')
            print(f'{kind} from namespace {namespace} successfully received')
            converter.convert(
                f'{timestamp}/{namespace}/{kind}/openshift',
                f'{timestamp}/{namespace}/{kind}/deckhouse'
            )
            d8.apply_helm_chart(path=f'{timestamp}/{namespace}/{kind}', ns=namespace)
            print(f'Helm-charts successfully applied to namespace {namespace}')
