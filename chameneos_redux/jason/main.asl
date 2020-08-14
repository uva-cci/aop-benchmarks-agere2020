/*
    This agent manages the overall execution of the experiment:
        . printouts the required messages
        . for each "run" (see runs.asl)
          . create the chameneos agents
          . wait the meetings to finish
          . collect data
*/

{ include("runs.asl") } // this file contains the runs of this experiment and is used as paramenters comming from the command shell
{ include("comp.asl") } // this file contains some common plans

!start. 

+!start
   <- !show_complements;
      !run.
   
+!show_complements
   <- for ( .member(A,[blue,red,yellow]) & .member(B,[blue,red,yellow]) & complement(A,B,C) ) {
         .println(A," + ",B," -> ",C);
      }.
      
+!run : run(Id,Colors,N)
   <- -run(Id,Colors,N);
         
      // print colors
      .println;
      for (.member(C,Colors)) {
          .print(" ",C);
      }
      .println;
      
      .send(broker,tell,nb_meets(N));
      
      // create the agents for the Colors
      -+chameneos_names([]);
      for (.range(I,1,.length(Colors))) {
         .concat("c_",Id,I,AgName);
         .create_agent(AgName,"chameneo.asl");
         .nth(I-1,Colors,C);
         .send(AgName,tell,color(C));
         // update the list of chameneos
         ?chameneos_names(L);
         -+chameneos_names([AgName|L]);
      }
      
      // start agents (it is better to create them all, and start them latter together)
      ?chameneos_names(L);
      .send(L,achieve,go_mall).
      
+!run // no more runs
   <- .stopMAS.
      
+run_finished : chameneos_names(L) // belief sent by broker 
   <- .send(L,askOne,nm(_)).       // ask chameneos the number of meetings
   
// receives the number of meetings from chameneos and, if all of them has already sent, finish the "run"   
+nm(_) : chameneos_names(L) & .findall(N,nm(N)[source(_)],LN) & .length(LN) == .length(L)
   <- .broadcast(achieve,stop);    // stop the agents
      //!spell(math.sum(LN),S);
      .println(math.sum(LN));
      .abolish(run_finished);
      .abolish(nm(_));
      !run. // next run
      
