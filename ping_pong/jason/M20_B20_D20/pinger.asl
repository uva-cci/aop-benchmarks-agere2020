// parameters --
// number of matchs: 20
// number of balls: 20
// delay: 20

ended(0).
t_total(20).

!init.

+!init : t_total(T) & .my_name(M) &
             .delete("pinger", M, NS) &
             .concat("ponger", NS, N) <-
    Time = system.time;
    .print("start at: ", Time);
    for ( .range(I,1,T) ) {
        W = math.random(20);
        .send(N, achieve, pong(W));
    }.

@lm[atomic]
+!finished : ended(I) & t_total(T) & T > I + 1 <-
    -+ended(I+1).

+!finished <-
    Time = system.time;
    .print("done at: ", Time);
    .stopMAS.
