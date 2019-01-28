
import java.io.*;
import java.io.FileReader;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.*;
public class SkylinOS {
    static private List<int[]> dataList;
    static private List<int[]> skylineList;
    public static void main(String[] args) throws Exception{   
        long startTime = System.currentTimeMillis();
        //Arguments
        String InFileName = args[0];
        String OutFileName = args[1];
        //IO
	BufferedWriter bw = null;
	FileWriter fw = null;
	// Data structure
        dataList = new ArrayList<int[]>();
        skylineList = new ArrayList<int[]>(); //use a new list to avoid deletion
        //if(DBG_ENABLE) System.out.format("Input file:%20s%nOutput file:%20s%n", InFileName, OutFileName );
        //INPUT FROM FILE#######################################################
        try{
            BufferedReader br = new BufferedReader(new FileReader(InFileName)); 
            for(String line; (line = br.readLine()) != null; ) {
                String temp[] = line.split(",");
                //System.out.format("reading line: %s%n", line);
                //System.out.format("read %d %d%n",Integer.parseInt(temp[0]),Integer.parseInt(temp[1]));
                dataList.add(new int[]{Integer.parseInt(temp[0]), Integer.parseInt(temp[1])});
                //System.out.format("after read dataList[$][0]=%d dataList[$][1]=%d%n", dataList.get(dataList.size()-1)[0],dataList.get(dataList.size()-1)[1]);
            }
        }catch(Exception e) {
            System.err.format("IO Eception!%n");
        }
        //List<int[]> tempskylineList = new ArrayList<int[]>();
        skylineHelper SH = new skylineHelper();
        
        //SH.baseSkyline(dataList, skylineList);
        skylineList = SH.twoDSkyline(dataList);
        //OUTPUT TO FILE########################################################
	try {
	    fw = new FileWriter(OutFileName);
	    bw = new BufferedWriter(fw);
	} catch (IOException e) {
	    e.printStackTrace();
	}
	try {
            bw.write(Integer.toString(skylineList.size()));
            bw.newLine(); 
            for(int[] d: skylineList) {
                bw.write(Integer.toString(d[0])+','+Integer.toString(d[1]));
                bw.newLine(); 
            }
            long endTime   = System.currentTimeMillis();
            long totalTime = endTime - startTime;
            NumberFormat formatter = new DecimalFormat("#0.00000");
            System.out.println();
            bw.write(formatter.format(totalTime / 1000d)+" seconds");
	} catch (IOException e) {
            e.printStackTrace();
	}
        try {
	    if (bw != null) bw.close();
	    if (fw != null) fw.close();
	} catch (IOException ex) {
	    ex.printStackTrace();
	} 
        //END OF OUTPUT TO FILE#################################################
    }
}
