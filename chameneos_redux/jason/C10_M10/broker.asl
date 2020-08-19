// parameters --
// number of meetings: 10
// number of agents: 10

/*
    This agent receives asks for meetings from chameneos,
    when pairs are formed, they are informed of their partners for
    the mutation.
*/

nb_meetings(10).
nb_chameneos(10).
ready(0).
done(0).

!init.

+!init <-
    Time = system.time;
    .print("start at: ", Time).

@lm[atomic]
+!ready : ready(I) & nb_chameneos(T) & T > I + 1 <-
    -+ready(I+1).

+!ready <- .broadcast(achieve,go_mall).

@lb[atomic] // this plan is atomic because it changes I, I is the number of meetings left
+!meet(C2)[source(A2)] : first(A1,C1) & nb_meetings(I) & I > 0 <-
    -first(A1,C1);
    -+nb_meetings(I-1);
    .send(A1,achieve,mutate(A2,C2));
    .send(A2,achieve,mutate(A1,C1)).
          
+!meet(C1)[source(A1)] : not nb_meetings(0) <-
    +first(A1,C1).

@lc[atomic]
+!meet(_) : not finished <-
    +finished;
    .broadcast(achieve, print_results).

+!meet(_).

@ls[atomic]
+!done : done(I) & nb_chameneos(T) & T > I + 1 <-
    -+done(I+1).

+!done <-
    Time = system.time;
    .print("done at: ", Time);
   .stopMAS.