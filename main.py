from oc_client import OpenshiftClient
import os
import datetime
import yaml

exceptions = ['kube', 'openshift']
kinds = ['Template']

if __name__ == '__main__':
    client = OpenshiftClient()
    namespaces = [ns.metadata.name for ns in client.get_obj('Namespace').get().items]
    for exception in exceptions:
        namespaces = list(filter(lambda ns: not(ns.startswith(exception)), namespaces))
    timestamp = f'oc2dh_{datetime.datetime.now()}'
    os.mkdir(timestamp)
    for namespace in namespaces:
        # os.mkdir(f'{timestamp}/{namespace}')
        for kind in kinds:
            client.read_and_write(kind, ns=namespace, target_path=f'{timestamp}/{namespace}/{kind}')
        #     os.mkdir(f'{timestamp}/{namespace}/{kind}')
        #     obj = client.get_obj(kind, ns=namespace)
        #     with open(f'{timestamp}/{namespace}/{kind}/{obj}', 'w') as file:
        #         file.write(obj)

