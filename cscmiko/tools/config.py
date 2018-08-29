import re
import os
from jinja2 import Environment, FileSystemLoader

def clean(x):
    def remove(x):
        string = x.strip(" ")
        return string
    return list(filter(None,map(remove,x)))

def check_config_result(output):
    """
    take the output result of executed commands on the device and check if any commands has failed
    :param output: str: result of executed commands
    :return: tuple: Bool,str: True if no errors found , str is the err_msg
    """
    print("Validating config execution")
    err_lines = []
    output = output.strip('config term')
    output = output.strip('Enter configuration commands, one per line.  End with CNTL/Z.')
    output_lines = output.splitlines()
    # Remove the empty lines
    output_lines = list(filter(None, output_lines))

    # Extract the Errors and warnings
    for line in output_lines:
        f = re.match(".*#", line)
        if not f:
            err_lines.append(line)

    # Classify errors and warnnings
    for err in err_lines:

        if "^" in err:
            print("Config failed , reason = syntax error ")

            return False, "internal error, (wrong syntax)"

        if 'ERROR' in err:
            print(f"config failed, reason = {err}")
            return False, err



    return True, err_lines


def render_command(template_name, variables):
    """
    render commands and return list of rendered cmds

    :param template_name: jinja template name
    :param variables: command variables
    :return: cmd: list of rendered commands
    """
    # get cisco_sdk/ path
    PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
    TEMPLATES_DIR = os.path.join(PROJECT_DIR, "features/configuration_templates")
    # render the jinja2 template from a string
    env = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_DIR))

    template = env.get_template(template_name)

    cmd = template.render(**variables)
    cmd = cmd.split('\n')


    return clean(cmd)
