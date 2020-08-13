// parameters --
// number of tokens: 100
// number of agents: 10
// number of consumptions: 1

t_total(100).
t_counter(1).
w_total(10).
ended(0).
!init_all.

+!init_all : t_total(T) & w_total(WT) <-
    Time = system.time;
    +start(Time);
    while (t_counter(I) & I <= T) {
    	W = math.ceil(I * (WT/T));
        .concat("thread_with_distributor", W, Thread);
        .send(Thread, achieve, token(1));
        -+t_counter(I+1);
    }
.

@lm[atomic]
+!finished : ended(I) & t_total(T) & T > I + 1 <-
	-+ended(I+1).

+!finished <-
    Time = system.time;
    +end(Time);
    .save_agent("distributor-FINALSNAPSHOT.asl")
	.stopMAS.

