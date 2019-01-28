/* =======================================================================
   A generic GUI for the JDBC project

   You may use this GUI in your CS377 project if you don't want to
   make a "nice looking one"

   Author: Shun Yan Cheung
   ======================================================================= */

import java.awt.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;

import java.awt.event.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.sql.*;
import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;

public class RelAlg
{
   static String path="";
   //static HashMap<String,Relation> relations=new HashMap<String,Relation> (Relation.storeallrelation(path));
	static HashMap<String,Relation> relations=new HashMap<String,Relation> ();
	
   final static char sigma = (char) 963;
   final static char pi = (char) 960;
   final static char join = (char) 10781;
   final static char cartprod = (char) 10799;
   final static char setFunc = (char) 8497;
   final static char intersect = (char) 8745;
   final static char union = (char) 8746;
   final static char minus = (char) 8722;
   final static char divide = (char) 247;

   public static JFrame mainFrame;

   public static JLabel DBName = new JLabel("Database: ");
   public static JTextField Db = new JTextField();
   public static JButton Select = new JButton("Select");
   public static JButton ShowAllRel = new JButton("ShowAllRel");
   public static JButton Execute = new JButton("Execute");


   public static JButton Sigma     = new JButton("" + sigma);
   public static JButton Pi        = new JButton("" + pi);
   public static JButton Join      = new JButton("" + join);
   public static JButton CartProd  = new JButton("" + cartprod);
   public static JButton SetFunc   = new JButton("" + setFunc);
   public static JButton Intersect = new JButton("" + intersect);
   public static JButton Union     = new JButton("" + union);
   public static JButton Minus     = new JButton("" + minus);
   public static JButton Divide    = new JButton("" + divide);
   public static JButton Assign    = new JButton("H =");

   public static JTextArea Input = new JTextArea();
   public static JTable Output = new JTable();
 


   public static void main( String[] args )
   {
	  path=args[0];
      Font ss_font = new Font("SansSarif",Font.BOLD,24) ;
      Font ms_font = new Font("Monospaced",Font.BOLD,16) ;




      JPanel P1 = new JPanel();   // Top panel
      JPanel P2 = new JPanel();

      P1.setLayout( new BorderLayout() );
      P2.setLayout( new BorderLayout() );

      /* =============================================
         Make top panel
         ============================================= */
      JScrollPane d1 = new JScrollPane(Input, 
                                       JScrollPane.VERTICAL_SCROLLBAR_ALWAYS ,
                                       JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
      Input.setFont( ss_font );

      JPanel s1 = new JPanel(); // Side panel
      s1.setLayout( new GridLayout( 8,1 ) );
      s1.add( DBName );
      s1.add( Db );
      Db.setFont( ss_font );
      s1.add( Select );
      s1.add(ShowAllRel);
      s1.add( Execute );
      Execute.setPreferredSize(new Dimension(140, 30)) ;

      P1.add(d1, "Center");
      P1.add(s1, "East");

      /* =============================================
         Make bottom panel
         ============================================= */
      JScrollPane d2 = new JScrollPane(Output,
                                       JScrollPane.VERTICAL_SCROLLBAR_ALWAYS ,
                                       JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);

      //Output.setFont( ms_font );
      Output.setFont(new Font("Serif",Font.PLAIN,18));
      Output.getTableHeader().setFont( new Font( "Arial" , Font.BOLD, 22));
      Output.setGridColor(Color.LIGHT_GRAY);
      Output.setRowHeight(22);
      //Output.setEditable(false);


      JPanel s2 = new JPanel(); // Side panel
      s2.setLayout( new GridLayout( 10,1 ) );

      Font OpFont = new Font("Monospaced",Font.BOLD,30) ;

      s2.add( Sigma);
      Sigma.setPreferredSize(new Dimension(140, 30)) ;
      Sigma.setFont( OpFont );

      s2.add( Pi);
      Pi.setFont( OpFont );
      s2.add( Join);
      Join.setFont( OpFont );
      s2.add( CartProd);
      CartProd.setFont( OpFont );
      s2.add( SetFunc);
      SetFunc.setFont( OpFont );
      s2.add( Intersect);
      Intersect.setFont( OpFont );
      s2.add( Union);
      Union.setFont( OpFont );
      s2.add( Minus);
      Minus.setFont( OpFont );
      s2.add( Divide);
      Divide.setFont( OpFont );
      s2.add( Assign);
      Assign.setFont( OpFont );


      P2.add(d2, "Center");
      P2.add(s2, "East");

      mainFrame = new JFrame("Relational Algebra tool");
      mainFrame.getContentPane().setLayout( new GridLayout(2,1) );
      mainFrame.getContentPane().add( P1 );
      mainFrame.getContentPane().add( P2 );
      mainFrame.setSize(900, 700);

      Select.addActionListener(new SelectListener() );  // Make Select active
      ShowAllRel.addActionListener(new ShowAllRelListener());
      Execute.addActionListener(new ExecuteListener());
      Sigma.addActionListener(new SigmaListener() );
      Pi.addActionListener(new PiListener() );  
      Join.addActionListener(new JoinListener() );  
      CartProd.addActionListener(new CartProdListener() );  
      SetFunc.addActionListener(new SetFuncListener() );  
      Intersect.addActionListener(new IntersectListener() );  
      Union.addActionListener(new UnionListener() );  
      Minus.addActionListener(new MinusListener() );  
      Divide.addActionListener(new DivideListener() );  
      Assign.addActionListener(new AssignListener() );  

      mainFrame.setVisible(true);
      //mainFrame.pack();
   }


   static class SigmaListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();   //get the cursor position
         Input.insert(sigma + "(c) (R)", pos); //insert text
      }
   }

   static class PiListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition(); 
         Input.insert(pi + "(c) (R)", pos); 
      }
   }

   static class JoinListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();   
         Input.insert( "R1 " + join + "(c) R2", pos);    
      }
   }

   static class CartProdListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( "R1 " + cartprod + " R2", pos); 
      }
   }

   static class SetFuncListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( (char)947 + "(a)" + setFunc + "(a)(R)", pos);
      }
   }

   static class IntersectListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( "R1 " + intersect + " R2", pos);
      }
   }

   static class UnionListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( "R1 " + union + " R2", pos);
      }
   }

   static class MinusListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( "R1 " + minus + " R2", pos);
      }
   }

   static class DivideListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( "R1 " + divide + " R2", pos);
      }
   }

   static class AssignListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
         int pos = Input.getCaretPosition();
         Input.insert( "Set H = ", pos);
      }
   }

   static class ShowAllRelListener implements ActionListener
   {
      public void actionPerformed(ActionEvent e)
      {
    	  String[] columns=new String[2];
    	  columns[0]="RelName";
    	  columns[1]="AttriName";
    	  int num=relations.size();
    	  String[][] data=new String[num][2];
    	  int i=0;
    	  for(Relation rel:relations.values()){
    		  data[i][0]=rel.relationname;
    		  StringBuilder attris=new StringBuilder();
    		  for(java.util.List<String> list:rel.attributename){
    			  attris.append(list.get(0));
    			  attris.append(", ");
    			  
    		  }
    		  attris.deleteCharAt(attris.length()-1);
    		  attris.deleteCharAt(attris.length()-1);
    		  data[i][1]=attris.toString();
    		  i++;
    	  }
    	  DefaultTableModel model = new DefaultTableModel(data, columns);
    	  Output.setModel( model );
      }
   }


   static class ExecuteListener implements ActionListener            
   {  
      public void actionPerformed(ActionEvent e)
      {    	 
    	  String name=Input.getText();
    	  Relation r= parse(relations,name);
    	  
    	  
  	      
    	  if(r!=null && r.relationname!=null && (r.relationname.equals("ambiguous")||r.relationname.equals("nullname")
    			  ||(r.relationname.length()>9 && r.relationname.substring(0,9).equals("nullattri")))){
    		  String[] columns=new String[1];
    		  columns[0]="Execute Error Message";
    		  String[][] data=new String[1][1];
    		  if(r.relationname.equals("ambiguous")){
    			  data[0][0]="Relation alg expression produces ambiguous attibute names.";
    		  }
    		  else if(r.relationname.equals("nullname")){
    			  data[0][0]="Can not find the input Relation:"+r.attributetype.get(0);
    		  }
    		  else if(r.relationname.substring(0,9).equals("nullattri")) {
    			  data[0][0]="Can not find the input Attribute:"+r.relationname.substring(9,r.relationname.length());
    		  }
    		  
    		  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    	  }
    	  else if(r==null){
    		  String[] columns=new String[1];
    		  columns[0]="Execute Null Error Message";
    		  String[][] data=new String[1][1];
    		  data[0][0]="Your input is invalid.";
    		  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    	  }
    	  
    	  else{
    		  int attrisize=r.attributename.size();
        	  int tuplesize=r.tuplesindata.size();
        	  String[] columns=new String[attrisize];
        	  String[][] data=new String[tuplesize][attrisize];
        	  for(int i=0;i<attrisize;i++){
        		  String attri=r.attributename.get(i).get(0);
        		  columns[i]=attri;
        	  }
        	  
        	  for(int j=0;j<tuplesize;j++){
        		  data[j]=r.tuplesindata.get(j).toArray(new String[attrisize]);
        	  }
        	  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    	  }
   
      }
   }
   
   static class SelectListener implements ActionListener            
   {  
      public void actionPerformed(ActionEvent e)
      {  
    	  String name=Db.getText();
    	  path=path+"/"+name+"/";
    	  Boolean exist=true;
    	  try {
    	        
    	        File f = new File(path);
    	        Scanner scan = new Scanner(f);
    	        scan.close();
    	    } catch (FileNotFoundException ee) {
    	        //System.out.println("File Not Found.");
    	        exist=false;
    	     
          	  	String[] columns=new String[1];
          	  	columns[0]=name+" Not Found.";
          	  	String[][] data=new String[1][1];
          	  	DefaultTableModel model = new DefaultTableModel(data, columns);
          	  	Output.setModel( model );
    	    }
    	  if(exist=true){
    		  relations=new HashMap<String,Relation> (Relation.storeallrelation(path));
        	  String[] columns=new String[1];
    		  columns[0]=name+" is selected.";
    		  String[][] data=new String[1][1];
    		  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    	  }
    	  
    	 
    	 /* 
    	  if(r==null){
    		  String[] columns=new String[1];
    		  columns[0]="Select Null Error Message";
    		  String[][] data=new String[1][1];
    		  data[0][0]="Your input is invalid.";
    		  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    	  }
    	  else if(r.relationname.equals("nullname")){
    		  String[] columns=new String[1];
    		  columns[0]="Select Null Error Message";
    		  String[][] data=new String[1][1];
    		  data[0][0]="Can not find the input Relation.";
    		  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    		  
    	  }
    	  else{
    		  int attrisize=r.attributename.size();
        	  int tuplesize=r.tuplesindata.size();
        	  String[] columns=new String[attrisize];
        	  String[][] data=new String[tuplesize][attrisize];
        	  for(int i=0;i<attrisize;i++){
        		  String attri=r.attributename.get(i).get(0);
        		  columns[i]=attri;
        	  }
        	  
        	  for(int j=0;j<tuplesize;j++){
        		  data[j]=r.tuplesindata.get(j).toArray(new String[attrisize]);
        	  }
        	  

        	  DefaultTableModel model = new DefaultTableModel(data, columns);
        	  Output.setModel( model );
    	  }*/
      }
   }
   
   private static Relation parse(HashMap<String,Relation> relations,String input) {
		Relation r = null;
		//boolean error=false;
		try {
			r= MyRelation.getparseresult(input,relations);
		} catch (Exception e) {
			System.out.println("Error during Parsing");
			e.printStackTrace();
		}
		return r;
	}
}
