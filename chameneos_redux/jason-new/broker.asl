/*
    This agent receives asks for meetings from chameneos,
    when pairs are formed, they are informed of their partners for
    the mutation.
*/

nb_meetings(100000).
nb_chameneos(500).
ready(0).
done(0).

!init.

+!init <- .term2string(system.time,T); .printf("sstart at:"); .printf(T).

@lm[atomic]
+!ready : ready(I) & nb_chameneos(T) & T > I + 1 <-
    -+ready(I+1).

+!ready <- .broadcast(achieve,go_mall).

@lb[atomic] // this plan is atomic because it changes I, I is the number of meetings left
+!meet(C2)[source(A2)] : first(A1,C1) & nb_meetings(I) & I > 0
   <- -first(A1,C1);
      -+nb_meetings(I-1);
      //.println("meet ",A1," and ",A2);
      //.println("meet ",A1," and ",A2);
      .send(A1,achieve,mutate(A2,C2));
      .send(A2,achieve,mutate(A1,C1)).
          
+!meet(C1)[source(A1)] : not nb_meetings(0) <- +first(A1,C1).

@lc[atomic]
+!meet(_) : not finished <- +finished; .broadcast(achieve,print_results).

+!meet(_).
   

@ls[atomic]
+!done : done(I) & nb_chameneos(T) & T > I + 1 <-
    -+done(I+1).

+!done <- .term2string(system.time,T); .printf("sdone at:"); .printf(T) ; .stopMAS.
