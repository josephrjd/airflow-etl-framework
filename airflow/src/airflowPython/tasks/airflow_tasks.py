"""

Class which holds all types of tasks in airflow

"""

import logging
from airflow.exceptions import AirflowException
from airflowPython.tasks.vertica_tasks import VerticaTask
from airflowPython.tasks.shell_script_task import ShellScriptTask
from airflowPython.tasks.sqoop_tasks import SqoopTask


class TaskGenerator():

    def __init__(self, dag):
        self.dag = dag

        self.taskClass = {
            "vertica": VerticaTask,
            "sqoop": SqoopTask,
            "shell_script": ShellScriptTask,
        }

    def generateTask(self, step):
        try:
            cls = self.taskClass[step["runtime"]["task"]](self.dag)
            return cls.generateTask(step)

        except Exception as e:
            message = "Error while creating task | "
            logging.error(message)
            raise AirflowException(message + str(e))
