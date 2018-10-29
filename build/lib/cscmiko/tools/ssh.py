from netmiko import ConnectHandler, NetmikoTimeoutError, NetMikoTimeoutException, \
    NetmikoAuthError, NetMikoAuthenticationException


class CiscoSDKSSHAuthenticationError(Exception):
    pass


class CiscoSDKSSHTimeoutError(Exception):
    pass


def _netmiko_connect(connection_dict):
    """
    to handel netmiko connection
    :param connection_dict: netmiko connection dict
    :return: netmiko connection object
    """
    try:
        connection = ConnectHandler(**connection_dict)

    except (NetMikoTimeoutException, NetmikoTimeoutError) as e:
        print(f"Time out while connecting to device {connection_dict['ip']}")
        raise CiscoSDKSSHTimeoutError(f"ERROR : Time out while connecting to device {connection_dict['ip']}")
    except (NetmikoAuthError, NetMikoAuthenticationException) as e:
        print(f"ERROR : ssh authentication failed to device {connection_dict['ip']}")
        raise CiscoSDKSSHAuthenticationError(f"SSH authentication failed to device {connection_dict['ip']}")
    return connection


class SSHManager:
    """
    SSH Context Manager
    """

    def __init__(self, connection_dict):

        self.conn_dict = connection_dict
        self.conn = self.connect()

    def __enter__(self):
        self.conn = self.connect()
        if not self.conn:
            return False
        return self

    def __exit__(self, *args):
        if not self.conn:
            return
        self.conn.disconnect()

    def disconnect(self):
        self.conn.disconnect()

    def connect(self):
        print(f"connecting to {self.conn_dict['ip']}")
        return _netmiko_connect(connection_dict=self.conn_dict)

    def save_config(self):
        self.conn.save_config()

    def send_commands_list(self, cmd):

        output = self.conn.send_config_set(cmd, strip_command=True)

        return output

    def get_command(self, cmd):
        try:
            output = self.conn.send_command(cmd, use_textfsm=True)
        except ValueError:
            raise ValueError(
                "invalid ~/ntc-templates/templates , please make sure to download download ntc-templates/templates from "
                "https://github.com/Ali-aqrabawi/cisco_sdk/templates and add templates dir to ~/ntc-templates/templates ")
        return output
