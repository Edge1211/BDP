
A = load 'big_data/NY/*' using PigStorage('\t'); 
B = RANK A BY $1 DESC;                                                                                   
C = FOREACH B GENERATE $0, $1, $2;
DUMP C;