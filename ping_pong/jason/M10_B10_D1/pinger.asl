// parameters --
// number of matchs: 10
// number of balls: 10
// delay: 1

ended(0).
t_total(10).

!init.

+!init : t_total(T) & .my_name(M) &
             .delete("pinger", M, NS) &
             .concat("ponger", NS, N) <-
    Time = system.time;
    .print("start at: ", Time);
    for ( .range(I,1,T) ) {
        W = math.random(1);
        .send(N, achieve, pong(W));
    }.

@lm[atomic]
+!finished : ended(I) & t_total(T) & T > I + 1 <-
    -+ended(I+1).

+!finished <-
    Time = system.time;
    .print("done at: ", Time);
    .stopMAS.
