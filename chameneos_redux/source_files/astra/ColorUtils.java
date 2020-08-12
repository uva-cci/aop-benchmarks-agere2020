package chameneos;


import astra.core.Module;
import astra.lang.Strings;

public class ColorUtils extends Module {
	
	public static ColorUtils INSTANCE = new ColorUtils();
		
	
	
	
	
	@TERM
	   public String calc_worker(String name) {
		int id = Integer.valueOf(name.replaceAll("chameneos", ""));
		
		switch (id % 3) {
			case 0 : return "red";
			case 1 : return "blue";
			case 2 : return "yellow";
		}
		
		return "blue";

		
	   }
	
}
