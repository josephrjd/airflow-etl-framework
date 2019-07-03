"""

Class which holds sqoop task generator

"""

from jinja2 import Template
from airflow.hooks.base_hook import BaseHook
from templates.sqoop_queries import sqoop_queries
from airflow.contrib.operators.ssh_operator import SSHOperator

class SqoopTask():

    def __init__(self, dag):
        self.dag = dag

    def generateTask(self, step):

        if (step.get("jinjaInTaskParam", False)):
            rendered = Template(sqoop_queries[step["type"]]).render(params={"step": step})
        else:
            rendered = sqoop_queries[step["type"]]

        conn = BaseHook._get_connections_from_db(step["source"]["connId"])[0]
        connection_details = conn

        # Getting decrypted password
        connection_details.password = conn.get_password()

        task = SSHOperator(
            task_id=step["stepId"],
            ssh_conn_id=step["runtime"]["connId"],
            command=rendered,
            params={
                "step": step,
                "conn": connection_details
            },
            dag=self.dag
        )

        return task
