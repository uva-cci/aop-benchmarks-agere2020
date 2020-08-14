/*
    The chameneo agent asks the broker for a meeting and them, when a pair is found,
    mutates its color based on the color of the pair. 
    
    The belief color/1 represents the current color of the chameneo. It is initially
    informed by main and then changed each mutation.
*/

{ include("comp.asl") }

// some counters for the number of meetings
nb_meetings(0).
nb_meetings_same_color(0).

+!go_mall : color(C) <- .send(broker, achieve, meet(C)).
   
+!mutate(A,C2) : color(C1) & complement(C1, C2, C) & nb_meetings(N)
   <- -+nb_meetings(N+1);
      //.println("Meet a chameneo with color ",C2,", then changing my color from ",C1," to ",C);
      .abolish(color(_));
      +color(C);
      !!check_same(A);
      !go_mall.
      
+!check_same(A) : .my_name(A) & nb_meetings_same_color(N) <- -+nb_meetings_same_color(N+1).
+!check_same(_). 
         
+!stop : .my_name(Me) <- .kill_agent(Me).
            
+?nm(N) : nb_meetings(N) & nb_meetings_same_color(NS) // main asked the number of meetings, so the run is finished
   <- //!spell(NS,NSS);
      .println(N,": shoul be 0:",NS).

