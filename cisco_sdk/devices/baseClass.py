from cisco_sdk.tools.ssh import SSHManager


class CiscoDevice(object):
    """
    base class for cisco Device managers,
    """

    def __init__(self, host, username, password):
        self.connection_dict = {
            "device_type": self.device_type,
            "ip": host,
            "username": username,
            "password": password
        }

    def get_command(self, command):
        """
        get output of command from device ,
        :param command:
        :return: list of dict or false if connection failed .
        """
        with SSHManager(self.connection_dict) as conn:
            return conn.get_command(command) or False

    def reboot(self):
        """
        reboot the device
        :return:
        """
        pass

    def ping(self, ip):
        """
        ping an ip address from the device
        :param ip:
        :return: bool
        """
        out = self.get_command(f"ping {ip}")
        if 'Success rate is 0' in out:
            return False
        return True

    def traceroute(self, ip):
        pass

    def backup(self, file):
        """
        take backup from device and stor it in file location
        :param file:
        :return:
        """
        pass

    def restore(self, file):
        """
        retore config on device from the given fie
        :param file:
        :return:
        """
        pass

    def get_sysname(self):
        """
        get host name
        :return:
        """
        pass

    def get_version(self):
        pass

    def get_sysuptime(self):
        pass
