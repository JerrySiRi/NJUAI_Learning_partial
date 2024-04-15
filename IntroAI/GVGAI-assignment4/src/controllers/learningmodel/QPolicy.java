/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package controllers.learningmodel;

import core.game.StateObservation;
import java.util.HashMap;
import java.util.Random;
import ontology.Types;
import weka.classifiers.Classifier;
import weka.classifiers.trees.REPTree;
import weka.core.Instance;
import weka.core.Instances;
/**
 *
 * @author yuy
 */

//【【【策略对象】】】
public class QPolicy {
    protected double m_epsilon=0.4;//epsilon-greedy的算法，参数是0.3【有0.3的概率探索，0.7的概率利用现有最好的】
    protected Classifier m_c;
    protected Instances m_dataset;
    protected Random m_rnd;
    protected int m_numActions;
    
    //构造函数
    public QPolicy(int N_ACTIONS){
        m_numActions = N_ACTIONS;
        m_dataset = RLDataExtractor.datasetHeader();//当前收集到的特征
        m_rnd = new Random();
        m_c = null;
    }

    //进行的epsilon greedy的参数初始化呢！
    public void setEpsilon(double epsilon){
        m_epsilon = epsilon;
    }
    
    // max Q action without epsilon-greedy 【全部进行利用（不探索了）】
    public int getActionNoExplore(double[] feature) throws Exception{
        double[] Q = getQArray(feature);
        
        // find best action according to Q value
        int bestaction = 0;
        for(int action=1; action<m_numActions; action++){//对总动作数进行遍历，选出收益最高的那个动作捏
            // get Q value from the prediction model【Q中存的是期望模型中对当前状态收益的估计】
            if( Q[bestaction] < Q[action] ){
                bestaction = action;
            }
        }
        // among the same best actions, choose a random one
        int sameactions =0;
        for(int action=bestaction+1; action<m_numActions; action++){
            if(Q[bestaction] == Q[action]){
                sameactions++;
                if( m_rnd.nextDouble() < 1.0/(double)sameactions )
                    bestaction = action;
            }
        }
        
        return bestaction;//选择收益最高的作为此步动作
    }
    
    // max Q action with epsilon-greedy 
    public int getAction(double[] feature,int count) throws Exception{
        double[] Q = getQArray(feature);//拿到了在当前模型下的评估值

        //依据评估值，拿到了最好的动作
        // find best action according to Q value
        int bestaction = 0;
        for(int action=1; action<m_numActions; action++){
            if( Q[bestaction] < Q[action] ){
                bestaction = action;
            }
        }
        //选择最好的那一个（多于一个就随机选）
        //【【【最终返回的是该动作的整数值-----和动作是一一对应的！】】】
        // among the same best actions, choose a random one
        int sameactions =0;
        for(int action=bestaction+1; action<m_numActions; action++){
            if(Q[bestaction] == Q[action]){
                sameactions++;
                if( m_rnd.nextDouble() < 1.0/(double)sameactions )
                    bestaction = action;
            }
        }


        //在初始化的时候给了一个随机值，如果这个随机值比epsilon要小的话，就进行探索【从所有可选动作中随机选择一个！】
        //下一个int值
        double temp=m_epsilon*(1-Math.log10(count/2+1));
        // epsilon greedy
        if( m_rnd.nextDouble() < temp ){
            bestaction = m_rnd.nextInt(m_numActions);
        }
        
        return bestaction;
    }
    
    public double getMaxQ(double[] feature) throws Exception{
        double[] Q = getQArray(feature);
        
        // find best action according to Q value
        int bestaction = 0;
        for(int action=1; action<m_numActions; action++){
            if( Q[bestaction] < Q[action] )
                bestaction = action;
        }
        
        return Q[bestaction];
    }
    
    public double[] getQArray(double[] feature) throws Exception{
        
        double[] Q = new double[m_numActions];
        
        // get Q value from the prediction model
        for(int action = 0; action<m_numActions; action++){
            feature[feature.length-2] = action;//传给weka之中的特征
            feature[feature.length-1] = Double.NaN;
            Q[action] = m_c == null ? 0 : m_c.classifyInstance(makeInstance(feature));
        }
        
        return Q;
    }
    
    public void fitQ(Instances data) throws Exception{
        if( m_c == null ){
            m_c = new weka.classifiers.trees.REPTree();
            ((REPTree)m_c).setMinNum(1);
            ((REPTree)m_c).setNoPruning(true);
        }
        m_c.buildClassifier(data);   
    }
        
    protected Instance makeInstance(double[] vector){
        Instance ins = new Instance(1,vector);
        ins.setDataset(m_dataset);
        return ins;
    }
}
