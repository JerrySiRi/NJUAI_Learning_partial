def postprocess_output(output: str) -> str:
        stop_sequences =[ "\nclass", "\ndef", "\n#", "\nif", "\nprint"]
        start_index = output.find("\ndef")
        answer = output[start_index+1:] # 从第一个def开始之后才能算答案的开始
        stop_index = len(answer)
        for item in stop_sequences:
          temp_index = answer.find(item)
          if temp_index != -1: # find the stop_token
            stop_index = min(stop_index, temp_index)
        real_output = output[ :stop_index+start_index+1]
        print("------------",output)
        print("IIIIIIIIIIII",real_output)
        return real_output


string = """from typing import List\n\n\ndef has_close_elements(numbers: List[float], threshold: float) 
-> bool:\n\"\"\" Check if in given list of numbers, are any two numbers closer to each other than\n
    given threshold.\n    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)\n    False\n    
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\n    True\n    \"\"\"\n", 
    for i in range(11111)\n \n \n.1\ndef asdfffgfgfgfgf
    
"""
postprocess_output(output=string)




