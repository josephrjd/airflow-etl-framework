"""

Sqoop query templates in dictionary

"""

sqoop_queries = {

"extract_and_load":

"""
# Init Kerberos
source ~/script/initKerberos.sh
# Run sqoop command
sqoop import --connect {% if params.step.source.connType == "mssql" %}'jdbc:jtds:sqlserver://{% endif %}{{ params.conn.host }}:{{ params.conn.port }}{% if params.step.source.collection %};database={{ params.step.source.collection }}{% endif %}' \
    {% if params.step.source.columnTransormation %}--map-column-java {{ params.step.source.columnTransormation }}{% endif %} \
    --table '{{ params.step.source.entity }}'{% if params.step.source.columns != "__all__" %} \
    --columns '{{ params.step.source.columns }}'{% endif %} \
    --connection-manager org.apache.sqoop.manager.SQLServerManager \
    --driver net.sourceforge.jtds.jdbc.Driver \
    --username '{{ params.conn.login }}' \
    --password '{{ params.conn.password }}' \
    --target-dir '{{ params.step.target.path }}{{ params.step.target.datasetName }}/{% if params.step.target.fileType=='parquetfile' %}part_{{ ds_nodash }}' --as-parquetfile{% else %}part={{ ds_nodash }}' --as-textfile{% endif %} \
"""

}
