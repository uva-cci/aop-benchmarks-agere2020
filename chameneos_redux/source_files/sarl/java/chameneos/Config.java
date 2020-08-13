package chameneos;

public class Config {
	
	public static int nb_agents = 500;
	public static int nb_meetings = 1000;
	
	public static void main(String[] args) throws Exception {
		
		
		if(args.length < 2)
		{
			System.out.println("args not provided");
			return;
		}
		
		nb_meetings = Integer.valueOf(args[0]);
		nb_agents = Integer.valueOf(args[1]);
		
		
		
		System.out.println(String.format("running with config: { \n\tagents: %d, \n\tmeetings: %d\n}",nb_agents,nb_meetings));
		
		io.sarl.bootstrap.SRE.main(new String[] {"chameneos.BootAgent"});
	}
	
	public static int exit() {
		System.exit(0);
		return 0;
	}
}
