from cisco_sdk.snmp_helper.standard_oids import interface_oids
from cisco_sdk.tools.ssh import SSHManager

class CiscoDevice:

    def __init__(self, host, username, password):
        self.connection_dict = {
            "device_type": self.device_type,
            "ip": host,
            "username": username,
            "password": password
        }
    def get_command(self, command):
        with SSHManager(self.connection_dict) as conn:
            return conn.get_command(command) or False

    def reboot(self):
        pass

    def ping(self, ip):
        out = self.get_command(f"ping {ip}")
        if 'Success rate is 0' in out:
            return False
        return True

    def traceroute(self, ip):
        pass

    def backup(self, file):
        pass

    def restore(self, file):
        pass

    def get_sysname(self):
        pass

    def get_version(self):
        pass

    def get_sysuptime(self):
        pass

    def get_cdp_neighbors(self):
        pass

