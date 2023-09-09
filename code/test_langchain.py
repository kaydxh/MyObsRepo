
from transformers import AutoTokenizer, AutoModel
import numpy as np
import generate_vector
import pickle
import json
def get_prompt(sentences,query):
    return "请根据以下事实回答问题{}。问题是：{}".format("。".join(sentences),query)
#分词器 仍然用原生的
# tokenizer = AutoTokenizer.from_pretrained("E:\code\chatglm\chatglm2", trust_remote_code=True)
# #加载训练好的模型模型
# model = AutoModel.from_pretrained("E:\code\chatglm\chatglm2", trust_remote_code=True).cuda()
with open("id_vector","rb") as f:
    index=pickle.load(f)
with open("id_know") as f:
    id_know=json.load(f)
input="江西旅游怎么玩"
#把问题变成向量
vector=generate_vector.get_vector(input)
vector=np.array([vector])
#从faiss库里面找到最近的3个id  D距离，I id
D, I = index.search(vector, 3)
D=D[0]
I=I[0]
sentences=[]
for d,i in zip(D,I):
    #距离过滤
    if d>0.02:
        continue
    #print (id_know[str(i)]['query'])
    sentences.append(id_know[str(i)]['target'])
#print (sentences)
prompt=get_prompt(sentences,input)
print (prompt)
# response, history = model.chat(tokenizer, prompt, history=[])
# print(response)

