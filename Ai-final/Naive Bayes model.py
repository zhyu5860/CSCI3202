import math
import string

def tokenize(sentence):
    return sentence.lower().translate(str.maketrans('','',string.punctuation)).split()[1:]

dictforword = {}

posr = open("PosMoviereview-training.txt", encoding="utf8")
count_pos = 0
for line in posr:
    count_pos += 1
posr.close()

posr = open("PosMoviereview-training.txt", encoding="utf8")
tokens = tokenize(posr.read())

dict_pos = {}
for token in tokens:
    token = token.strip()
    if token not in dict_pos.keys():
        dict_pos[token] = 0
        if token not in dictforword.keys():
            dictforword[token] = 1
    dict_pos[token] += 1
posr.close()


negr = open("NegMoviereview-training.txt", encoding="utf8")
count_neg = 0
for line in negr:
    count_neg += 1
negr.close()

negr = open("NegMoviereview-training.txt", encoding="utf8")
tokens = tokenize(negr.read())

dict_neg = {}
for token in tokens:
    token = token.strip()
    if token not in dict_neg.keys():
        dict_neg[token] = 0
        if token not in dictforword.keys():
            dictforword[token] = 1
    dict_neg[token] += 1
negr.close()
#print(dict_neg)
countp = 0
countn = 0
output = open("zhengwuyuan-out.txt", "w",encoding="utf8")

for line in open("test-set.txt", encoding="utf8"):
    ids = line.split()[0]

    ProbPos = (math.log(float(count_pos)/float(count_pos + count_neg)))
    ProbNeg = (math.log(float(count_neg)/float(count_pos + count_neg)))

    tokens = tokenize(line)

    for token in tokens:
        
        possum = sum(dict_pos.values())
        negsum = sum(dict_neg.values())
        
        pos_bottom = math.log(float(possum + len(dictforword)))
        neg_bottom = math.log(float(negsum + len(dictforword)))
        
        if token in dict_pos.keys():
            ProbPos += (math.log(float(dict_pos[token] + 1))/pos_bottom)
        else:
            ProbPos += (math.log(float(1))/pos_bottom)
        if token in dict_neg.keys():
            ProbNeg += (math.log(float(dict_neg[token] + 1))/neg_bottom)
        else:
            ProbNeg += (math.log(float(1))/neg_bottom)
            
    if ProbPos > ProbNeg:
        output.write(ids + " Positive\n")
        countp= 1+countp
    else:
        output.write(ids + " Negative\n")
        countn= 1+countn
        
probability = countp/(countp+countn)
print("positive rate: "+str(probability*100)+"%")

output.close()

solution = open("answer.txt","r")
list1 =[]
for line in solution:
    
    list1.append(line.strip())
solution.close

predicted = open("zhengwuyuan-out.txt","r")
list2 =[]
for line in predicted:
    list2.append(line.strip())
predicted.close

from sklearn.metrics import accuracy_score

accurate = accuracy_score(list1, list2)
accuracy = accurate *100

print("accurate of our predicted data: "+str(accuracy)+"%" )
