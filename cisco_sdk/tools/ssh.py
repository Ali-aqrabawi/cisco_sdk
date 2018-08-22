from netmiko import ConnectHandler, NetmikoTimeoutError, NetMikoTimeoutException, \
    NetmikoAuthError,NetMikoAuthenticationException

def netmiko_connect(connection_dict):
    try:
        connection = ConnectHandler(**connection_dict)

    except (NetMikoTimeoutException, NetmikoTimeoutError) as e:
        print(f"Time out while connecting to device {connection_dict['ip']}")
        return False
    except (NetmikoAuthError, NetMikoAuthenticationException) as e:
        print(f"ssh authentication failed to device {connection_dict['ip']}")
        return False
    return connection


class SSHManager():
    """
    SSH Context Manager
    """

    def __init__(self,connection_dict):

        self.conn_dict = connection_dict

    def __enter__(self):
        self.conn = self.connect()
        if not self.conn:
            return False
        return self

    def __exit__(self,*args):
        self.conn.disconnect()


    def connect(self):
        print(f"connecting to {self.conn_dict['ip']}")
        return netmiko_connect(connection_dict=self.conn_dict)

    def send_command(self,cmd):

        try:
            output = self.conn.send_config_set(cmd, strip_command=True)

        except Exception as e:

            return False
        return output

    def get_command(self,cmd):
        output = self.conn.send_command(cmd,use_textfsm=True)
        return output