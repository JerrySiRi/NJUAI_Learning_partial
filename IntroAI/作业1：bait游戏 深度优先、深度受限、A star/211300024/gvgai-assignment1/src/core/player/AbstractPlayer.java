package core.player;

import java.awt.Graphics2D;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import core.game.StateObservation;
import ontology.Types;
import tools.ElapsedCpuTimer;

/**
 * Created with IntelliJ IDEA.
 * User: ssamot
 * Date: 14/11/13
 * Time: 13:42
 * This is a Java port from Tom Schaul's VGDL - https://github.com/schaul/py-vgdl
 */
public abstract class AbstractPlayer {

    /**
     * File where the actions played in a given game are stored.
     */
    private String actionFile;
    //这个游戏所有的可以发出的动作

    /**
     * Writer for the actions file.
     */
    private BufferedWriter writer;

    /**
     * Set this variable to FALSE so that to avoid logging the actions to a file.
     */
    private static final boolean SHOULD_LOG = true;

    /**
     * Last action executed by this agent.
     */
    private Types.ACTIONS lasAction = null;
    //最后一次agent实施的动作。Types.ACTIONS是一个在Types.java中定义的枚举类型，返回值如下。
/*
* ACTION_NIL(new int[]{0}),
* ACTION_UP(new int[]{KeyEvent.VK_UP}),
* ACTION_LEFT(new int[]{KeyEvent.VK_LEFT}),
* ACTION_DOWN(new int[]{KeyEvent.VK_DOWN}),
* ACTION_RIGHT(new int[]{KeyEvent.VK_RIGHT}),
* ACTION_USE(new int[]{KeyEvent.VK_SPACE}),
* ACTION_ESCAPE(new int[]{KeyEvent.VK_ESCAPE});
 */


    /**
     * Picks an action.
     * This function is called every game step to request an
     * action from the player.(这个函数需要玩家在每一轮都给予这个函数一个动作)
     * The action returned must be contained in the
     * actions accessible from stateObs.（每一个动作需要在stateObs中可以识别-合法的）
     * getAvailableActions(), or no action will be applied.
     *
     * @param stateObs Observation of the current state.
     * @param elapsedTimer Timer when the action returned is due.
     * @return An action for the current state
     */
    public abstract Types.ACTIONS act(StateObservation stateObs, ElapsedCpuTimer elapsedTimer);
//抽象类，只做声明，不能做定义。之后再继承了这个类的子类之中再重写在这个act 方法（返回值是Types.ACTIONS类型）

    /**
     * Function called when the game is over. This method must finish before CompetitionParameters.
     * TEAR_DOWN_TIME,or the agent will be DISQUALIFIED
     * @param stateObservation the game state at the end of the game
     * @param elapsedCpuTimer timer when this method is meant to finish.
     */
    public void result(StateObservation stateObservation, ElapsedCpuTimer elapsedCpuTimer)
    {

    }


    /**
     * This function sets up the controller to save the actions executed in a given game.
     * @param actionFile file to save the actions to.
     * @param randomSeed Seed for the sampleRandom generator of the game to be played.
     */
    final public void setup(String actionFile, int randomSeed) {
        this.actionFile = actionFile;

        try {
            if(this.actionFile!=null && SHOULD_LOG)
            {
                writer = new BufferedWriter(new FileWriter(new File(this.actionFile)));
                writer.write(randomSeed + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Closes the agent, writing actions to file.
     */
    final public void teardown() {
        try {
            if(writer!=null) {
                writer.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Logs a single action
     * @param action the action to log.
     */
    final public void logAction(Types.ACTIONS action) {

        lasAction = action;
        if(writer!=null && SHOULD_LOG) {
            try {
                writer.write(action.toString() + "\n");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }

    /**
     * Gets the last action executed by this controller.
     * @return the last action
     */
    public Types.ACTIONS getLastAction()
    {
        return lasAction;
    }

    /**
     * Gets the player the control to draw something on the screen.
     * It can be used for debug purposes.
     * @param g Graphics device to draw to.
     */
    public void draw(Graphics2D g)
    {
        //Overwrite this method in your controller to draw on the screen.
        //This method should be left empty in this class.
    }


}
