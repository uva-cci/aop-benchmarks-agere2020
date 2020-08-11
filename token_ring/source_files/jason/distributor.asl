t_total(1).
t_counter(1).
w_total(500).
ended(0).
!init_all.



+!init_all : t_total(T) & w_total(WT) <-
                .printf("start");
                while(t_counter(I) & I <= T) {
                    W = math.round(I * (WT/T));
                   .concat("thread_with_distributor",W,Thread);
                   .send(Thread,achieve,token(50000));
                   -+t_counter(I+1);
                 }
                 .

@lm[atomic] // this plan is atomic because it changes I, I is the number of meetings left
+!finished : ended(I) & t_total(T) & T < I
   <-
      -+ended(I+1).


+!finished <- .stopMAS.


