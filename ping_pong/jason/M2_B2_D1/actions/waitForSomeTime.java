package actions;

import jason.asSemantics.DefaultInternalAction;
import jason.asSemantics.TransitionSystem;
import jason.asSemantics.Unifier;
import jason.asSyntax.NumberTermImpl;
import jason.asSyntax.Term;

import java.util.concurrent.TimeUnit;

public class waitForSomeTime extends DefaultInternalAction {

    @Override
    public Object execute(TransitionSystem ts, Unifier un, Term[] args) throws Exception {
        int wait = (int)(Double.parseDouble(args[0].toString()) * 1000d);
        System.out.println("waiting for " + wait + "ms");
        Thread.sleep(wait);
        return true;
    }


}
