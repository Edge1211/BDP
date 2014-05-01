    # -input "/projects/trending/test/201311210800.bz2/*/part*" \
#!/bin/sh
# -D mapred.output.compress=true \    
#  -D mapred.output.compression.type=gzip \                                                                                                
#  -D mapred.output.compression.codec=org.apache.hadoop.io.compress.GzipCodec \

$HADOOP_PREFIX/bin/hadoop jar /home/gs/hadoop/current/share/hadoop/tools/lib/hadoop-streaming.jar \
    -D mapred.job.queue.name=search_general \
    -D mapred.map.tasks.speculative.execution=true  \
    -D mapred.reduce.tasks.speculative.execution=true \
    -D mapred.task.timeout=6000000  \
    -D mapred.reduce.tasks=5 \
    -D mapred.job.reduce.memory.mb=3072 \
    -D mapred.job.name="countSkills" \
    -D dfs.umask=0 \
    -D mapreduce.job.acl-view-job="*" \
    -files /homes/xuhe/big_data/project/countSkills.py \
    -mapper "python countSkills.py Map" \
    -reducer "python countSkills.py Reduce" \
    -input "big_data/project/1-s*" \
    -output "big_data/project/result"


#    -libjars MT.jar \
#    -files ./qsFeature_quFeature_build.py,/homes/chihoon/sap/norm_west_europe.py,/homes/chihoon/sap/utils.py,/homes/chihoon/sap/shellwords.py,/homes/chihoon/sap/runexternal.py \
#    -outputformat Mystreaming.MTout.MTout  \
