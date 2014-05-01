import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.InputStreamReader;


public class ParseSkillsJson {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
			String input="1-s";
			try{
				//write
				FileWriter fw = new FileWriter("1-s-afterparse");  
				
				//read
				File filename = new File(input); 
	            InputStreamReader reader = new InputStreamReader(  
	                    new FileInputStream(filename));
	            BufferedReader br = new BufferedReader(reader); 
	            String line="";
	            StringBuilder builder=new StringBuilder();
	            
	            while((line=br.readLine())!=null){
	            	String[] words=line.split("},");
	            	for(int index=0;index<words.length;index++){
	            		String current=words[index].substring(2);

	            		String[] fields=current.split("\",");
	            		for(int q=0;q<fields.length;q++){
	            			/**
	            			 * "date": "2014-04-16
 "jobTitle": "Windows System Administrator
 "company": "Modis
 "location": "San Antonio, TX
 "detailUrl": "http://www.dice.com/job/result/10208432/39828615?src=19"
 
 "skills": "NOT FOUND",
 "jobTitle": "Database Design Engineer 4", 
 "company": "NORTHROP GRUMMAN",
  "detailUrl": "http://www.dice.com/job/result/ngitbot/14003579?src=19",
   "location": "San Diego, CA", 
   "date": "2014-04-15"},
 
	            			 * 
	            			 * **/
	            			String[] values=fields[q].split("\": \"");
	            			
	            			if(values.length>1){
	            				builder.append(values[1]);
		            			System.out.print(values[1]);
		            			if(q<fields.length-1){
		            				builder.append("\t");
		            				System.out.print("\t");
		            			}
	            			}

	            		}
	            		builder.deleteCharAt(builder.length()-1);
	            		fw.write(builder.toString()+"\n");
	            		fw.flush();
	            		builder.setLength(0);
	            		System.out.println();
	            		
	            	}
	            }
				
			}catch(Exception e){
				System.out.println(e.getMessage());
			}
			 
	}

}
