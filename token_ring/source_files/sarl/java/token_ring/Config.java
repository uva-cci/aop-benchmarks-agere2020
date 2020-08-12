package token_ring;

public class Config {
	
	public static int nb_agents = 500;
	public static int nb_tokens = 250;
	public static int nb_token_hops = 50000;
	
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
		
		System.out.println(String.format("running with config: { \n\tagents: %d, \n\ttokens: %d, \n\ttoken hops: %d\n}",nb_agents,nb_tokens,nb_token_hops));
		
		io.sarl.bootstrap.SRE.main(new String[] {"token_ring.BootAgent"});
	}
}
