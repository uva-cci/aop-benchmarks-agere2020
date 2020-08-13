package token_ring;

public class Config {
	
	public static double nb_agents = 5.0;
	public static double nb_tokens = 10.0;
	public static int nb_token_hops = 50;
	
	public static void main(String[] args) throws Exception {
		
		
		if(args.length < 2)
		{
			System.out.println("args not provided");
			return;
		}
		
		nb_tokens = Integer.valueOf(args[0]);
		nb_agents = Integer.valueOf(args[1]);
		
		if(args.length == 3)
			 nb_token_hops =  Integer.valueOf(args[2]);
		
		System.out.println(String.format("running with config: { \n\tagents: "+ nb_agents +", \n\ttokens: " + nb_tokens +", \n\ttoken hops: %d\n}",nb_token_hops));
		
		io.sarl.bootstrap.SRE.main(new String[] {"token_ring.BootAgent"});
	}
	
	public static int exit() {
		System.exit(0);
		return 0;
	}
}
