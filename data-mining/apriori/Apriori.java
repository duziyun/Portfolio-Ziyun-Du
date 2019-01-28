

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.HashMap;
import java.util.Map;
import java.util.LinkedList;
import java.util.TreeMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Set;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
public class Apriori {
    public static void main(String[] args) throws Exception {
        AprioriLib A = new AprioriLib();
        //Arguments
        String InFileName = args[0];
        int min_support = Integer.valueOf(args[1]);
        String OutFileName = args[2];
        //data structures
	ArrayList<ArrayList<String>> RawTrans = new ArrayList<ArrayList<String>>(); //raw transactions
	HashMap<String, Integer> C1 = new HashMap<String, Integer>(); //one-element set; //one-element set
	HashMap<String, Integer> L = new HashMap<String, Integer>(); //frequentItemSets //INDEX is k-item-set, value is support
	//IO
	HashMap<String, String> to_print = new HashMap<String, String>(); 
	BufferedWriter bw = null;
	FileWriter fw = null;
	
        //read input file to get Transactions and one-element frequent set
        try{
            BufferedReader br = new BufferedReader(new FileReader(InFileName)); 
            for(String line; (line = br.readLine()) != null; ) {
                String tx[] = line.split("\\s+");
                ArrayList<String> tr = new ArrayList<String>(Arrays.asList(tx));
                RawTrans.add(tr);
                for(String t:tx) {
                    if(C1.containsKey(t)) C1.put(t, C1.get(t) + 1);
                    else C1.put(t, 1);
                }
            }
        }catch(Exception e) {
            System.err.format("IO Eception!%n");
        }
	//output to file
	try {
	    fw = new FileWriter(OutFileName);
	    bw = new BufferedWriter(fw);
	} catch (IOException e) {
	    e.printStackTrace();
	}
        //create L1
        for(String s:C1.keySet()){
            if(C1.get(s) >= min_support) {
		L.put(s, C1.get(s)); //to fix - no need to create additional
		String line =" ("+L.get(s)+")";
		to_print.put(s,line);
	    }
        }
        
	for(int k = 2; L.size() > 0; ++k) {
            L = A.CandidateGen(L, k); 
	    L = A.Scan(L, RawTrans, k, min_support);
	    //WritetoFile(L);
	    for( String s : L.keySet()){
		String[] a = s.split(",");
		String line = "";
		for(String ss : a){
		    line +=ss+" ";
		}
		to_print.put(line,"("+L.get(s)+")");
	    }
	}
	
	LinkedList<String> ordered = order_output(to_print);
	for(String o : ordered){ 
	    try {
		bw.write(o+to_print.get(o));
		bw.newLine();
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	
	try {
	    if (bw != null)
		bw.close();
	    if (fw != null)
		fw.close();
	    
	} catch (IOException ex) {
	    ex.printStackTrace();
	} 
    }
    public static LinkedList<String> order_output(Map<String, String> a) {
        LinkedList<String> ans = new LinkedList<String>();
        for(String s: a.keySet()){
            String[] ar = s.split("\\s+");
            int done_insertion = 0;
            int search_next = 0;
            if(ans.size() == 0) {
		ans.add(s);
	    }
            else{
                for(int i = 0; i < ans.size();++i) {
                    String[] split = ans.get(i).split("\\s+");
                    for(int j = 0; j < ar.length; ++j) {
			if(Integer.parseInt(split[j]) == Integer.parseInt(ar[j])) {
			    if(split.length - 1 == j) {
				if(i == ans.size() - 1) {
				    ans.add(i + 1, s);
				    done_insertion = 1;
				    break;
				} else {
				    search_next = 1;
				}
				break; 
			    } else if(ar.length - 1 == j){
				ans.add(i, s);
				done_insertion = 1;
				break;
			    } else continue;
			} else if(Integer.parseInt(split[j]) < Integer.parseInt(ar[j])) {
			    if(i == ans.size() - 1) {
				ans.add(i + 1, s);
				done_insertion = 1;
				break;
			    } else {
				search_next = 1;
			    }
			    break;            
			} else {
			    ans.add(i, s);
			    done_insertion = 1;
			    break;
			}
		    } 
		    if(done_insertion == 1) {
			done_insertion = 0;
			break;
		    }
		}
	    }
	}
	return ans;
    }
}


