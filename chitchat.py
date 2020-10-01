import json
import random

from nltk_utils import tokenize,stem

def network(leng , sentence , bot_name):

    #   varibles
    tags = []
    xy = []
    ab = []
    chat_history = []
    given_ans = []

    #Json FIle
    with open('intents.json', 'r') as f:
        intents = json.load(f)

    #   store Intents data
    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        # store Pattern Questions
        for pattern in intent['patterns']:
            w = tokenize(pattern.lower())
            xy.append((w, tag))
         # store Responses
        for response in intent['responses']:
            w = tokenize(response.lower())
            ab.append((w, tag))

    # Find length og tags for new variable
    tags_len = len(tags)
    tags_prob = [0] * tags_len

# ready for chat very low level------------------------------------------------

    # for intent in intents['intents']:
    #         for pattern in intent['patterns']:
    #             if(sentence in pattern):
    #
    #                 prob = len(sentence)/len(pattern)
    #
    #                 print("probability" , prob)
    #                 print("tag: " , intent['tag'])
    #
    #                 # current = intent['tag']
    #                 # tags_len = len(tags)
    #
    #                 print(f"{bot_name}: {random.choice(intent['responses'])}")
    #
    #                 # for j in range(tags_len):
    #                 #     if(current==tags[j]):
    #                 #         print("tags value: ", tags_value)
    #                 #         tags_value[j] +=1
    #                 #         print("now tags are; ", tags_value)
#----------------------------------------------------------------------------------

#......Chat Optimization 1.0
    # for pattern_sentence,tag in xy:
    #     matching_point = 0
    #     for i in range(leng):
    #         if (sentence[i] in pattern_sentence):
    #             matching_point+=1
    #             prob = float(len(sentence) / len(pattern_sentence) * matching_point)
    #             # print("Sentence: ", sentence[i] , " Match..." , " Matching point: ", matching_point , " ...Tag: " ,tag)
    #             tags_len = len(tags)
    #             for j in range(tags_len):
    #                 if (tag == tags[j]):
    #                     if(tags_prob[j] <= prob):
    #                         tags_prob[j] = prob
    #                         print("prob: ", tags_prob, " ... tags: ", tag)
    #
    # k=0
    # for j in range(len(tags_prob)-1):
    #     if tags_prob[k] > tags_prob[j+1] :
    #         output=tags[k]
    #     else:
    #         k=j+1
    # for intent in intents['intents']:
    #     if (tags[k] == intent['tag']):
    #         print("value of K: ", k)
    #         print(f"{bot_name}: {random.choice(intent['responses'])}")
#-------------------------------------------------------------------------------------

# Make probablity for tag
    for pattern_sentence,tag in xy:
        matching_point = 0
        for i in range(leng):
            if (sentence[i] in pattern_sentence):
                matching_point+=1
                prob = float(len(sentence) / len(pattern_sentence) * matching_point)
                # print("Sentence: ", sentence[i] , " Match..." , " Matching point: ", matching_point , " ...Tag: " ,tag)
                tags_len = len(tags)
                for j in range(tags_len):
                    if (tag == tags[j]):
                        if(tags_prob[j] <= prob):
                            tags_prob[j] = prob
                            # print("prob: ", tags_prob, " ... tags: ", tag)
    # find high probability tag
    k=0
    for j in range(len(tags_prob)-1):
        if tags_prob[k] > tags_prob[j+1] :
            output=tags[k] # k = k
        else:
            k=j+1

    # store related messages in arry

    # for intent in intents['intents']:
    #     if (tags[k] == intent['tag']):
    for i in range(leng):
        for pattern_response, tag in ab:
            if (sentence[i] in pattern_response and tag==tags[k]):
                if(pattern_response not in given_ans ):
                    given_ans.append(pattern_response)
    # print("Given ans: " , given_ans)

    # variables
    given_ans_len = len(given_ans)
    ans_prob = [0] * given_ans_len

    # make probability for ans
    if(given_ans_len>0):
        for i in range(given_ans_len):
            matching_point = 0
            for j in range(leng):
                if (sentence[j] in given_ans[i]):
                    matching_point += 1
                    # print("Sentence: ", sentence[j] , " Match..." , " Matching point: ", matching_point , " ...given ans: " ,given_ans[i])
                    prob = float(len(sentence) / len(given_ans[i]) * matching_point)
                    for k in range(given_ans_len):
                        if (ans_prob[k] <= prob):
                            ans_prob[i] = prob
    # print("ans Probability: " , ans_prob)

    # find high probability for ans

    l = 0
    for m in range(len(ans_prob)-1):
        if ans_prob[l] > ans_prob[m+1] :
            l = l
        else:
            l=m+1

    if(given_ans_len>0):
        print(f"{bot_name}:{given_ans[l]}")
    else:
        print(f"{bot_name}: {random.choice(intent['responses'])}")





bot_name = "robo"
print("Let's chat! (type 'quit' to exit)")
while True:
    sentence = input("You: ")
    if sentence == "quit":
        break
    sentence = tokenize(sentence)
    leng = len(sentence)

    network(leng , sentence , bot_name)