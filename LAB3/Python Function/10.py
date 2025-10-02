def unique_list(list):
    unique=[]
    for i in list:
        if i not in unique:
            unique.append(i) 
    return unique

words=["qwe","qwe","asd","dfg"]
print(unique_list(words))