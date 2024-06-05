import os
with open(os.path.join('words',"russian_nouns.txt"),'r',encoding='utf-8') as file:
    lines = file.readlines()
    files = [[] for i in range(26)]
    for i in lines:
        if '-' not in i:
            files[len(i)].append(i)
        
    for index,j in enumerate(files):
        with open(os.path.join('words',f'len_{index-1}.txt'),'w',encoding='utf-8') as file2:
            file2.writelines(j)
    