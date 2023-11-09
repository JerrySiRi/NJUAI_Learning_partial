#include "lib.h"
#include "types.h"
#define HUNGRY 0
#define EATING 1
#define THINKING 2
void test(int i,int *now_state,sem_t* forks);


int uEntry(void) {

	// For lab4.1
	// Test 'scanf' 
	int dec = 0;
	int hex = 0;
	char str[6];
	char cha = 0;
	int ret = 0;
	while(1){
		printf("Input:\" Test %%c Test %%6s %%d %%x\"\n");
		ret = scanf(" Test %c Test %6s %d %x", &cha, str, &dec, &hex);
		printf("Ret: %d; %c, %s, %d, %x.\n", ret, cha, str, dec, hex);
		if (ret == 4)
			break;
	}
	
	// For lab4.2
	// Test 'Semaphore'
	int i = 4;

	sem_t sem;
	printf("Father Process: Semaphore Initializing.\n");
	ret = sem_init(&sem, 2);
	if (ret == -1) {
		printf("Father Process: Semaphore Initializing Failed.\n");
		exit();
	}

	ret = fork();
	if (ret == 0) {
		while( i != 0) {
			i --;
			printf("Child Process: Semaphore Waiting.\n");
			sem_wait(&sem);
			printf("Child Process: In Critical Area.\n");
		}
		printf("Child Process: Semaphore Destroying.\n");
		sem_destroy(&sem);
		exit();
	}
	else if (ret != -1) {
		while( i != 0) {
			i --;
			printf("Father Process: Sleeping.\n");
			sleep(128);
			printf("Father Process: Semaphore Posting.\n");
			sem_post(&sem);
		}
		printf("Father Process: Semaphore Destroying.\n");
		sem_destroy(&sem);
		exit();
	}


	// For lab4.3
	// TODO: You need to design and test the philosopher problem.
	// Producer-Consumer problem and Reader& Writer Problem are optional.
	// Note that you can create your own functions.
	// Requirements are demonstrated in the guide.
	//XXX：五个哲学家进程fork
	//思考的时候:printf("Philosopher %d:think\n",id);
	//就餐的时候：printf("Philosopher %d:eat\n",id);
	//任意P、V及思考、就餐之间，添加sleep(128)

/*
	int now_state[5];
	sem_t forks[5];
	sem_t mutex;

	//【step1：信号量初始化+状态初始化,forks和mutex。在创建子进程之前完成，保证只初始化一次！】
	for(int i=0;i<5;i++){
		int result_1 = sem_init(&forks[i],0);
		if(result_1<0)
			{printf("something wrong with initializing semaphores forks\n");exit();}
	}

	int result_2 = sem_init(&mutex,1);
	if(result_2<0)
		{printf("something wrong with initializing semaphores(lock) mutex\n");exit();}

	for(int i=0;i<5;i++)
		now_state[i]=THINKING;

	//【step2：创建五个哲学家，确定当前哲学家的编号cur_ph】
	int cur_ph;//XXX：指示当前的进程是谁,不是pid！！！而是五个哲学家中的编号(0-4)！
	pid_t new_ph;//XXX：指示新的进程是谁，是pid！！！
	for(cur_ph=0;cur_ph<5;cur_ph++){
		new_ph = fork();//fork返回两次，父进程返回子的pid，子进程返回0！
		if(new_ph==0)//子进程返回，此时cur_ph就指示当前子进程中哲学家的编号是什么了！
			break;
		else if(cur_ph<0){
			printf("something wrong with creating new philosophers\n");
			exit();
		}	
	}

	//【step3：开始思考吃饭】
	for(int i=0;i<5;i++){

	printf("Philosopher %d:think\n",cur_ph);
	sleep(128);

	sem_wait(&mutex);
	now_state[cur_ph] = HUNGRY;
	test(cur_ph,now_state,forks);//此时已经同时拿上左右筷子开始吃啦！
	sem_post(&mutex);
	sem_wait(&forks[cur_ph]);
	printf("Philosopher %d:eat\n",cur_ph);
	sleep(128);
	
	sem_wait(&mutex);
	now_state[cur_ph] = THINKING;
	int left_c = (cur_ph-1>=0)?(cur_ph-1):(cur_ph+4);
	int right_c = (cur_ph+1>4)?(cur_ph-4):(cur_ph+1);
	test(left_c,now_state,forks);
	test(right_c,now_state,forks);//此时sem_post操作中会有时间中断来重新调度的呢！
	sem_post(&mutex);
	}
	printf("finishing think&eat,philosopher %d is released\n",cur_ph);
	sem_destroy(&forks[cur_ph]);
	exit();
*/
	return 0;
}


void test(int i,int *now_state,sem_t* forks){
	int left = (i-1>=0)?(i-1):(i+4);
	int right = (i+1>4)?(i-4):(i+1);
	if(now_state[i]==HUNGRY && now_state[left]!=EATING && now_state[right]!=EATING){
		now_state[i]=EATING;
		sem_post(&forks[i]);
	}
		
}

