package token_ring;


import astra.core.Module;
import astra.core.Module.ACTION;

public class Timer extends Module {
	
	public static Timer INSTANCE = new Timer();
		
	public long startTime = 0;
	
	public int finished = 0;
	
	
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
	   public int calc_worker(int I , int W, int T) {
		int w = (int) ((I * Math.ceil( ((double) W) / ((double) T))) % W);
		if(w == 0) return (int) W;
		return w;
	   }
	
	@TERM
	   public int finished() {
		return this.INSTANCE.finished;
	   }
	
	@ACTION public boolean time() {
		System.out.println("time:" + System.currentTimeMillis());
		return true;
	}
	
	
}
