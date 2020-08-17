+!pong(D) <-
        .concat("", D, Wait);
        .printf("start waiting");
        actions.waitForSomeTime(D);
        .printf("done waiting");
        .send("pinger",achieve,finished)
.


