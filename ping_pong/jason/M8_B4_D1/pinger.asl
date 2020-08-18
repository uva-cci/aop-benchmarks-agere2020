// parameters --
// number of pingers: 8
// number of balls: 4
// delay: 1

ended(0).
terminated(0).
t_total(4).
m_total(8).

!init.

+!init : t_total(T) <-
    Time = system.time;
    .print("start at: ", Time);
    for ( .range(I,1,T) ) {
        W = math.random(1);
        .send(ponger, achieve, pong(W));
    }.

@lm[atomic]
+!finished : ended(I) & t_total(T) & T > I + 1 <-
    -+ended(I+1).

+!finished <-
    .send("pinger1", achieve, terminate).

@lm2[atomic]
+!terminate : terminated(I) & m_total(M) & M > I + 1 <-
    -+terminated(I+1).

+!terminate <-
    Time = system.time;
    .print("done at: ", Time);
    .stopMAS.
