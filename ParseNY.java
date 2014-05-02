import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;


public class ParseNY {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String input="NY";
		try{
			//write
			FileWriter fw = new FileWriter("NY-afterparse");  
			
			//read
			File filename = new File(input); 
            InputStreamReader reader = new InputStreamReader(  
                    new FileInputStream(filename));
            BufferedReader br = new BufferedReader(reader); 
            String line="";
            StringBuilder builder=new StringBuilder();
            
            while((line=br.readLine())!=null){
            	line=line.replaceAll("\\s+","");
//            	System.out.println(line);
//            	if(line.equalsIgnoreCase("{") || line.equalsIgnoreCase("},") || line.equalsIgnoreCase("}") ){
//            		
//            	}else 
            	
            	/***
            	 * 
            	 name : "12165":{
"PropertyTax":"5590",
"MedianSalePrice":"0",
"MedianCondoValue":0,
"MedianListPricePerSqFt":"0",
"zipcode":"12165",
"NewConstruction":null,
"MedianValuePerSqFt":"235",
"state":"NewYork",
"lot":"-73.508678",
"Median3-BedroomHomeValue":0,
"Median4-BedroomHomeValue":0,
"HomesForSaleByOwner":null,
"HomesForSale":"0",
"PercentHomesDecreasing":"0.113",
"Turnover(SoldWithinLastYr.)":"0.016",
"1-Yr.Change":0,
"ZillowHomeValueIndex":0,
"lat":"42.31527",
"MedianListPrice":"359000",
"Median2-BedroomHomeValue":0,
"MedianSingleFamilyHomeValue":0,
"HomesRecentlySold":"0",
"PercentListingPriceReduction":"0.111",
"Foreclosures":null
},
            	 * 
            	 * 
            	 * ***/
            	
            	if(line.indexOf(":{")>0){
//            		System.out.println(line);
            		String[] result=new String[25];
            		String[] words=line.split("\":");
            		result[0]=words[0].substring(1);
            		
            		for(int i=1;i<25;i++){
            			line=br.readLine();
            			words=line.split("\":");
            			if(words[1].indexOf("null")>=0){
            				result[i]="null";
            			}else{
//            				System.out.println(words[1]);
            				if(words[1].indexOf("\"") >= 0){
            					result[i]=words[1].substring(2, words[1].length()-3);
//               				    System.out.println(result[i]);
            				}else{
            					result[i]=words[1].substring(1, words[1].length()-3);
            					result[i]="0";
//               				    System.out.println(result[i]);
            				}
            				
            			}
//            			System.out.println(result[i]);		
            		}
            		builder.append(result[0]);
            		for(int k=1;k<25;k++){
            			builder.append("\t"+result[k]);
            		}
            		fw.write(builder.toString()+"\n");
            		fw.flush();
            		builder.setLength(0);
            		
            		for(int q=0;q<25;q++){
            			System.out.print(result[q]+"\t");
            			
            		}
            		System.out.println();
            	}
            }
			
		}catch(IOException e){
			
		}

	}

}
