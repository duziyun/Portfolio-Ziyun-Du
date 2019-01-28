import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Set;

public class Relation {
	public String relationname;
	public List<List<String>> attributename;
	public List<String> attributetype;
	public List<Integer> displaysize;
	public List<List<String>> tuplesindata;
	
	public Relation(String rname,List<List<String>> attriname,List<String> attritype,List<Integer> dissize,List<List<String>> rdata){
		relationname=rname;
		attributename=attriname;
		attributetype=attritype;
		displaysize=dissize;
		tuplesindata=rdata;	
	}
	
	public Relation(Relation R){
		this.relationname=R.relationname;
		this.attributename=R.attributename;
		this.attributetype=R.attributetype;
		this.displaysize=R.displaysize;
		this.tuplesindata=R.tuplesindata;
	}
	
	public static List<List<String>> readcatalog (String catalogpath){
		List<List<String>> catalogdata = new ArrayList<>();		  
        try {
            Scanner in = new Scanner(new File(catalogpath));
            while (in.hasNextLine()) {
               String str = in.nextLine(); 
               String[] temp = str.split("\\s+");
               List<String> tempList = new ArrayList<String>();
               for(String s:temp) tempList.add(s); 
                catalogdata.add(tempList);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
		return catalogdata;		
	}
	
	public static List<List<String>> readdata(String path){
		List<List<String>> data = new ArrayList<>();		  
        try {
            Scanner in = new Scanner(new File(path));
            while (in.hasNextLine()) {
               String str = in.nextLine(); 
               String[] temp = str.split(",");
               List<String> tempList = new ArrayList<String>();
               for(String s:temp) tempList.add(s.replaceAll("\\s+", "")); 
               data.add(tempList);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
		return data;		
	}
	
	public static HashMap<String,List<String>> getallattributename(String catalogpath){
		List<List<String>> catalogdata=readcatalog (catalogpath);
		HashMap<String,List<String>> allattrinamemap= new HashMap<String,List<String>>();
		List<String> firstlist = new ArrayList<String>();
	    firstlist.add(catalogdata.get(0).get(1));
	    allattrinamemap.put(catalogdata.get(0).get(0),firstlist);
		for (int i = 1; i < catalogdata.size(); i++){
			if(catalogdata.get(i).get(0).equals(catalogdata.get(i-1).get(0))){
				List<String> temlist = allattrinamemap.get(catalogdata.get(i-1).get(0));
			    temlist.add(catalogdata.get(i).get(1));
			    allattrinamemap.put(catalogdata.get(i-1).get(0),temlist);
			}
			else{
				List<String> otherlist = new ArrayList<String>();
			    otherlist.add(catalogdata.get(i).get(1));
			    allattrinamemap.put(catalogdata.get(i).get(0),otherlist);				
			}
		}
		return allattrinamemap;	
	}
	
	public static HashMap<String,List<String>> getallattributetype(String catalogpath){
		List<List<String>> catalogdata=readcatalog (catalogpath);
		HashMap<String,List<String>> allattritypemap= new HashMap<String,List<String>>();
		List<String> firstlist = new ArrayList<String>();
	    firstlist.add(catalogdata.get(0).get(2));
	    allattritypemap.put(catalogdata.get(0).get(0),firstlist);
		for (int i = 1; i < catalogdata.size(); i++){
			if(catalogdata.get(i).get(0).equals(catalogdata.get(i-1).get(0))){
				List<String> temlist = allattritypemap.get(catalogdata.get(i-1).get(0));
			    temlist.add(catalogdata.get(i).get(2));
			    allattritypemap.put(catalogdata.get(i-1).get(0),temlist);
			}
			else{
				List<String> otherlist = new ArrayList<String>();
			    otherlist.add(catalogdata.get(i).get(2));
			    allattritypemap.put(catalogdata.get(i).get(0),otherlist);				
			}
		}
		return allattritypemap;
	}
	
	public static HashMap<String,List<String>> getallattributesize(String catalogpath){
		List<List<String>> catalogdata=readcatalog (catalogpath);
		HashMap<String,List<String>> allattrisizemap= new HashMap<String,List<String>>();
		List<String> firstlist = new ArrayList<String>();
	    firstlist.add(catalogdata.get(0).get(3));
	    allattrisizemap.put(catalogdata.get(0).get(0),firstlist);
		for (int i = 1; i < catalogdata.size(); i++){
			if(catalogdata.get(i).get(0).equals(catalogdata.get(i-1).get(0))){
				List<String> temlist = allattrisizemap.get(catalogdata.get(i-1).get(0));
			    temlist.add(catalogdata.get(i).get(3));
			    allattrisizemap.put(catalogdata.get(i-1).get(0),temlist);
			}
			else{
				List<String> otherlist = new ArrayList<String>();
			    otherlist.add(catalogdata.get(i).get(3));
			    allattrisizemap.put(catalogdata.get(i).get(0),otherlist);				
			}
		}
		return allattrisizemap;
	}
	
	//store all relation in map from catalog
	public static HashMap<String,Relation> storeallrelation(String filepath){
		HashMap<String,Relation> relations=new HashMap<String,Relation>();
		String catalogpath= new String(filepath+"catalog");
		HashMap<String,List<String>> allattrinamemap= new HashMap<String,List<String>>(getallattributename(catalogpath));	
		HashMap<String,List<String>> allattritypemap= new HashMap<String,List<String>>(getallattributetype(catalogpath));		
		HashMap<String,List<String>> allattrisizemap= new HashMap<String,List<String>>(getallattributesize(catalogpath));
		Set<String> keylist=allattrinamemap.keySet();
		int numberofrelation=keylist.size();
		for(String str:keylist) {
			String name= str;
			List<String> tempattributesname= allattrinamemap.get(name);
			List<List<String>> attributesname= new ArrayList<>();
			for(String attriname:tempattributesname){
				List<String> oneattri= new ArrayList<>();
				oneattri.add(attriname);
				oneattri.add(name);
				attributesname.add(oneattri);
			}
            int attrinum=tempattributesname.size();
			List<String> attributestype= allattritypemap.get(name);
			
			List<String> strattributessize= allattrisizemap.get(name);
			List<Integer> intattributessize=new ArrayList<Integer>();
			for(String s : strattributessize) intattributessize.add(Integer.valueOf(s));
			;
			List<List<String>> data=readdata(filepath+name);
			int tuplenum=data.size();
			Relation R= new Relation(name,attributesname,attributestype,intattributessize,data);
			relations.put(R.relationname,R);		
		}
		return relations;		
	}
	
    public static Relation carditionproduct(Relation r1, Relation r2){
    	if(checkr(r1)){
    		return r1;
    	}
    	if(checkr(r2)){
    		return r2;
    	}
    	List<List<String>> newdata=new ArrayList<List<String>>();
		for(int i=0;i<r1.tuplesindata.size();i++){
			for(int j=0;j<r2.tuplesindata.size();j++){
				List<String> temtuple=concatestringlist(r1.tuplesindata.get(i),r2.tuplesindata.get(j));
				newdata.add(temtuple);
			}	
		}
		Relation res= new Relation(null,concate2dlist(r1.attributename,r2.attributename)
			      ,concatestringlist(r1.attributetype,r2.attributetype),concateintlist(r1.displaysize,r2.displaysize),newdata);
        return removeduplicate(res);
    }
	
	public static Relation union(Relation r1,Relation r2){
		if(checkr(r1)){
    		return r1;
    	}
    	if(checkr(r2)){
    		return r2;
    	}
		Relation newr1=new Relation(null,copy2dlist(r1.attributename),new ArrayList<String>( r1.attributetype),
				new ArrayList<Integer>(r1.displaysize),copy2dlist( r1.tuplesindata));
		Relation newr2=new Relation(null,copy2dlist(r2.attributename),new ArrayList<String>( r2.attributetype),
				new ArrayList<Integer>(r2.displaysize),copy2dlist( r2.tuplesindata));
		for(int i=0;i<newr1.tuplesindata.size();i++){
			for(int j=0;j<newr2.tuplesindata.size();j++){
				if(comparelist(newr1.tuplesindata.get(i),newr2.tuplesindata.get(j))){
					newr2.tuplesindata.remove(j);
					break;
				}
			}
		}
		return new Relation(null,copy2dlist(r1.attributename),new ArrayList<String>(r1.attributetype),new ArrayList<Integer>(r1.displaysize),concate2dlist(newr1.tuplesindata,newr2.tuplesindata));
    }
	
	public static Relation intersection(Relation r1,Relation r2){
		if(checkr(r1)){
    		return r1;
    	}
    	if(checkr(r2)){
    		return r2;
    	}
		List<List<String>> ndata=new ArrayList<List<String>>();
		Relation newr1=new Relation(null,copy2dlist(r1.attributename),new ArrayList<String>( r1.attributetype),
				new ArrayList<Integer>(r1.displaysize),copy2dlist( r1.tuplesindata));
		Relation newr2=new Relation(null,copy2dlist(r2.attributename),new ArrayList<String>( r2.attributetype),
				new ArrayList<Integer>(r2.displaysize),copy2dlist( r2.tuplesindata));
		for(int i=0;i<newr1.tuplesindata.size();i++){
			for(int j=0;j<newr2.tuplesindata.size();j++){
				if(comparelist(newr1.tuplesindata.get(i),newr2.tuplesindata.get(j))){
					ndata.add(newr1.tuplesindata.get(i));
					newr2.tuplesindata.remove(j);
					break;
				}
			}
		}
		return new Relation(null,copy2dlist(r1.attributename),new ArrayList<String>(r1.attributetype),new ArrayList<Integer>(r1.displaysize),ndata);
	}
	
	public static Relation minus(Relation r1,Relation r2){
		if(checkr(r1)){
    		return r1;
    	}
    	if(checkr(r2)){
    		return r2;
    	}
		Relation newr1=new Relation(null,copy2dlist(r1.attributename),new ArrayList<String>( r1.attributetype),
				new ArrayList<Integer>(r1.displaysize),copy2dlist( r1.tuplesindata));
		Relation newr2=new Relation(null,copy2dlist(r2.attributename),new ArrayList<String>( r2.attributetype),
				new ArrayList<Integer>(r2.displaysize),copy2dlist( r2.tuplesindata));
		for(int i=0;i<newr1.tuplesindata.size();i++){
			for(int j=0;j<newr2.tuplesindata.size();j++){
				if(comparelist(newr1.tuplesindata.get(i),newr2.tuplesindata.get(j))){
					newr1.tuplesindata.remove(i);
					i--;
					newr2.tuplesindata.remove(j);
					break;
				}
			}
		}
		return newr1;		
	}
	
	public static Relation joinclause(Relation r1,Relation r2, ArrayList<ArrayList<ArrayList<String>>> allconditionlist){
		if(checkr(r1)){
    		return r1;
    	}
    	if(checkr(r2)){
    		return r2;
    	}
		if(r1==null) return r2;
		if(r2==null) return r1;
		if(allconditionlist.size()!=0 && allconditionlist.get(0).get(0).size()==1){
			if(allconditionlist.get(0).get(0).get(0).equals("union")){
				return union(r1,r2);
			}
			else if(allconditionlist.get(0).get(0).get(0).equals("intersection")){
				return intersection(r1,r2);
			}
			else if(allconditionlist.get(0).get(0).get(0).equals("minus")){
				return minus(r1,r2);
			}
			else if(allconditionlist.get(0).get(0).get(0).equals("divide")){
				ArrayList<String> attri=new ArrayList<String>();
				for(List<String> a1:r1.attributename){
					Boolean find=true;
					for(List<String> a2:r2.attributename){
						if(a1.get(0).equals(a2.get(0))){
							find=false;
							break;
						}
					}
					if(find==true){
						attri.add(a1.get(0));
					}
				}
				System.out.println("--------------------------------------------------------");
				System.out.println(attri);
				System.out.println("--------------------------------------------------------");
				
				ArrayList<ArrayList<String>> attris=new ArrayList<ArrayList<String>>();
				for(String s:attri){
					ArrayList<String> temp=new ArrayList<String>();
					temp.add(s);
					attris.add(temp);
				}
				Relation temp1=project(attris,r1);
				Relation qualify=carditionproduct(temp1,r2);
				
				Relation unqualify=minus(qualify,r1);
				Relation res=minus(project(attris,r1),project(attris,unqualify));
				return res;
			}
		}
		else{
			Relation temp=carditionproduct(r1,r2);
			Relation res=selectmethod(allconditionlist,temp);
			return res;
			}
		return null;
		}
	
	public static Relation selectmethod(ArrayList<ArrayList<ArrayList<String>>> allconditionlist,Relation r){
		if(checkr(r)){
    		return r;
    	}
		Relation res=r;
		for(ArrayList<ArrayList<String>> condition:allconditionlist){
			res=simpleselect(condition,res);
		}
		return res;
	}
	
	public static Relation simpleselect(ArrayList<ArrayList<String>> conditionlist,Relation rel){
		if(checkr(rel)){
    		return rel;
    	}
    	List<List<String>> resdata= new ArrayList<>();
    	List<List<String>> data=rel.tuplesindata;
    	ArrayList<String> left=conditionlist.get(0);
    	ArrayList<String> operator=conditionlist.get(1);
    	String oper=operator.get(1);
    	ArrayList<String> right=conditionlist.get(2);
    	int leftindex=getleftorrightindex(left,rel);
    	if(leftindex==-1){
    		String es="";
    		if(left.size()==2){
    			es+=left.get(1);
    		}
    		else{
    			es+=left.get(1);
    			es+=".";
    			es+=left.get(3);
    		}
    		return new Relation("nullattri"+es,null,null,null,null);
    	}
    	if((right.get(0).equals("relationname")
    			||right.get(0).equals("attributename")) && left.get(left.size()-1).equals(right.get(right.size()-1)))
    	   {
    	    int rightindex=-1;
    	    for(int i=rel.attributetype.size()-1;i>=0;i--){
    	    	if(rel.attributename.get(i).get(0).equals(left.get(left.size()-1))){
    	    		rightindex=i;
    	    		break;
    	    	}
    	    }
    	    if(rightindex==-1){
        		String es="";
        		if(right.size()==2){
        			es+=right.get(1);
        		}
        		else{
        			es+=right.get(1);
        			es+=".";
        			es+=right.get(3);
        		}
        		return new Relation("nullattri"+es,null,null,null,null);
        	}
    	    if (oper.equals("=")){
    	    	for(List<String> tuple:data){
    	    		if (tuple.get(leftindex).equals(tuple.get(rightindex))||(tuple.get(leftindex).matches("-?\\d+(\\.\\d+)?")
    	    				&&tuple.get(rightindex).matches("-?\\d+(\\.\\d+)?") && 
    	    				Double.parseDouble(tuple.get(leftindex))==Double.parseDouble(tuple.get(rightindex)))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    	    }
    	    else if (oper.equals("!=")){
    	    	for(List<String> tuple:data){
    	    		if (!tuple.get(leftindex).equals(tuple.get(rightindex))||(tuple.get(leftindex).matches("-?\\d+(\\.\\d+)?")
    	    				&&tuple.get(rightindex).matches("-?\\d+(\\.\\d+)?") && 
    	    				Double.parseDouble(tuple.get(leftindex))!=Double.parseDouble(tuple.get(rightindex)))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    	    }
    	}
    	else if(right.get(0).equals("relationname")
    			||right.get(0).equals("attributename"))
    	   {
    	    int rightindex=getleftorrightindex(right,rel);
    	    if(rightindex==-1){
        		String es="";
        		if(right.size()==2){
        			es+=right.get(1);
        		}
        		else{
        			es+=right.get(1);
        			es+=".";
        			es+=right.get(3);
        		}
        		return new Relation("nullattri"+es,null,null,null,null);
        	}
    	    if (oper.equals("=")){
    	    	for(List<String> tuple:data){
    	    		if (tuple.get(leftindex).equals(tuple.get(rightindex)) || (tuple.get(leftindex).matches("-?\\d+(\\.\\d+)?")
    	    				&&tuple.get(rightindex).matches("-?\\d+(\\.\\d+)?") && 
    	    				Double.parseDouble(tuple.get(leftindex))==Double.parseDouble(tuple.get(rightindex)))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    	    }
    	    else if (oper.equals("!=")){
    	    	for(List<String> tuple:data){
    	    		if (!tuple.get(leftindex).equals(tuple.get(rightindex)) ||(tuple.get(leftindex).matches("-?\\d+(\\.\\d+)?")
    	    				&&tuple.get(rightindex).matches("-?\\d+(\\.\\d+)?") && 
    	    				Double.parseDouble(tuple.get(leftindex))!=Double.parseDouble(tuple.get(rightindex)))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    	    }
    	}
    	else if(right.get(0).equals("string")){
    		if(oper.equals("=")){
    			for(List<String> tuple:data){
    	    		if (tuple.get(leftindex).equals(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    		else{
    			for(List<String> tuple:data){
    	    		if (!tuple.get(leftindex).equals(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    	}
    	else {
    		if(oper.equals("=")){
    			for(List<String> tuple:data){
    	    		if (tuple.get(leftindex).equals(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    		else if(oper.equals(">")){
    			for(List<String> tuple:data){
    	    		if (Double.parseDouble(tuple.get(leftindex))>Double.parseDouble(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    		else if(oper.equals(">=")){
    			for(List<String> tuple:data){
    	    		if (Double.parseDouble(tuple.get(leftindex))>=Double.parseDouble(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    		else if(oper.equals("<")){
    			for(List<String> tuple:data){
    	    		if (Double.parseDouble(tuple.get(leftindex))<Double.parseDouble(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    		else if(oper.equals("<=")){
    			for(List<String> tuple:data){
    	    		if (Double.parseDouble(tuple.get(leftindex))<=Double.parseDouble(right.get(1))){
    	    			resdata.add(tuple);
    	    		}
    	    	}
    		}
    		
    	}
    	Relation res= new Relation(null,copy2dlist(rel.attributename),new ArrayList<String>(rel.attributetype),new ArrayList<Integer>(rel.displaysize),copy2dlist(resdata));
    	return res;
    }
	
	public static Relation project(ArrayList<ArrayList<String>> attrilist,Relation r){
		if(checkr(r)){
    		return r;
    	}
		Collections.reverse(attrilist);
		int attrilength=attrilist.size();
		int alllength=r.attributename.size();
		List<List<String>> nattributename =new ArrayList<List<String>>();
		List<String> nattributetype =new ArrayList<String>();
		List<Integer> ndisplaysize =new ArrayList<Integer>();
		List<List<String>> ntuplesindata =new ArrayList<List<String>>();
		ArrayList<Integer> indexlist=new ArrayList<Integer>();
		for(int i=0;i<attrilength;i++){
			boolean exsit=false;
			String eattri="";
			if(attrilist.get(i).size()==1){
				eattri=attrilist.get(i).get(0);
				for(int j=0;j<alllength;j++){
					if(attrilist.get(i).get(0).equals(r.attributename.get(j).get(0))){
						indexlist.add(j);
						nattributename.add(new ArrayList<String>(r.attributename.get(j)));
						nattributetype.add(r.attributetype.get(j));
						ndisplaysize.add(r.displaysize.get(j));
						exsit=true;
						break;
					}
				}
			}
			else{
				eattri=attrilist.get(i).get(1);
				for(int j=0;j<alllength;j++){
					if(attrilist.get(i).get(1).equals(r.attributename.get(j).get(0)) && attrilist.get(i).get(0).equals(r.attributename.get(j).get(1))){
						indexlist.add(j);
						nattributename.add(new ArrayList<String>(r.attributename.get(j)));
						nattributetype.add(r.attributetype.get(j));
						ndisplaysize.add(r.displaysize.get(j));
						exsit=true;
						break;
					}
				}
			}
			System.out.println(eattri);
			if(exsit==false){
				String error="nullattri"+eattri;
				return new Relation(error,null,null,null,null);
			}
		}
		for(List<String> tuple:r.tuplesindata){
			List<String> ntuple=new ArrayList<String>();
			for(int index:indexlist){
				ntuple.add(tuple.get(index));
			}
			ntuplesindata.add(ntuple);
		}
		
		return removeduplicate(new Relation(null,nattributename,nattributetype,ndisplaysize,ntuplesindata));
	}

	public static Relation storeOneRelation(HashMap<String,Relation> relations,Relation r1,ArrayList<String> renamelist){
		if(checkr(r1)){
    		return r1;
    	}
		Relation nr;
		if(renamelist.size()==1){
			for(int i=0;i<r1.attributename.size();i++){
				for(int j=i+1;j<r1.attributename.size();j++){
					if(r1.attributename.get(i).get(0).equals(r1.attributename.get(j).get(0))){
						String s="ambiguous";
						return new Relation(s,null,null,null,null);
					}
				}
			}
			ArrayList<List<String>> attri= copy2dlist(r1.attributename);
			for(int i=0;i<r1.attributename.size();i++){
				attri.get(i).set(1, renamelist.get(0));
			}
			nr=new Relation(renamelist.get(0),attri,new ArrayList<String>( r1.attributetype),
							new ArrayList<Integer>(r1.displaysize),copy2dlist( r1.tuplesindata));
		}
		else{
			ArrayList<List<String>> attri= copy2dlist(r1.attributename);
			for(int i=0;i<r1.attributename.size();i++){
				attri.get(i).set(0, renamelist.get(i));
				attri.get(i).set(1, renamelist.get(renamelist.size()-1));
			}
			nr=new Relation(renamelist.get(renamelist.size()-1),attri,new ArrayList<String>( r1.attributetype),
					new ArrayList<Integer>(r1.displaysize),copy2dlist( r1.tuplesindata));
		}
			relations.put(nr.relationname, nr);
			return nr;
	}
	public static Relation rename(Relation r1, Relation r2){
		if(checkr(r1)){
    		return r1;
    	}
    	if(checkr(r2)){
    		return r2;
    	}
		if (r2==null){
			return r1;
		}
		else{
			return r2;
		}
	}
	
	public static Relation groupby(ArrayList<String> attrilist,ArrayList<ArrayList<String>> functions,Relation r){
		if(checkr(r)){
    		return r;
    	}
		Map<String, ArrayList<ArrayList<String>>> map=new LinkedHashMap<String,ArrayList<ArrayList<String>>>();
		Collections.reverse(attrilist);
		Collections.reverse(functions);
		int attrilength=attrilist.size();
		int funclen=functions.size();
		int alllength=r.attributename.size();
		ArrayList<String> typelist=new ArrayList<String>();
		List<List<String>> nattributename =new ArrayList<List<String>>();
		List<String> nattributetype =new ArrayList<String>();
		List<Integer> ndisplaysize =new ArrayList<Integer>();
		List<List<String>> ntuplesindata =new ArrayList<List<String>>();
		ArrayList<Integer> attriindexlist=new ArrayList<Integer>();
		ArrayList<Integer> functionindexlist=new ArrayList<Integer>();
		if(attrilist.size()!=0){
			for(int i=0;i<attrilength;i++){
				boolean exsit=false;
				for(int j=0;j<alllength;j++){
					if(attrilist.get(i).equals(r.attributename.get(j).get(0))){
						attriindexlist.add(j);
						nattributename.add(new ArrayList<String>(r.attributename.get(j)));
						nattributetype.add(r.attributetype.get(j));
						ndisplaysize.add(r.displaysize.get(j));
						 exsit=true;
						break;
					}
				}
				if(exsit==false){
					return new Relation("nullattri"+attrilist.get(i),null,null,null,null);
				}
			}
		}
		
		for(int i=0;i<funclen;i++){
			if(functions.get(i).get(1).equals("*")){
				functionindexlist.add(0);
				List<String> tempattri=new ArrayList<String>();
				tempattri.add(functions.get(i).get(0));
				tempattri.add(r.relationname);
				nattributename.add(tempattri);
				nattributetype.add("I");
				ndisplaysize.add(4);
				typelist.add("I");
			}
			else{
				boolean exist=false;
				for(int j=0;j<alllength;j++){
					if(functions.get(i).get(1).equals(r.attributename.get(j).get(0))){
						functionindexlist.add(j);
						List<String> tempattri=new ArrayList<String>();
						tempattri.add(functions.get(i).get(0));
						tempattri.add(r.relationname);
						nattributename.add(tempattri);
						nattributetype.add(r.attributetype.get(j));
						ndisplaysize.add(r.displaysize.get(j));
						typelist.add(r.attributetype.get(j));
						exist=true;
						break;
					  }
			    }
				if(exist==false){
					return new Relation("nullattri"+functions.get(i).get(1),null,null,null,null);
				}
		  }
		}
		if(attrilist.size()!=0){
			for(List<String> tuple:r.tuplesindata){
				StringBuilder sb=new StringBuilder();
				for(int i:attriindexlist){
					sb.append(tuple.get(i)+" ");
				}
				sb.deleteCharAt(sb.length()-1);
				if(map.containsKey(sb.toString())){
					ArrayList<String> ntuple=new ArrayList<String>();
					for(int j:functionindexlist){
						ntuple.add(tuple.get(j));
					}
					map.get(sb.toString()).add(ntuple);
				}
				else{
					ArrayList<ArrayList<String>> newvalue=new ArrayList<ArrayList<String>>();
					ArrayList<String> ntuple=new ArrayList<String>();
					for(int j:functionindexlist){
						ntuple.add(tuple.get(j));
					}
					newvalue.add(ntuple);
					map.put(sb.toString(), newvalue);
					
				}
			}
		}
		
		else{
			ArrayList<ArrayList<String>> value=new ArrayList<ArrayList<String>>();
			for(int i=0;i<r.tuplesindata.size();i++) {
				ArrayList<String> ntuple=new ArrayList<String>();
				for(int j:functionindexlist){
					ntuple.add(r.tuplesindata.get(i).get(j));
				}
				value.add(ntuple);
			}
			map.put("all",value);
		}
		
		for(String key:map.keySet()){
			ArrayList<ArrayList<String>> value=map.get(key);
			ArrayList<String> tuple= new ArrayList<String>();
			if(attrilist.size()!=0){
				for(String s:key.split(" ")){
					tuple.add(s);
				}
			}
		    for(int i=0;i<funclen;i++){
		    	ArrayList<String> func=functions.get(i);
		    	if(func.get(0).equals("max")){
		    		ArrayList<Double> column= new ArrayList<Double>();
		    		for(int j=0;j<value.size();j++){
		    			column.add(Double.parseDouble(value.get(j).get(i)));
		    		}
		    		Double res=Collections.max(column);
		    		if(typelist.get(i).equals("I")){
		    			tuple.add(Integer.toString(res.intValue()));
		    		}
		    		else{
		    			tuple.add(res.toString());
		    		}
		    	}
		    	else if(func.get(0).equals("min")){
		    		ArrayList<Double> column= new ArrayList<Double>();
		    		for(int j=0;j<value.size();j++){
		    			column.add(Double.parseDouble(value.get(j).get(i)));
		    		}
		    		Double res=Collections.min(column);
		    		if(typelist.get(i).equals("I")){
		    			tuple.add(Integer.toString(res.intValue()));
		    		}
		    		else{
		    			tuple.add(res.toString());
		    		}
		    	}
		    	else if(func.get(0).equals("sum")){
		    		Double res=0.0;
		    		for(int j=0;j<value.size();j++){
		    			res+=(Double.parseDouble(value.get(j).get(i)));
		    		}
		    		if(typelist.get(i).equals("I")){
		    			tuple.add(Integer.toString(res.intValue()));
		    		}
		    		else{
		    			tuple.add(res.toString());
		    		}
		    	}
		    	else if(func.get(0).equals("avg")){
		    		Double sum=0.0;
		    		for(int j=0;j<value.size();j++){
		    			sum+=(Double.parseDouble(value.get(j).get(i)));
		    		}
		    		Double res=sum/value.size();
		    		tuple.add(res.toString());	    		
		    	}
		    	else if(func.get(0).equals("any")){
		    		if(value.size()>0){
		    			tuple.add("true");	  
		    		}
		    		else tuple.add("false");	    		
		    	}	
		    	else if(func.get(0).equals("count")){
		    		ArrayList<String> column= new ArrayList<String>();
		    		tuple.add(Integer.toString(value.size()));		    		
		    	}
		    }
		    ntuplesindata.add(tuple);
		}
		return new Relation(r.relationname,nattributename,nattributetype,ndisplaysize,ntuplesindata);
	}
	
	
	//functions bellow are helpers:
	//
	//
	//
	//
	//
	
	//print all information for a Relation
		public void printall(){
			System.out.println(this.relationname);
			/*
			List<List<String>> ddata=this.tuplesindata;
			for (List<String> strings : ddata) {
				 System.out.println(strings.toString());
	          } 
	          
			
			System.out.println(this.attributename);
			System.out.println(this.attributetype);
			System.out.println(this.displaysize);
			System.out.println(this.relationname);*/
			
		}
		
		public static List<List<String>> concate2dlist(List<List<String>> lista,List<List<String>> listb){
			List<List<String>> res= new ArrayList<>();
	    	for(int i=0;i<lista.size();i++){
	    		res.add(new ArrayList<>(lista.get(i)));
	    	}
	    	for(int j=0;j<listb.size();j++){
	    		res.add(new ArrayList<>(listb.get(j)));
	    	}
	    	return res;
	    	
	    }
		
	    public static List<String> concatestringlist(List<String> lista,List<String> listb){
	    	List<String> res= new ArrayList<>();
	    	for(int i=0;i<lista.size();i++){
	    		res.add(lista.get(i));
	    	}
	    	for(int j=0;j<listb.size();j++){
	    		res.add(listb.get(j));
	    	}
	    	return res;
	    	
	    }
	    
	    public static List<Integer> concateintlist(List<Integer> lista,List<Integer> listb){
	    	List<Integer> res= new ArrayList<>();
	    	for(int i=0;i<lista.size();i++){
	    		res.add(lista.get(i));
	    	}
	    	for(int j=0;j<listb.size();j++){
	    		res.add(listb.get(j));
	    	}
	    	return res;
	    	
	    }
	    
	    public static int getattrindex(String orirel, String attr,Relation r){
	    	List<List<String>> attrilist=r.attributename;
	    	int res=-1;
	    	int numofattr=attrilist.size();
	    	if(orirel.equals("")){
	    		for (int i=0;i<numofattr;i++){
	        		if (attrilist.get(i).get(0).equals(attr)){
	        			res=i;
	        			break;
	        		}
	        	}		
	    	}
	    	else {
	    		for (int i=0;i<numofattr;i++){
	        		if (attrilist.get(i).get(0).equals(attr)&&attrilist.get(i).get(1).equals(orirel)){
	        			res=i;
	        			break;
	        		}
	        	}	
	    	}
	    	return res;  	
	    }
	    	
	    public static int  getleftorrightindex(ArrayList<String> element,Relation rel){
	    	int res=-1;
	    	if(element.get(0).equals("relationname")){
	    		res=getattrindex(element.get(1),element.get(3),rel);
	    	}
	    	else {
	    		res=getattrindex("",element.get(1),rel);
	    	}
	    	return res;
	    }
	    
	    public static Relation getrelationbyname(HashMap<String,Relation> relations, String name){
	    	if(!relations.containsKey(name)){
	    		ArrayList<String> error=new ArrayList<String>();
	    		error.add(name);
	    		return new Relation("nullname",null,error,null,null);
	    	}
			Relation  r= relations.get(name) ;
			
			return r;
			
		}
	    
	    //returns true if two tuples are the same
		public static Boolean comparelist(List<String> tuple1,List<String> tuple2){
			for(int i=0;i<tuple1.size();i++){
				if(!tuple1.get(i).equals(tuple2.get(i))) return false;
			}
			return true;
		}
		
		public static ArrayList<List<String>> copy2dlist(List<List<String>> list){
			ArrayList<List<String>> res=new ArrayList<List<String>>();
			for(int i=0;i<list.size();i++) res.add(new ArrayList<String>(list.get(i)));
			return res;
		}
		
		//remove duplicate tuples
		public static Relation removeduplicate(Relation r){
			Relation rcopy=new Relation(null,copy2dlist(r.attributename),new ArrayList<String>( r.attributetype),
					new ArrayList<Integer>(r.displaysize),copy2dlist( r.tuplesindata));
			for(int i=0;i<rcopy.tuplesindata.size();i++){
				for(int j=i+1;j<rcopy.tuplesindata.size();j++){
					if(comparelist(rcopy.tuplesindata.get(i),rcopy.tuplesindata.get(j))){
						rcopy.tuplesindata.remove(j);
						j--;
					}
				}
			}
			return rcopy;
		}
		public static boolean checkr(Relation r){
			if(r!=null && r.relationname!=null && (r.relationname.equals("ambiguous")||r.relationname.equals("nullname")
	    			  ||(r.relationname.length()>9 && r.relationname.substring(0,9).equals("nullattri")))){
				return true;
			}
			else return false;
		}
}
