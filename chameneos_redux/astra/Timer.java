package chameneos;


import astra.core.Module;
import astra.core.Module.ACTION;

public class Timer extends Module {
	
	public static Timer INSTANCE = new Timer();
		
	public long startTime = 0;
	
	public int finished = 0;
	
	@ACTION public boolean time() {
		System.out.println("time:" + System.currentTimeMillis());
		return true;
	}
	
	@ACTION public boolean start() {
		Timer.INSTANCE.startTime = System.currentTimeMillis();
		return true;
	}
	
	@ACTION public boolean timeTaken() {
		System.out.println(System.currentTimeMillis() - Timer.INSTANCE.startTime);
		return true;
	}
	
	@ACTION public synchronized boolean done() {
		Timer.INSTANCE.finished++;
		return true;
	}
	
	
	@TERM
	public int finished() {
		return this.INSTANCE.finished;
	}
	
	
}
