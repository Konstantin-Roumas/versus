import argparse
from operator import itemgetter
import glob
def get_mc_name(battle):
    mc = ""
    t = []
    if battle.find("против") != -1:
        t = battle.split("против")
    elif battle.find("&") != -1:
        t = battle.split("&")
    elif battle.find("VS") != -1:
        t = battle.split("VS")
    elif battle.find("vs") != -1:
        t = battle.split("vs")
    if t != []:
        mc = (t[0].strip())
    return mc


battle_list = glob.glob("*")
mc_info = dict()
best_word = dict()
for battle in battle_list:
    mc = get_mc_name(battle)
    mc = mc.replace(" ", "_")
    if mc == "":
        continue
    with open(battle) as f:
        file = f.read()
    l = mc_info.get(mc,[0,0])
    #l[0] - amount of words
    #l[1] - amount of battles
    with open("words.yml") as bd:
       words = bd.read()
    for cur_word in words.lower().split():
        l[0] += file.lower().count(cur_word)
    l[1] += 1
    mc_info[mc] = l

    if mc not in best_word:
        best_word[mc] = dict()
        our_text = file.lower()
    for word in our_text.split():
        if len(word) < 3:
            continue
        for tr in [",",".","!","?",":","-",";","»","«", "...", "(", ")", "&quot", "…"]:
            word = word.strip(tr)
        word = word.strip()
        if word not in best_word[mc]:
            best_word[mc][word] = 1
        else:
            best_word[mc][word] += 1

result = list(mc_info.items())
result = sorted(result,key=itemgetter(1), reverse=True)
first = argparse.ArgumentParser()
first.add_argument("--top-bad-words", type=int)
first.add_argument("--name",type=str)
first.add_argument("--top-words",type=int)
args_dict = vars(first.parse_args())
ans = result[0:args_dict["top_bad_words"]]

for mc, cnt in ans:
    word_bat = cnt[0] / cnt[1]
    print("{} | батлов {} | {} нецензурных слов | {} слова на батл".format(mc, cnt[1], cnt[0], word_bat))

if args_dict["name"]  not in best_word:
    print("Мы не знаем этого МС")
else:
    res = best_word[args_dict["name"]].items()
    res = sorted(res,key=itemgetter(1), reverse=True)
    for i in res[0:args_dict["top_words"]]:
        print("Слово {} - {} раз".format(i[0], i[1]))
