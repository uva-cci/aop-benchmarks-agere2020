+!token(0) <- .printf("finished"); .send("distributor", achieve, finished).

+!token(T) : next(X) <- .send(X, achieve, token(T-1)).

+!token(T) : .my_name(M) & .delete("thread_with_distributor", M, NS) & .term2string(N,NS) &
                                     Y = N mod 500 + 1 &
                                 .concat("thread_with_distributor",Y,X) <- +next(X); .send(X, achieve, token(T-1)).

+!token(N) : not next(F) <- .printf("WTF").

