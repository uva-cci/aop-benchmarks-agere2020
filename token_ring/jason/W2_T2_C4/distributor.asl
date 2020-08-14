// parameters --
// number of tokens: 2
// number of agents: 2
// number of consumptions: __NBHOPS__

t_total(2).
t_counter(1).
w_total(2).
ended(0).
!init_all.

+!init_all : t_total(T) & w_total(WT) <-
    Time = system.time;
    .print("start at: ", Time);
    while (t_counter(I) & I <= T) {
    	W = math.ceil(I * (WT/T));
        .concat("thread_with_distributor", W, Thread);
        .send(Thread, achieve, token(__NBHOPS__));
        -+t_counter(I+1);
    }
.

@lm[atomic]
+!finished : ended(I) & t_total(T) & T > I + 1 <-
	-+ended(I+1).

+!finished <-
    Time = system.time;
    .print("done at: ", Time);
	.stopMAS.

