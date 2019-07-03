"""

Vertica SQL templates in dictionary

"""

vertica_sql = {

"insert_data_load":

"""
INSERT INTO {{ params.step.target.collection }}.{{ params.step.target.entity }} {% if params.step.target.columns != "__all__" %}({{ params.step.target.columns }}){% endif %}
SELECT {% if params.step.source.columns != "__all__" %}{{ params.step.source.columns }}{% else %}*{% endif %} FROM {{ params.step.source.collection }}.{{ params.step.source.entity }};
COMMIT;
""",

"truncate_and_load_from_hdfs":

"""
TRUNCATE TABLE {{ params.step.target.collection }}.{{ params.step.target.entity }};
COPY {{ params.step.target.collection }}.{{ params.step.target.entity }}{% if not params.step.mapping.auto %} ({% for column in params.step.mapping.columnMappings %}{{ column.targetField }}{% if not loop.last %}, {% endif %}{% endfor %}){% endif %}
FROM 'hdfs://maf{{ params.step.source.path }}{{ params.step.source.datasetName }}{% if params.step.source.fileType == 'parquetfile' %}/part_{{ ds_nodash }}/*.parquet' PARQUET{% else %}/part={{ ds_nodash }}/{{ params.step.target.fileRegex }}'{% endif %}
{% if "rejectedData" in params.step.target %}REJECTED DATA AS TABLE {{ params.step.target.rejectedData.collection }}.{{ params.step.target.rejectedData.entity }}{% endif %}
{% if params.step.source.fileType != 'parquetfile' %} DELIMITER '{{ params.step.source.fileSeparator }}'
ENCLOSED BY '{{ params.step.source.fileEnclosedBy }}'
{% if params.step.source.fileHeader %}SKIP 1{% endif %} DIRECT{% endif %};
COMMIT;
""",

"scd2_load":
"""
-- Update for history
UPDATE {{ params.step.target.collection }}.{{ params.step.target.entity }}
SET active_flag=0, valid_to=(now()-1)::date
WHERE {{ params.step.target.hashPrefix }}_hash_id in (
    SELECT DISTINCT t.{{ params.step.target.hashPrefix }}_hash_id
    FROM {{ params.step.target.collection }}.{{ params.step.target.entity }} t
    JOIN {{ params.step.source.collection }}.{{ params.step.source.entity }} s
        ON t.{{ params.step.target.hashPrefix }}_hash_id=s.{{ params.step.source.hashPrefix }}_hash_id 
        AND t.{{ params.step.target.hashPrefix }}_hash_scd!=s.{{ params.step.source.hashPrefix }}_hash_scd
        AND t.active_flag = 1 
) AND active_flag = 1;

-- Insert for updates and new values
INSERT INTO {{ params.step.target.collection }}.{{ params.step.target.entity }}
    ({{ params.step.target.columns }}, 
    {{ params.step.target.hashPrefix }}_hash_id, {{ params.step.target.hashPrefix }}_hash_scd, file_name, processing_date, valid_from, valid_to, active_flag)
SELECT {{ params.step.source.columns }}, 
    {{ params.step.target.hashPrefix }}_hash_id, {{ params.step.target.hashPrefix }}_hash_scd, file_name, processing_date, now()::date, '9999-12-31'::date, 1
FROM  {{ params.step.source.collection }}.{{ params.step.source.entity }}
WHERE {{ params.step.source.hashPrefix }}_hash_id NOT IN (
    SELECT {{ params.step.target.hashPrefix }}_hash_id
    FROM {{ params.step.target.collection }}.{{ params.step.target.entity }}
    where active_flag=1
);
COMMIT;
""",

"fact_incremental_load":

"""
-- Deleting updated records
DELETE FROM {{ params.step.target.collection }}.{{ params.step.target.entity }}
WHERE {{ params.step.target.hashPrefix }}_hash_id IN (
    SELECT {{ params.step.source.hashPrefix }}_hash_id
    FROM {{ params.step.source.collection }}.{{ params.step.source.entity }}
);

-- Inserting incoming records
INSERT INTO {{ params.step.target.collection }}.{{ params.step.target.entity }}{% if params.step.target.columns != "__all__" %}({{ params.step.source.columns }}){% endif %}
SELECT {% if params.step.source.columns != "__all__" %}{{ params.step.source.columns }}{% else %}*{% endif %}
FROM {{ params.step.source.collection }}.{{ params.step.source.entity }};

COMMIT;
""",

"tuncate_and_load_raw_to_flex":

"""
TRUNCATE TABLE {{ params.step.target.collection }}.{{ params.step.target.entity }}; 
COPY {{ params.step.target.collection }}.{{ params.step.target.entity }} {% if params.step.target.columns != "__all__" %}({{ params.step.target.columns }}){% endif %}
FROM 'hdfs://maf{{ params.step.source.path }}/{{ params.step.source.fileRegex }}' 
PARSER fjsonparser(flatten_maps=False, flatten_arrays=False);
COMMIT;
"""
}
