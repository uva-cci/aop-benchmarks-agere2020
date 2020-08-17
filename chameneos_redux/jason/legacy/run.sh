# uncomment the following echos to setup the runs of the experiment
#
#echo 'run(a,[blue, red, yellow], 600).' > runs.asl
#echo 'run(b,[blue, red, yellow, red, yellow, blue, red, yellow, red, blue], 6000).' >> runs.asl

java -cp ../../lib/jason.jar:bin/classes jason.infra.centralised.RunCentralisedMAS chameneos.mas2j
