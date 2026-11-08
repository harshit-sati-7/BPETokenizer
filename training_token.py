from main_tokenizer import BPETokinizer
import time

start=time.perf_counter()

tok=BPETokinizer()


with open("training.txt","r",encoding="utf-8") as f:
    data=f.read()


print("Reading...",flush=True)

tok.train(data,500)



tok.save()

print("Training completed...")

print("Time taken: ",time.perf_counter()-start)

