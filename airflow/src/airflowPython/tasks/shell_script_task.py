"""

Class which holds shell task generator

"""

from jinja2 import Template
from templates.shell_scripts import shell_scripts
from airflow.contrib.operators.ssh_operator import SSHOperator

class ShellScriptTask():

    def __init__(self, dag):
        self.dag = dag

    def generateTask(self, step):

        if (step.get("jinjaInTaskParam", False)):
            rendered = Template(shell_scripts[step["type"]]).render(params={"step": step})
        else:
            rendered = shell_scripts[step["type"]]

        task = SSHOperator(
            task_id=step["stepId"],
            ssh_conn_id=step["runtime"]["connId"],
            command=rendered,
            params={
                "step": step
            },
            dag=self.dag
        )

        return task
