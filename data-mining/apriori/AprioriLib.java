
import java.util.HashMap;
import java.util.Set;
import java.util.ArrayList;
import java.util.List;
import java.io.Writer;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
public class AprioriLib {
    public HashMap<String, Integer> CandidateGen(HashMap<String, Integer> L, int k){ 
        Set<String> sets = L.keySet();
        HashMap<String, Integer> Ck = new HashMap<String, Integer>();
	LinkedList<String> ordered_ = order(L);
	
        for(String s:ordered_){ //each element is a index ABC ...
            String[] set1 = s.split(","); //one set
	    int[] set_int1 = new int[set1.length];
	    for(int jj =0; jj < set1.length; ++jj){
		set_int1[jj] = Integer.parseInt(set1[jj]);
	    }
	    Arrays.sort(set_int1);
            for(String j:ordered_) { 
                String[] set2 = j.split(","); //one set
		int[] set_int2 = new int[set2.length];
		for(int jj =0; jj < set2.length; ++jj){
		    set_int2[jj] = Integer.parseInt(set2[jj]);
		}
		Arrays.sort(set_int2);
		Boolean DO = true;
		for(int iii = 0; iii < k-1; ++iii ){
		    if(set_int1[iii] > set_int2[iii]) {
			DO =false;
			break;
		    }
		}
		if(DO){
		    Boolean valid = true; 
		    for(int t = 0; t < k - 2; ++t) {
			if(set_int1[t] == set_int2[t]) valid = false;
		    }
		    if(valid) {
			String set_new = Integer.toString(set_int1[0]);
			for(int f = 1; f < set_int1.length; f ++) {
			    set_new += ","+Integer.toString(set_int1[f]);
			}
			set_new += ","+Integer.toString(set_int2[set_int2.length - 1]);
			Ck.put(set_new,0);
		    }
		}
            }   
        }
        //now need to remove the entry whose subset doesn't exist in L
        ArrayList<String> to_remove = new ArrayList<String>();
        for(String set3:Ck.keySet()){
            //System.out.format("set3 is %s%n", set3);
            String[] sets3 = set3.split(",");
            if(!SubsetGenCheck(sets3, L)){ //remove the invalid entry
                to_remove.add(set3);
            }
        }
        for(String sss:to_remove) Ck.remove(sss);
        return Ck;
    }

    public LinkedList<String> order(HashMap<String, Integer> a) {
        LinkedList<String> ans = new LinkedList<String>();
        for(String s: a.keySet()){
            String[] ar = s.split(",");
            int done_insertion = 0;
            int search_next = 0;
            if(ans.size() == 0) {
		ans.add(s);
	    }
            else{
                for(int i = 0; i < ans.size();++i) {
                    String[] split = ans.get(i).split(",");
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
    
    //k-item set to get k-1 subsets
    public Boolean SubsetGenCheck(String[] s, HashMap<String, Integer> L){ // A B C
        for(int i = 0; i< s.length; ++i) {
            String ss = "";
            for(int j = 0; j < s.length; ++j) {
                if(j != i) {
                    if(ss.equals("")) ss = s[j];
                    else ss += ","+s[j];
                }
            }
            //check if this subset exist in L
            if(!L.containsKey(ss)) return false;
        }
        return true;
    } 
    private HashMap<String,Integer> kSubsets;
    //to do 1: one possible optimizaiton is that: use subsets of DB for k-1 to compute that of k - DP
    //to do 2: should exist some conditions where some transactions shoud be excluded:when the tr contains no entry from Lk-1
    public HashMap<String, Integer> Scan(HashMap<String, Integer> Ck,ArrayList<ArrayList<String>> RawTrans, int k, int min_support) {
        kSubsets = new HashMap<String,Integer> ();
        for(ArrayList<String> l: RawTrans){
            String[] tr =  new String[l.size()];
            tr = l.toArray(tr);
	    Subsetk(tr, k, Ck);
        }
        ArrayList<String> to_remov = new ArrayList<String>();
        for(String s:kSubsets.keySet()) { //!Ck.containsKey(s)
            if(kSubsets.get(s) < min_support) to_remov.add(s); //to do: can check if Ck contains it when adding to kSubsets in Subsetk
        }
        for(String ss: to_remov) kSubsets.remove(ss);
        return kSubsets;
    }
    
    private void Subsetk(String[] S, int k, HashMap<String, Integer> Ck) {
	List<List<String>> res = new ArrayList<>();
        res.add(new ArrayList<String>());
        for(String i : S) {
            List<List<String>> tmp = new ArrayList<>();
            for(List<String> sub : res) {
                List<String> a = new ArrayList<>(sub);
                a.add(i);
                tmp.add(a);
            }
            for(List<String> t: tmp) {
                if(t.size() < k) res.add(t);
                if(t.size() == k){
		    String oneSubset = "";
		    for(String tt : t) {
			if(oneSubset.equals("")) oneSubset = tt;
			else oneSubset += ","+tt;
		    }
		    if(Ck.containsKey(oneSubset)){ //to do:pontential is order is messed up
			if(!kSubsets.containsKey(oneSubset)) kSubsets.put(oneSubset, 1);
			else kSubsets.put(oneSubset,kSubsets.get(oneSubset) + 1);
		    }
		}
            }
        }   
    }
    
    public void print_subsets(int k){
	System.out.format("%nthe subsets of DB for k = %d is%n", k);
	for(String s: kSubsets.keySet()) System.out.format("support[%s] = %d%n",s, kSubsets.get(s));
    }
}
