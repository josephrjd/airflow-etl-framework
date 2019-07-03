"""

Shell scripts templates in dictionary

"""

shell_scripts = {

"copy_from_s3_to_hdfs_without_keys":

"""
~/script/copyFromS3ToHdfsWithoutKeys.sh --hdfs_path {{ params.step.target.path }} --local_folder /tmp/{{ params.step.target.datasetName }}/landing --s3_path {{ params.step.source.collection }}{{ params.step.source.entity }} --file_regex {{ params.step.source.fileRegex }}
""",

}
