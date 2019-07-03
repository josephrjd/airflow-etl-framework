"""

Class which holds vertica task generator

"""

from jinja2 import Template
from templates.vertica_sql import vertica_sql
from airflow.operators.vsql_plugin import VSQLOperator

class VerticaTask():

    def __init__(self, dag):
        self.dag = dag

    def generateTask(self, step):

        if (step.get("jinjaInTaskParam", False)):
            rendered = Template(vertica_sql[step["type"]]).render(params={"step": step})
        else:
            rendered = vertica_sql[step["type"]]

        task = VSQLOperator(
            task_id=step["stepId"],
            sql=rendered,
            conn_id=step["runtime"]["connId"],
            params={
                "step": step
            },
            dag=self.dag
        )

        return task
