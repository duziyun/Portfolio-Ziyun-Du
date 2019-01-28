
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
public class skylineHelper {
     private boolean DBG = false;
    List<List<int[]>> subSkyline;//skylines of all subsets
    public void baseSkyline(List<int[]> inList, List<int[]>outList) {
        //SORT THE DATA BASED ON FIRST DIMENSION################################
        Collections.sort(inList,(a, b) -> {
             if(a[0] != b[0]) return a[0] - b[0];
             else return a[1] - b[1];
        });
        //ADD POINT TO ANSER IF ITS 2ND DIMENSION IS NO BIGGER THAN PREVIOUS#### 
        outList.clear();
        outList.add(new int[]{inList.get(0)[0], inList.get(0)[1]});
        for(int i = 1; i < inList.size(); ++i) {
            /*
            if(inList.get(i)[1] <= outList.get(outList.size()-1)[1]) {
                if(!(inList.get(i)[1] == outList.get(outList.size()-1)[1] &&  inList.get(i)[0] == outList.get(outList.size()-1)[0])) { //remove dups
                    outList.add(new int[]{inList.get(i)[0], inList.get(i)[1]});
                }
            } 
            */
            if(inList.get(i)[1] < outList.get(outList.size()-1)[1]) {
                 outList.add(new int[]{inList.get(i)[0], inList.get(i)[1]});
            } 
        }
    }
    //return remaining points and push one skypoint#############################
    public List<int[]> Kskyline(List<int[]> inList, int K) {
         int subsetCnt = 0;
         if(inList.size()%K != 0) subsetCnt = inList.size()/K + 1;
         else subsetCnt = inList.size()/K;
         //partition into subsets###############################################
         List<List<int[]>> subsets =  new ArrayList<>();
         int j = 0;
         for(int i = 0; i<subsetCnt; ++i) {
             List<int[]> temp = new ArrayList<int[]>();
             for(int v = 0; v < K; ++v) {
                 if(j == inList.size()) break;
                 temp.add(inList.get(j++));
             }
             subsets.add(temp);
         }
         //compute skylines of each subset######################################
         subSkyline =  new ArrayList<>();
          for(int f = 0; f < subsets.size(); ++f) {
              List<int[]> t = new ArrayList<>(); 
              subSkyline.add(t);
          }
         for(int k =0; k < subsets.size();++k) {
             baseSkyline(subsets.get(k), subSkyline.get(k));
         }
         //loop#################################################################
         int cnt = 0;
         List<int[]> skylineReturn = new ArrayList<int[]>(); 
         while(!isEmpty() && cnt < K) {
            //find candidate point with smallest first dimension in each subSkyline
            List<int[]> skylineCandidates = new ArrayList<>();
            for(List<int[]> subS :subSkyline) {
                skylineCandidates.add(findOneSkylinePoint(subS));
            }
            //choose the skyline point from candidate skyline points###############
            int[] skylinePoint = findOneSkylinePoint(skylineCandidates);
            //eliminate dominated points and get the remaining list################
            subSkyline = removeDominatedPoints(skylinePoint[1]); //RemainList
            //for(List<int[]> ll:subSkyline) {
                //System.out.format("subSkyline.size() is %d%n", ll.size());
           //}
            skylineReturn.add(skylinePoint); //add to anwser
            ++cnt;
        }
        //System.out.format("reach here%n");
        //foundAll = isEmpty();
        //System.out.format("reach here2%n");
        return skylineReturn;
     }
    /*ToDoubleCheck: what if 2 points has same first dimension but different 2nd
            should select (1,2) over (1,3) since the fommer dominates the latter
            or can leave both
            the latter should not be included in skyline
            MIGHT BE a BUG in baseSkyline
            currently the order is (1,2) (1,3)
            Per SPEC:
             the skyline of P is the set of points in P that are not dominated
             by ANY other point in P . */
     private int[] findOneSkylinePoint(List<int[]> inList) {
        int[] min = new int[2];
        min[0] = Integer.MAX_VALUE;
        for(int[] point:inList) { 
            if( point[0] < min[0]) {
                min = point;
            } else if(point[0] == min[0]) {
                if(point[1] < min[1]) {
                    min = point;
                }
            }
        }
        return min;
     }
     //to reduce latency, don't delete in place; instead add the remained to 
     //a new list
     public List<List<int[]>> removeDominatedPoints(int maxSecD) {
        /*for(int i = 0; i < inList.size(); ++i) {
                if(inList.get(i)[1] < maxSecD) { //so won't include itself
                 outList.add(new int[]{inList.get(i)[0], inList.get(i)[1]});
            } 
        }     
        */
        //System.out.format("max SecD is %d%n", maxSecD);
        List<List<int[]>> toRet = new ArrayList<>();
        for(List<int[]> oneSet : subSkyline) {
            List<int[]> tempSet = new ArrayList<int[]>();
            for(int[] onePoint : oneSet) {
                if(onePoint[1] < maxSecD) { //should copy instead of removing
                    tempSet.add(onePoint);
                }
            }
            toRet.add(tempSet);
        }
        return toRet;
    }
     
    private boolean isEmpty(){
        for(List<int[]> l: subSkyline) {
            if (l.size() > 0) {
                //System.out.format("lsize is %d%n", l.size());
                //for(int[] p:l) System.out.format("p = [%d,%d] %n", p[0],p[1]);
                //System.out.format("Not empty%n");
                return false;
            } 
        }
        return true;
     } 
     //input points and return skyline
     public List<int[]> twoDSkyline(List<int[]> inList) {
         //for(int t = 1)
         List<int[]> ans;
         int K = 140;
         int t = 3;
         while(true) {
             ans = Kskyline(inList,K);
             if(isEmpty())return ans; 
             K = Math.min(inList.size(), (int)Math.pow(2, Math.pow(2, t)));
             ++t;
         }
     }
}
