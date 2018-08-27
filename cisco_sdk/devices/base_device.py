from cisco_sdk.tools.ssh import SSHManager
from cisco_sdk.tools.config import check_config_result
from cisco_sdk.features.base_component import FeatureSet


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

    def get_command_output(self, command):
        """
        get output of command from device ,
        :param command:
        :return: list of dict or false if connection failed .
        """
        with SSHManager(self.connection_dict) as conn:
            if not conn:
                return False
            return conn.get_command(command)

    def send_commands_config(self, cmds, save):
        """
        send config commands to device
        :param cmds: list: commands strings
        :return: str: execution output
        """
        with SSHManager(self.connection_dict) as conn:
            if not conn:
                return False
            output = conn.send_commands_list(cmds)
            if save:
                conn.save_config()
            return output

    def _get_all_cmds(self):
        """try:
        return all cmds added to all self.FeatureSet , and return them
        :return: list of all added commands on that device
        """
        results = []
        for name, obj in vars(self).items():
            if isinstance(obj, FeatureSet):
                results += obj.cmds
        return results

    def commit(self, save=False):
        """
        commit config changes to device,
        :return: (is_ok,err_msg): is_ok is bool() , err_msg is str()
        """
        # get all config changes and set them
        all_cmds = self._get_all_cmds()
        if not all_cmds:
            return False, "No changes to commit"
        # execute the commands
        output = self.send_commands_config(all_cmds, save)
        if not output:
            return False, "Connection to device failed"
        return check_config_result(output)

    def save(self):
        with SSHManager(self.connection_dict) as conn:
            if not conn:
                return False
            conn.save_config()

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
        out = self.get_command_output(f"ping {ip}")
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
