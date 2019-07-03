"""Operator for vsql client"""

import logging
from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
from plugins.vsql_plugin.hook import VSQLHook

log = logging.getLogger(__name__)

class VSQLOperator(BaseOperator):
    """vsql operator for Vertica"""

    template_fields = ('sql', )
    template_ext = ('.sql',)
    ui_color = '#F2A7A7'

    @apply_defaults
    def __init__(self, sql: str, conn_id: str, *args, **kwargs):
        """Initialization

        :param sql: SQL query to be executed
        :param conn_id: Connection id of vertica to be used
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.sql = sql
        self.conn_id = conn_id

    def execute(self, context: dict):
        """Execute vsql command

        :param context: DAG execution context
        :return: None
        """
        self.hook = VSQLHook(
            sql=self.sql,
            conn_id=self.conn_id
        )

        self.hook.run_cmd()

class VSQLPlugin(AirflowPlugin):
    name = 'vsql_plugin'
    operators = [VSQLOperator]
    hooks = [VSQLHook]
