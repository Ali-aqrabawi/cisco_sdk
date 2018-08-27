# """
# SNMP tools
# """
#
# from easysnmp import Session
# from collections import defaultdict
#
#
# class SNMPManager:
#     """
#     snmp manager , take hostname and community and return dict of results
#     example :
#     snmp_client = SNMPManager('192.168.1.1','private')
#     interfaces = snmp_client.get_fields(name='ifName',mtu='mtu',admin_status='ifAdminStatus')
#     interfaces will equal to ; {'oid_index':'11', 'name':'Ethernet1/0', 'mtu':'1500', 'admin_status':'up'}
#     """
#
#     def __init__(self, hostname, community):
#         self.snmp = Session(hostname=hostname, community=community, version=2, use_sprint_value=True)
#
#     def get_fields(self, **kwargs):
#         """
#         method takes kwargs of field_name and oid name (name='ifName',mtu='mtu',admin_status='ifAdminStatus')
#         :param kwargs: field_name and it's oid name
#         :return: dict: {'oid_index':'11', 'name':'Ethernet1/0', 'mtu':'1500', 'admin_status':'up'}
#         """
#
#         inner_res = defaultdict(dict)
#         for key in kwargs:
#             res = self.snmp.walk(oids=kwargs[key])
#             for item in res:
#
#                 if 'ipAdEntIfIndex' in item.oid:
#                     print(item)
#                     inner_res[item.value].update({key: item.oid_index})
#
#                 else:
#                     inner_res[item.oid_index].update({key: item.value})
#
#         return dict(inner_res)
