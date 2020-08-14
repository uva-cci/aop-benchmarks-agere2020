package chameneos;



public class ColorUtils {
	
				
	   public static String color(int id) {
		
		switch (id % 3) {
			case 0 : return "red";
			case 1 : return "blue";
			case 2 : return "yellow";
		}
		
		
		return "blue";
	   }
	   
	   public static String mutate(String c1,String c2) {
		   if(c1.equals(c2)) return c1;
		   String c = c1+c2;
		   if(c.contains("red") && c.contains("blue")) return "yellow";
		   else if(c.contains("yellow") && c.contains("blue")) return "red";
		   else if(c.contains("red") && c.contains("yellow")) return "blue";
		   throw new RuntimeException();
	   }

	
}
