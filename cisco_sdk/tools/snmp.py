from easysnmp import Session
from collections import defaultdict

class snmp_manager:

    def __init__(self, hostname, community):
        self.snmp = Session(hostname=hostname, community=community, version=2,use_sprint_value=True)

    def get_fields(self, **kwargs):

        inner_res = defaultdict(dict)
        for key in kwargs:
            res = self.snmp.walk(oids=kwargs[key])
            for item in res :

                if 'ipAdEntIfIndex' in item.oid :
                    print(item)
                    inner_res[item.value].update({key:item.oid_index})

                else :
                    inner_res[item.oid_index].update({key:item.value})

        return dict(inner_res)