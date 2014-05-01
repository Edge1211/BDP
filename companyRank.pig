-- A = load 'data/1' using JsonLoader();
A = load 'big_data/project/data/*' using PigStorage('\t') AS (date:chararray, jobtitle:chararray, company:chararray, location:chararray, url:chararray);
B = GROUP A BY company;
C = FOREACH B GENERATE group, COUNT(B);
D = RANK C BY $1 DESC;
DUMP D;
