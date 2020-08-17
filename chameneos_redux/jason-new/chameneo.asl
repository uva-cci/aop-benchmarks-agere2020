/*
    The chameneo agent asks the broker for a meeting and them, when a pair is found,
    mutates its color based on the color of the pair. 
    
    The belief color/1 represents the current color of the chameneo. It is initially
    informed by main and then changed each mutation.
*/

nb_meetings(0).
nb_meetings_self(0).

color_code(0,red).
color_code(1,blue).
color_code(2,yellow).

complement(blue,   red,    yellow).
complement(blue,   yellow, red).
complement(red,    blue,   yellow).
complement(red,    yellow, blue).
complement(yellow, blue,   red).
complement(yellow, red,    blue).
complement(C, C, C).

!set_and_print_color.

+!set_and_print_color : .my_name(M) &
                                     .delete("chameneo", M, NS) &
                                     .term2string(N, NS) &
                                     Y = N mod 3  &
                                     color_code(Y,C) &
                                      .term2string(C,CS)<-
   .printf(CS); +color(C); .send(broker, achieve, ready).


+!go_mall : color(C) <- .send(broker, achieve, meet(C)).
   
+!mutate(A,C2) : color(C1) & complement(C1, C2, C) & nb_meetings(N)
   <- -+nb_meetings(N+1);
      //.println("Meet a chameneo with color ",C2,", then changing my color from ",C1," to ",C);
      .abolish(color(_));
      +color(C);
      !check_same(A);
      !go_mall.
      
+!check_same(A) : .my_name(A) & nb_meetings_self(N) <- -+nb_meetings_self(N+1).
+!check_same(_). 
         

            
+!print_results : nb_meetings(N) & nb_meetings_self(NS) & .term2string(N,NT) & .term2string(NS,NST)
   <-
      .println(NT,": should be 0:",NST);
      .send(broker, achieve, done).

