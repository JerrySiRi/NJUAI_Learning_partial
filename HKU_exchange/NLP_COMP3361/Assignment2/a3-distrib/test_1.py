
string="""\n question:There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\n # solution in Python:\n def solution():\n    \"\"\"There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?\"\"\"\n    trees_initial = 15\n    trees_after = 21\n    trees_added = trees_after - trees_initial\n    result = trees_added\n    return result\n\n question:If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\n # solution in Python:\n def solution():\n    \"\"\"If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?\"\"\"\n    cars_initial = 3\n    cars_arrived = 2\n    total_cars = cars_initial + cars_arrived\n    result = total_cars\n    return result\n\n question:Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\n # solution in Python:\n def solution():\n    \"\"\"Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?\"\"\"\n    leah_chocolates = 32\n    sister_chocolates = 42\n    total_chocolates = leah_chocolates + sister_chocolates\n    chocolates_eaten = 35\n    chocolates_left = total_chocolates - chocolates_eaten\n    result = chocolates_left\n    return result\n\n question:Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\n # solution in Python:\n def solution():\n    \"\"\"Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?\"\"\"\n    jason_lollipops_initial = 20\n    jason_lollipops_after = 12\n    denny_lollipops = jason_lollipops_initial - jason_lollipops_after\n    result = denny_lollipops\n    return result\n\n question:Janet\u2019s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?\n # solution in Python:\n \n def solution():\n    \"\"\"Janet\u2019s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg.\"\"\"\n    eggs_per_day = 16\n    eggs_eaten_per_day = 3\n    eggs_baked_per_day = 4\n    eggs_sold_per_day = 2\n    eggs_left_per_day = eggs_per"""



slots = 4
end_index = -1
start_index = 0
for i in range(slots+2):
    temp_answer =string[start_index:]
    index = temp_answer.find("question")# 就算没找到end-index和start_index也不会变！
    if index == -1:#找不到下一个
        end_index = len(string)
    else:
        end_index += index+1
        start_index += (index+1)


print(string[:end_index])




