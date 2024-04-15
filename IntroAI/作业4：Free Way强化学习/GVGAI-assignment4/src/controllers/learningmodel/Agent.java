package controllers.learningmodel;

import controllers.Heuristics.SimpleStateHeuristic;
import controllers.Heuristics.StateHeuristic;
import controllers.Heuristics.WinScoreHeuristic;
import core.game.StateObservation;
import core.player.AbstractPlayer;
import java.io.FileInputStream;
import java.io.ObjectInputStream;
import java.util.HashMap;
import java.util.Random;
import java.util.concurrent.TimeoutException;
import ontology.Types;
import tools.ElapsedCpuTimer;
import tools.Utils;
import weka.classifiers.Classifier;
import weka.core.Instance;
import weka.core.Instances;


//【【【Agent的封装】】】
public class Agent extends AbstractPlayer {

    protected Classifier m_model;
    protected Random m_rnd;
    private static int SIMULATION_DEPTH = 50;
    private final HashMap<Integer, Types.ACTIONS> action_mapping;
    protected QPolicy m_policy;
    protected int N_ACTIONS;
    protected static Instances m_dataset;
    protected int m_maxPoolSize = 1000;
    protected double m_gamma = 0.85;

    public Agent(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {
        m_rnd = new Random();

        // convert numbers to actions
        action_mapping = new HashMap<Integer, Types.ACTIONS>();
        int i = 0;
        for (Types.ACTIONS action : stateObs.getAvailableActions()) {
            action_mapping.put(i, action);
            //action_mapping放的（当前是可以做的第几个动作(i)，当前动作是什么(action)）
            i++;
        }

        N_ACTIONS = stateObs.getAvailableActions().size();//当前可以做的动作总数是多少
        m_policy = new QPolicy(N_ACTIONS);//Qpolicy变量---放的当前可做动作总数、收集到的特征...
        m_dataset = new Instances(RLDataExtractor.s_datasetHeader);
    }

    /**
     *
     * Learning based agent.
     *
     * @param stateObs Observation of the current state.
     * @param elapsedTimer Timer when the action returned is due.
     * @return An action for the current state
     */
    //Agent开始要选出他要做的动作啦！
    public Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer) {

        //m_timer = elapsedTimer;
        //依据此函数获得对不同动作的估计.依据当前所处状态，进行深度20层的搜索
        //
        learnPolicy(stateObs, SIMULATION_DEPTH, new WinScoreHeuristic(stateObs));

        Types.ACTIONS bestAction = null;
        try {
            //获取特征提出出来的信息呢！
            double[] features = RLDataExtractor.featureExtract(stateObs);
            //根据获取的信息来进行对Q值函数的更新
            int action_num = m_policy.getActionNoExplore(features); // no exploration
            bestAction = action_mapping.get(action_num);
        } catch (Exception exc) {
            exc.printStackTrace();
        }

        // System.out.println("====================");
        return bestAction;
    }

    //进行蒙特卡洛取样的模拟？
    //返回的用于weka进行训练的一个实例
    private Instances simulate(StateObservation stateObs, StateHeuristic heuristic, QPolicy policy,int count) {

        Instances data = new Instances(RLDataExtractor.datasetHeader(), 0);
        stateObs = stateObs.copy();

        Instance sequence[] = new Instance[SIMULATION_DEPTH];//对每个深度都创建一个实例用于存储
        int depth = 0;
        double factor = 1;
        for (; depth < SIMULATION_DEPTH; depth++) {
            try {
                double[] features = RLDataExtractor.featureExtract(stateObs);

                int action_num = policy.getAction(features,count);// max Q action with epsilon-greedy
                //拿到了“最好”动作（可能是随机的探索）所对应的数字！

                //启发式函数评价当前局面
                double score_before = heuristic.evaluateState(stateObs);


                //在这个哈希集合之中找到拿到“最好”动作的数字所对应的动作！
                // simulate
                Types.ACTIONS action = action_mapping.get(action_num);

                stateObs.advance(action);//往后走一步


                //评价走完一步的局面
                double score_after = heuristic.evaluateState(stateObs);


                //走一步之后的分数之差
                double delta_score = factor * (score_after - score_before);
                //此factor会不断减小，0.99*0.99*0.99...
                //【【【在程序不断运行的时候走一步的回报所占的比例会越来越小】】】
                factor = factor * m_gamma;
                //收集走了当前步（以action_num来表示）之后，拿到的回报或者乘法是多少，传到DataExtractor之中
                // collect data
                sequence[depth] = RLDataExtractor.makeInstance(features, action_num, delta_score);

            } catch (Exception exc) {
                exc.printStackTrace();
                break;
            }
            if (stateObs.isGameOver()) {
                depth++;
                break;
            }
        }

        // get the predicted Q from the last state
        double accQ = 0;
        if (!stateObs.isGameOver()) {
            try {
                accQ = factor*policy.getMaxQ(RLDataExtractor.featureExtract(stateObs));
            } catch (Exception exc) {
                exc.printStackTrace();
            }
        }

        // calculate the acumulated Q
        for (depth = depth - 1; depth >= 0; depth--) {
            accQ += sequence[depth].classValue();
            sequence[depth].setClassValue(accQ);
            data.add(sequence[depth]);
        }
        return data;
    }

    private void learnPolicy(StateObservation stateObs, int maxdepth, StateHeuristic heuristic) {

        // assume we need SIMULATION_DEPTH*10 milliseconds for one iteration
        int iter = 0;
        while (iter++ <= 10 //truem_timer.remainingTimeMillis() > SIMULATION_DEPTH*10
                ) {

            // get training data of the MC sampling
            //【进行蒙特卡洛取样】
            /*
            *蒙特卡洛方法是通过平均样本的回报来解决强化学习问题
            * 其通过多次采样来对潜在的搜索空间进行描述
            * 使用均值来近似价值
            * */
            //拿到了weka用于训练的一个实例(里边放了各个收集的特征状态)
            Instances dataset = simulate(stateObs, heuristic, m_policy,iter);

            // update dataset
            m_dataset.randomize(m_rnd);
            //在状态数量没有过多的时候，就加入到用于weka训练的instance变量m_dataset之中
            // 【此步把收集到的dataset中所有状态全部加进去啦】
            for (int i = 0; i < dataset.numInstances(); i++) {
                m_dataset.add(dataset.instance(i)); // add to the last
            }
            //【程序设置了最大收集状态数，所以如果超了的话，就会删除一部分状态，直到不超过最大状态数】
            while (m_dataset.numInstances() > m_maxPoolSize) {
                m_dataset.delete(0);
            }
        }
        // train policy
        /*
        * public void fitQ(Instances data) throws Exception{
        if( m_c == null ){
            m_c = new weka.classifiers.trees.REPTree();
            ((REPTree)m_c).setMinNum(1);
            ((REPTree)m_c).setNoPruning(true);
        }
        m_c.buildClassifier(data);
    }
        * */
        //本实验，使用weka中REPTree来对收集的数据进行训练
        //降低错误率剪枝算法 Reduce Error Pruning
        try {
            m_policy.fitQ(m_dataset);
        } catch (Exception exc) {
            exc.printStackTrace();
        }
    }
}
