"""

Dags gets generated here

"""

import json
import glob
import logging
from airflow.models import DAG
from airflow import configuration
from datetime import datetime, timedelta
from airflow.exceptions import AirflowException
from airflowPython.tasks.airflow_tasks import TaskGenerator


# Setting directory path for reading json
directoryPath = "/usr/local/airflow/etlConfig/"

def get_jobs():
    """Get dynamic DAGs configuration by glob pattern."""
    for file in glob.glob(directoryPath + '*.json'):
        logging.info(f"Found JSON at '{file}'")
        with open(file, 'r') as f:
            dag_config = json.load(f)
        yield dag_config

def dag_generator():
    try:
        for job in get_jobs():

            # Defining default args for all the dags
            # TODO
            # 1. get retry_delay from json
            default_args = {
                'owner': job.get("owner", "airflow"),
                'depends_on_past': job.get("dependsOnPast", False),
                'start_date': datetime(2015, 6, 1),
                'email': job.get("emails", ['the_grid@mafia.com']),
                'email_on_failure': job.get("emailOnFailure", True),
                'email_on_retry': job.get("emailOnRetry", True),
                'retries': job.get("numberOfRetries", 1),
                'retry_delay': timedelta(minutes=5)
            }

            dag = DAG(
                job["dagId"],
                default_args=default_args,
                description=job["description"],
                schedule_interval=job["schedule"],
                start_date=datetime.strptime(job["startDate"], job.get("dateFormat", "%Y-%m-%d")),
                catchup=job.get("catchup", False),
                max_active_runs=job.get("maxActiveDagRuns",
                                        configuration.conf.getint('core', 'max_active_runs_per_dag'))

            )

            # Initializing task generator
            task_generator = TaskGenerator(dag)

            # Tasks dictionary will hold all tasks with task id as key
            tasks = {}

            # Generate tasks
            for step in job["steps"]:
                tasks[step["stepId"]] = task_generator.generateTask(step)

            # Create DAG flow for tasks
            for step in job["steps"]:
                currentTask = tasks[step["stepId"]]

                if step.get("runAfter", None) is not None:
                    for beforeTaskId in step.get("runAfter"):
                        beforeTask = tasks[beforeTaskId]

                        # Creating link
                        beforeTask.set_downstream(currentTask)

            # Passing the dag to global scope
            globals()[job["dagId"]] = dag

    except Exception as e:
        message = "Unable to create dag "
        logging.error(message)
        raise AirflowException(message + str(e))


dag_generator()
