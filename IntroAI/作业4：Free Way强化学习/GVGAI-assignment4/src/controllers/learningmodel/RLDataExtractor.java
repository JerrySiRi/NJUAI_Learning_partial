/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package controllers.learningmodel;

import tools.*;
import core.game.Observation;
import core.game.StateObservation;

import java.io.FileWriter;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Observable;

import ontology.Types;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;

/**
 *
 * @author yuy
 */

//【【【特征提取方法】】】
public class RLDataExtractor {
    public FileWriter filewriter;
    public static Instances s_datasetHeader = datasetHeader();
    
    public RLDataExtractor(String filename) throws Exception{

        //自动创建一个给weka可以识别到的、收集了数据的文件来进行训练。
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
    
    public static Instance makeInstance(double[] features, int action, double reward){
        features[872] = action;
        features[873] = reward;
        Instance ins = new Instance(1, features);
        ins.setDataset(s_datasetHeader);
        return ins;
    }

    //特征提取
    public static double[] featureExtract(StateObservation obs){

        //存放特征的数组
        double[] feature = new double[886];  // 868 + 10 + 1(action) + 1(Q)
        //原来是874

        /*增加的特征提取*/
        Vector2d avatar_cur_pos=obs.getAvatarPosition();//【当前avatar的位置】

        double dist_to_distination=0;//【距离目标位置的距离】
        double y_to_distination=0;//【竖向到目标位置的距离】
        double x_to_distination=0;//【竖向到目标位置的距离】

        double zhang_min_shang=0;//【当前距离avatar最近的上、下、左、右障碍物的距离是多少】
        double zhang_min_xia=0;
        double zhang_min_zuo=0;
        double zhang_min_you=0;

        double ge_min_shang=0;//【当前距离avatar最近的上一行、同行、下一行最近的红黄格子距离是多少】
        double ge_min_xia=0;
        double ge_min_you=0;
        double ge_min_zuo=0;





        // 448 locations
        int[][] map = new int[28][31];       //其中28*31=868
        // Extract features
        //把当前状态（可以看做一张图）中的信息提取出来
        LinkedList<Observation> allobj = new LinkedList<>();


        //【potential option2】
        if( obs.getImmovablePositions()!=null ){//把所有不可动的物体的位置信息收集
            for(ArrayList<Observation> l : obs.getImmovablePositions()) {
                    allobj.addAll(l);
                for(Observation o:l){
                    if(avatar_cur_pos.y==o.position.y){//当前不可移动的障碍物和avatar在一条水平线上
                        if(o.position.x<avatar_cur_pos.x)//左[没加28的时候]
                            if(zhang_min_zuo==0)
                                zhang_min_zuo=avatar_cur_pos.x-zhang_min_zuo;
                            else
                                zhang_min_zuo=Math.min(zhang_min_zuo,avatar_cur_pos.x-zhang_min_zuo);

                        if(o.position.x>avatar_cur_pos.x)//右
                            if(zhang_min_you==0)
                                zhang_min_you=zhang_min_you-avatar_cur_pos.x;
                            else
                                zhang_min_you=Math.min(zhang_min_you,zhang_min_you-avatar_cur_pos.x);
                    }
                    if(avatar_cur_pos.x==o.position.x){//当前不可移动的障碍物和avatar在一条水平线上
                        if(o.position.y<avatar_cur_pos.y)//下
                            if(zhang_min_xia==0)
                                zhang_min_xia=avatar_cur_pos.y-zhang_min_xia;
                            else
                                zhang_min_xia=Math.min(zhang_min_xia,avatar_cur_pos.x-zhang_min_xia);
                        if(o.position.y>avatar_cur_pos.y)//上
                            if(zhang_min_shang==0)
                                zhang_min_shang=zhang_min_shang - avatar_cur_pos.y;
                            else
                                zhang_min_shang=Math.min(zhang_min_shang,zhang_min_shang-avatar_cur_pos.y);
                    }
                }
            }
        }

        //【potential option 3】
        if( obs.getMovablePositions()!=null ){//把所有可动的物体的位置信息收集
            for(ArrayList<Observation> l : obs.getMovablePositions()) {
                allobj.addAll(l);
                for(Observation o:l){
                    if(avatar_cur_pos.y==o.position.y){//当前不可移动的障碍物和avatar在一条水平线上
                        if(o.position.x<avatar_cur_pos.x)//左
                            if(ge_min_zuo==0)
                                ge_min_zuo=avatar_cur_pos.x-ge_min_zuo;
                            else
                                ge_min_zuo=Math.min(ge_min_zuo,avatar_cur_pos.x-ge_min_zuo);

                        if(o.position.x>avatar_cur_pos.x)//右
                            if(ge_min_you==0)
                                ge_min_you=ge_min_you-avatar_cur_pos.x;
                            else

                                ge_min_you=Math.min(ge_min_you,ge_min_you-avatar_cur_pos.x);
                    }
                    if(avatar_cur_pos.x==o.position.x){//当前不可移动的障碍物和avatar在一条水平线上
                        if(o.position.y<avatar_cur_pos.y)//下
                            if(ge_min_xia==0)
                                ge_min_xia=avatar_cur_pos.y-ge_min_xia;
                            else
                                ge_min_xia=Math.min(ge_min_xia,avatar_cur_pos.x-ge_min_xia);
                        if(o.position.y>avatar_cur_pos.y)//上
                            if(ge_min_shang==0)
                                ge_min_shang=ge_min_shang - avatar_cur_pos.y;
                            else
                                ge_min_shang=Math.min(ge_min_shang,ge_min_shang-avatar_cur_pos.y);
                    }
                }
            }

        }

        //if( obs.getNPCPositions()!=null )//NPC的位置收集
            //for(ArrayList<Observation> l : obs.getNPCPositions()) allobj.addAll(l);
        if(obs.getPortalsPositions()!=null)//目标位置信息收集【potential option1】
            for(ArrayList<Observation> l:obs.getPortalsPositions()) allobj.addAll(l);



        //【potential option1】
        for(Observation o:allobj){
            Vector2d dis=o.position;
            if(o.itype==4){
                dist_to_distination=avatar_cur_pos.dist(dis);//距离目标位置的距离
                y_to_distination=dis.y-avatar_cur_pos.y;//和目标位置纵坐标的差距
                x_to_distination=Math.abs(dis.x-avatar_cur_pos.x);;//【竖向到目标位置的距离】
            }
        }






        //对收集到的信息进行预处理
        for(Observation o : allobj){
            Vector2d p = o.position;
            int x = (int)(p.x/28); //size is 28 for FreeWay
            int y= (int)(p.y/28);
            map[x][y] = o.itype;
        }

        //向特征数组中把收集到的处理过的信息加入进去
        for(int y=0; y<31; y++)
            for(int x=0; x<28; x++)
                feature[y*28+x] = map[x][y];

        //4个游戏状态信息
        // 4 states
        feature[868] = obs.getGameTick();
        feature[869] = obs.getAvatarSpeed();
        feature[870] = obs.getAvatarHealthPoints();
        feature[871] = obs.getAvatarType();
        feature[872] =dist_to_distination;
        feature[873] =y_to_distination;
        feature[874] =zhang_min_shang;
        feature[875] =zhang_min_xia;
        feature[876] =zhang_min_zuo;
        feature[877] =zhang_min_you;
        feature[878] =ge_min_shang;
        feature[879] =ge_min_xia;
        feature[880] =ge_min_zuo;
        feature[881] =ge_min_you;
        feature[882] =x_to_distination;


        return feature;
    }
    
    public static Instances datasetHeader(){
        
        if (s_datasetHeader!=null)
            return s_datasetHeader;
        
        FastVector attInfo = new FastVector();
        // 448 locations
        for(int y=0; y<28; y++){
            for(int x=0; x<31; x++){
                Attribute att = new Attribute("object_at_position_x=" + x + "_y=" + y);
                attInfo.addElement(att);
            }
        }
        Attribute att = new Attribute("GameTick" ); attInfo.addElement(att);
        att = new Attribute("AvatarSpeed" ); attInfo.addElement(att);
        att = new Attribute("AvatarHealthPoints" ); attInfo.addElement(att);
        att = new Attribute("AvatarType" ); attInfo.addElement(att);
        att = new Attribute("dist_to_distination" ); attInfo.addElement(att);
        att = new Attribute("y_to_distination" ); attInfo.addElement(att);
        att = new Attribute("zhang_min_shang" ); attInfo.addElement(att);
        att = new Attribute("zhang_min_xia" ); attInfo.addElement(att);
        att = new Attribute("zhang_min_zuo" ); attInfo.addElement(att);
        att = new Attribute("zhang_min_you" ); attInfo.addElement(att);
        att = new Attribute("ge_min_shang" ); attInfo.addElement(att);
        att = new Attribute("ge_min_xia" ); attInfo.addElement(att);
        att = new Attribute("ge_min_zuo" ); attInfo.addElement(att);
        att = new Attribute("ge_min_you" ); attInfo.addElement(att);
        att = new Attribute("x_to_distination" ); attInfo.addElement(att);

        //action
        FastVector actions = new FastVector();
        actions.addElement("0");
        actions.addElement("1");
        actions.addElement("2");
        actions.addElement("3");
        actions.addElement("4");
        actions.addElement("5");
        actions.addElement("6");
        actions.addElement("7");
        actions.addElement("8");
        actions.addElement("9");
        actions.addElement("10");
        actions.addElement("11");
        actions.addElement("12");
        actions.addElement("13");
        att = new Attribute("actions", actions);        
        attInfo.addElement(att);
        // Q value
        att = new Attribute("Qvalue");
        attInfo.addElement(att);
        
        Instances instances = new Instances("PacmanQdata", attInfo, 0);
        instances.setClassIndex( instances.numAttributes() - 1);
        
        return instances;
    }
    
}
