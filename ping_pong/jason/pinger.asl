
ended(0).
t_total(100).

!init.

+!init : t_total(T) <-
 for ( .range(I,1,T) ) {
        W = math.random(2);
        .send("ponger",achieve,pong(W));
    }
    .

@lm[atomic]
+!finished : ended(I) & t_total(T) & T > I + 1 <-
    -+ended(I+1).

+!finished <-
    Time = system.time;
    +end(Time);
    .save_agent("pinger-FINALSNAPSHOT.asl")
    .stopMAS.
