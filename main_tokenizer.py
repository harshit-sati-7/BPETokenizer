import json 
import re

class BPETokinizer:
    def __init__(self):
        self.merges={}
        self.vocab={
            i:bytes([i]) for i in range(256)
        }
        self.pattern=r"\w+|\s+|[^\w\s]"




    def get_stats(self,ids):
        stats={}
        for i in range(len(ids)-1):
            pair=(ids[i],ids[i+1])
            stats[pair]=stats.get(pair,0)+1
        return stats
    def fre(self,stats):
        temp=[]
        for pair,val in stats.items():
            temp.append(val)
        maxvalue=max(temp)
        for pair,val in stats.items():
            if val==maxvalue:
                pairs=pair
        return pairs

    def merge(self,ids,pair,new_id):
        res=[]
        i=0
        while(i<len(ids)):
            if(i<len(ids)-1 and (ids[i],ids[i+1])==pair):
                res.append(new_id)
                i+=2
            else:
                res.append(ids[i])
                i+=1
        return res

    def get_stats_chunks(self,chunks):
        res={}
        for chunk in chunks:
            nres=self.get_stats(chunk)
            
            for key,valu in nres.items():
                res[key]=res.get(key,0) + valu

        return res

    def get_merge_chunk(self,ids,pair,new_id):
        chunks=[]
        for i in ids:
            ids=self.merge(i,pair,new_id)
            chunks.append(ids)
        return chunks

    def train(self,text,vocab_size):
        res=[]
        chunks=[]
        self.merges={}
        if vocab_size<256:
            raise ValueError("Enter vocab_size more thab 256")
        if not text.strip():
            raise ValueError("Enter atleast one character to train tokenizer")
        parts=re.findall(self.pattern,text)
        for part in parts:
            res.append(part.encode("utf-8"))
        for chunk in res:
            chunks.append(chunk)    

        for new_id in range(256,vocab_size):
            stats=self.get_stats_chunks(chunks)
            if not stats:
                break

            pair=self.fre(stats)
            chunks=self.get_merge_chunk(chunks,pair,new_id)

            self.merges[pair]=new_id

        for pair,new_id in self.merges.items():
            self.vocab[new_id]=self.vocab[pair[0]]+self.vocab[pair[1]]   

    def save(self):
        data={
            "pattern": self.pattern,
            "merges": []
        }
       
        for key,value in self.merges.items():
            data["merges"].append([key[0],key[1],value])
 
        with open("token.json","w") as f:
                json.dump(data,f)

        print("Data saved succesfully")        



    def load(self):
        self.merges={}
        self.vocab={
            i:bytes([i]) for i in range(256)

        }   

        try:
            with open("token.json","r") as f:
                data=json.load(f)

            for val in data['merges']:
                pair=(val[0],val[1])
                self.merges[pair]=val[2]

            for pair,value in self.merges.items():
                self.vocab[value]=self.vocab[pair[0]] + self.vocab[pair[1]]    


        except Exception as e:
            raise e

        return self.merges     

    def encode(self,text):
        res=[]
        chunks=[]
        parts=re.findall(self.pattern,text)
        for part in parts:
            ids=list(part.encode("utf-8"))
            res.append(ids)

        for pair,value in self.merges.items():
            res=self.get_merge_chunk(res,pair,value)

        for chunk in res:
            chunks.extend(chunk)

        return chunks

    def decode(self,ids):
        try:
            res=b''
            for i in ids:
                res+=self.vocab[i]  
            return res.decode("utf-8")
        except Exception as e:
            raise e

        

        
tok=BPETokinizer()

