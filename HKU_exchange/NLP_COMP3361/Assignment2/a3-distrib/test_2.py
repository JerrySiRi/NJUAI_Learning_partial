# 8-shot in-context examples
GSM_EXAMPLARS = [
    {
        "question": "There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?",
        "cot_answer": "There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. So the answer is 6.",
        "pot_answer": "def solution():\n    \"\"\"There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\"\"\"\n    trees_initial = 15\n    trees_after = 21\n    trees_added = trees_after - trees_initial\n    result = trees_added\n    return result",
        "short_answer": "6"
    },
    {
        "question": "If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?",
        "cot_answer": "There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. So the answer is 5.",
        "pot_answer": "def solution():\n    \"\"\"If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\"\"\"\n    cars_initial = 3\n    cars_arrived = 2\n    total_cars = cars_initial + cars_arrived\n    result = total_cars\n    return result",
        "short_answer": "5"
    },
    {
        "question": "Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?",
        "cot_answer": "Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. So the answer is 39.",
        "pot_answer": "def solution():\n    \"\"\"Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\"\"\"\n    leah_chocolates = 32\n    sister_chocolates = 42\n    total_chocolates = leah_chocolates + sister_chocolates\n    chocolates_eaten = 35\n    chocolates_left = total_chocolates - chocolates_eaten\n    result = chocolates_left\n    return result",
        "short_answer": "39"
    },
    {
        "question": "Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?",
        "cot_answer": "Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. So the answer is 8.",
        "pot_answer": "def solution():\n    \"\"\"Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\"\"\"\n    jason_lollipops_initial = 20\n    jason_lollipops_after = 12\n    denny_lollipops = jason_lollipops_initial - jason_lollipops_after\n    result = denny_lollipops\n    return result",
        "short_answer": "8"
    },
    {
        "question": "Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?",
        "cot_answer": "Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. So the answer is 9.",
        "pot_answer": "def solution():\n    \"\"\"Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?\"\"\"\n    toys_initial = 5\n    mom_toys = 2\n    dad_toys = 2\n    total_received = mom_toys + dad_toys\n    total_toys = toys_initial + total_received\n    result = total_toys\n    return result",
        "short_answer": "9"
    },
    {
        "question": "There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?",
        "cot_answer": "There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. So the answer is 29.",
        "pot_answer": "def solution():\n    \"\"\"Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?\"\"\"\n    toys_initial = 5\n    mom_toys = 2\n    dad_toys = 2\n    total_received = mom_toys + dad_toys\n    total_toys = toys_initial + total_received\n    result = total_toys\n    return result",
        "short_answer": "29"
    },
    {
        "question": "Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?",
        "cot_answer": "Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. So the answer is 33.",
        "pot_answer": "def solution():\n    \"\"\"Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?\"\"\"\n    golf_balls_initial = 58\n    golf_balls_lost_tuesday = 23\n    golf_balls_lost_wednesday = 2\n    golf_balls_left = golf_balls_initial - golf_balls_lost_tuesday - golf_balls_lost_wednesday\n    result = golf_balls_left\n    return result",
        "short_answer": "33"
    },
    {
        "question": "Olivia has $23. She bought five bagels for $3 each. How much money does she have left?",
        "cot_answer": "Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. So the answer is 8.",
        "pot_answer": "def solution():\n    \"\"\"Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\"\"\"\n    money_initial = 23\n    bagels = 5\n    bagel_cost = 3\n    money_spent = bagels * bagel_cost\n    money_left = money_initial - money_spent\n    result = money_left\n    return result",
        "short_answer": "8"
    }
]

data=[{
        "question": "11110000",
        "cot_answer": "Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. So the answer is 8.",
        "pot_answer": "def solution():\n    \"\"\"Olivia has $23. She bought five bagels for $3 each. How much money does she have left?\"\"\"\n    money_initial = 23\n    bagels = 5\n    bagel_cost = 3\n    money_spent = bagels * bagel_cost\n    money_left = money_initial - money_spent\n    result = money_left\n    return result",
        "short_answer": "8"
    }]

def build_prompts(dataset, n_shot=8, demos=GSM_EXAMPLARS):
        """
        Build few-shot prompts from the GSM8K dataset. Use
        :param dataset: list of examples
        :param n_shot: number of examples to use for few-shot learning
        :param demos: list of demonstrator examples
        :return: list of prompts
        """

        shared_prompts = []
        for index in range(n_shot):
          prompt = {
            'question': demos[index]["question"],
            'answer': demos[index]["short_answer"]
          }
          shared_prompts.append(prompt)
        # 应该还需要每个prompts加一下dataset的提问，需要先看dataset的格式，再把question加上
        data_prompt = []
        for index in range(len(dataset)):
          current_prompt=shared_prompts
          prompt={
            "question":dataset[index]["question"],
            "answer": ""
          }
          current_prompt.append(prompt)
          data_prompt.append(current_prompt)
        return data_prompt


print(build_prompts(data,n_shot=8,demos=GSM_EXAMPLARS))