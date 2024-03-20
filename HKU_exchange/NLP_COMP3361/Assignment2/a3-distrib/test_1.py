string="""Janet's ducks lay 16 eggs per day. She eats 3 for breakfast every morning. 
Bakes 4 muffins for her friends every day. 
Sells the remainder at the farmers' market daily for $2 per fresh duck egg. 
So 16 * 3 = 48 eggs. 48 * 2 = 96 dollars. So the answer is 96."""

index = string.find("So the answer is ")
print(string[index+17:-1])




