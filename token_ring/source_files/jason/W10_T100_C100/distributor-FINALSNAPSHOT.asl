// beliefs and rules
ended(99).
start(1597265223917).
t_counter(101).
end(1597265224044).
t_total(100).
w_total(10).


// initial goals


// plans from distributor.asl

@l__7[source(self)] +!init_all : (t_total(T) & w_total(WT)) <- (Time = system.time); +start(Time); .loop((t_counter(I) & (I <= T)),{ (W = math.ceil((I*(WT/T)))); .concat("thread_with_distributor",W,Thread); .send(Thread,achieve,token(100)); -+t_counter((I+1)) }).
@lm[atomic,source(self)] +!finished : (ended(I) & (t_total(T) & (T > (I+1)))) <- -+ended((I+1)).
@l__8[source(self)] +!finished <- (Time = system.time); +end(Time); .save_agent("distributor-FINALSNAPSHOT.asl"); .stopMAS.

