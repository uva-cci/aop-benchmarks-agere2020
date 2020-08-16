// parameters --
// number of tokens: __NBTOKENS__
// number of agents: __NBAGENTS__
// number of consumptions: __NBCONSUMPTIONS__

+!pong(D) <-
        .concat("", D, Wait);
        .printf("start waiting");
        actions.waitForSomeTime(D);
        .printf("done waiting");
        .send("pinger",achieve,finished)
.


