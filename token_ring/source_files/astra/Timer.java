package token_ring;


import astra.core.Module;

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
		return Math.round(I * ( W / T ));
	   }
	
	@TERM
	   public int finished() {
		return this.INSTANCE.finished;
	   }
	
	
}
