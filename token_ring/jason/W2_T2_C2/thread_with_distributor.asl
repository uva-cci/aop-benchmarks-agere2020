// parameters --
// number of agents: 2 

+!token(0) <- 
	.send("distributor", achieve, finished).

+!token(T) : next(X) <- 
	.send(X, achieve, token(T-1)).

+!token(T) : .my_name(M) & 
             .delete("thread_with_distributor", M, NS) & 
             .term2string(N, NS) &
             Y = N mod 2 + 1 &
             .concat("thread_with_distributor", Y, X) <- 
	+next(X);
	.send(X, achieve, token(T-1)).


