/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tools;

import core.game.Observation;
import core.game.StateObservation;

import java.io.FileWriter;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Observable;

import ontology.Types;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instances;

/**
 *
 * @author yuy
 */
public class Recorder {
    public FileWriter filewriter;
    public static Instances s_datasetHeader = datasetHeader();
    
    public Recorder(String filename) throws Exception{
        
        filewriter = new FileWriter(filename+".arff");
        filewriter.write(s_datasetHeader.toString());
        /*
                // ARFF File header
        filewriter.write("@RELATION AliensData\n");
        // Each row denotes the feature attribute
        // In this demo, the features have four dimensions.
        filewriter.write("@ATTRIBUTE gameScore  NUMERIC\n");
        filewriter.write("@ATTRIBUTE avatarSpeed  NUMERIC\n");
        filewriter.write("@ATTRIBUTE avatarHealthPoints NUMERIC\n");
        filewriter.write("@ATTRIBUTE avatarType NUMERIC\n");
        // objects
        for(int y=0; y<14; y++)
            for(int x=0; x<32; x++)
                filewriter.write("@ATTRIBUTE object_at_position_x=" + x + "_y=" + y + " NUMERIC\n");
        // The last row of the ARFF header stands for the classes
        filewriter.write("@ATTRIBUTE Class {0,1,2}\n");
        // The data will recorded in the following.
        filewriter.write("@Data\n");*/
        
    }
    //提取特征和保存数据文件的代码
    public static double[] featureExtract(StateObservation obs){
        int N=3;
        double[] feature = new double[5+448*N];  // 448 + 4 + 1(class)
        
        // 448 locations
        int[][] map = new int[32][14];
        // Extract features
        //所有要存的位置信息都放到了这个集合之中！
        LinkedList<Observation> allobj = new LinkedList<>();

        //不可移动的位置（好像没东西呀）
        //Observations of immovable sprites in the game
        //此时getImmovablePositions返回的是集合的集合
        if( obs.getImmovablePositions()!=null )
            for(ArrayList<Observation> l : obs.getImmovablePositions())
                allobj.addAll(l);

        //可移动的位置（玩家）
        //Returns a list of observations of sprites that move, but are NOT NPCs in the game.
        if( obs.getMovablePositions()!=null )
            for(ArrayList<Observation> l : obs.getMovablePositions())
                allobj.addAll(l);
        
        //NPC的位置（敌人）
        //Observations of NPCs in the game
        if( obs.getNPCPositions()!=null )
            for(ArrayList<Observation> l : obs.getNPCPositions())
                allobj.addAll(l);

        
        for(Observation o : allobj){//allobj中存放的是元素类型为Observation的集合，可以直接访问集合的元素呢！（跨过集合符号！）
            Vector2d p = o.position;//存放各个二维坐标
            int x = (int)(p.x/25);
            int y= (int)(p.y/25);
            map[x][y] = o.itype;
        }
        for(int y=0; y<14; y++)
            for(int x=0; x<32; x++)
                feature[y*32+x] = map[x][y];

        for(int k=0; k<N; k++)
            for(int y=0; y<14; y++)
                for(int x=0; x<32; x++)
                    feature[k*448+y*32+x] = map[x][y];
        
        // 4 states
        //确实也都在weka之中看到了他们四个的信息，但不是存在了同一个位置吗？
        feature[448*N] = obs.getGameTick();
        feature[448*N+1] = obs.getAvatarSpeed();
        feature[448*N+2] = obs.getAvatarHealthPoints();//玩家剩余的血量
        feature[448*N+3] = obs.getAvatarType();
       return feature;
    }
    
    //准备数据集的格式信息--要保持和提取的特征一致！
    public static Instances datasetHeader(){
        FastVector attInfo = new FastVector();
        // 448 locations
        for (int k = 0; k<3; k++){
            for(int y=0; y<14; y++){
                for(int x=0; x<32; x++){
                    Attribute att = new Attribute("num of time" + k + "object_at_position_x=" + x + "_y=" + y);
                    attInfo.addElement(att);
                }
            }
        }
        Attribute att = new Attribute("GameTick" ); attInfo.addElement(att);
        att = new Attribute("AvatarSpeed" ); attInfo.addElement(att);
        att = new Attribute("AvatarHealthPoints" ); attInfo.addElement(att);
        att = new Attribute("AvatarType" ); attInfo.addElement(att);
        //class
        FastVector classes = new FastVector();
        classes.addElement("0");
        classes.addElement("1");
        classes.addElement("2");
        classes.addElement("3");
        att = new Attribute("class", classes);        
        attInfo.addElement(att);
        
        Instances instances = new Instances("AliensData", attInfo, 0);
        instances.setClassIndex( instances.numAttributes() - 1);
        
        return instances;
    }
    
    //记录特征和玩家按下的按键
    // Record each move as the ARFF instance
    public void invoke(StateObservation obs, Types.ACTIONS action) {
        double[]  feature = featureExtract(obs);
        
        try{  
            for(int i=0; i<feature.length-1; i++)
                filewriter.write(feature[i] + ",");
            // Recorde the move type as ARFF classes
            int action_num = 0;
            if( Types.ACTIONS.ACTION_NIL == action) action_num = 0;
            if( Types.ACTIONS.ACTION_USE == action) action_num = 1;
            if( Types.ACTIONS.ACTION_LEFT == action) action_num = 2;
            if( Types.ACTIONS.ACTION_RIGHT == action) action_num = 3;
            filewriter.write(action_num + "\n");
            filewriter.flush();
        }catch(Exception exc){
            exc.printStackTrace();
        }
    }
    
    public void close(){
        try{
            filewriter.close();
        }catch(Exception exc){
            exc.printStackTrace();
        }
    }
}
