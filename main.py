from oc_client import OpenshiftClient
from d8_client import DeckhouseClient
import os
import datetime

exceptions = ['kube', 'openshift']
kinds = ['Template', 'BuilderConfig', 'Builder']

if __name__ == '__main__':
    oc = OpenshiftClient()
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
            oc.read_and_write(kind, ns=namespace, target_path=f'{timestamp}/{namespace}/{kind}')
            d8.apply_helm_chart(path=f'{timestamp}/{namespace}/{kind}', ns=namespace)
