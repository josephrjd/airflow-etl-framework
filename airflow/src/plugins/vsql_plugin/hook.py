"""
This module contains a vsql hook
"""
import subprocess
from copy import deepcopy
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook

class VSQLHook(BaseHook):

    def __init__(self, sql, conn_id='vrtica_default'):
        self.sql = sql
        self.conn = self.get_connection(conn_id)

    def cmd_mask_password(self, cmd_orig):
        cmd = deepcopy(cmd_orig)
        try:
            password_index = cmd.index('-w')
            cmd[password_index + 1] = 'XXXXXXXX'
        except ValueError:
            self.log.debug("No password in cmd")
        return cmd

    def _prepare_command(self):
        cmd = ["/opt/vertica/bin/vsql"]

        if self.conn.host:
            cmd += ["-h", self.conn.host]

        if self.conn.port:
            cmd += ["-p", str(self.conn.port)]

        if self.conn.login:
            cmd += ["-U", self.conn.login]

        if self.conn.password:
            cmd += ["-w", self.conn.password]

        if self.conn.extra_dejson:
            for key, value in self.conn.extra_dejson.items():
                cmd += ["{}".format(str(key))]
                if value:
                    cmd += [str(value)]

        cmd += ["-c {}".format(self.sql)]
        return cmd

    def Popen(self, cmd, **kwargs):
        """
        Remote Popen

        :param cmd: command to remotely execute
        :param kwargs: extra arguments to Popen (see subprocess.Popen)
        """

        masked_cmd = ' '.join(self.cmd_mask_password(cmd))
        self.log.info("Executing command: {}".format(masked_cmd))
        self.sp = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            **kwargs)

        for line in iter(self.sp.stdout):
            self.log.info(line.strip())

        self.sp.wait()

        self.log.info("Command exited with return code %s", self.sp.returncode)

        if self.sp.returncode:
            raise AirflowException("SQL command failed: {}".format(masked_cmd))


    def run_cmd(self):

        vsql_command = self._prepare_command()

        self.Popen(vsql_command)
