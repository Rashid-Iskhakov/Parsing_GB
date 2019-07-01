from requests import get
import re
def get_link(topic):
    link = "https://ru.wikipedia.org/wiki/" + topic.capitalize()
    return link

def get_topic_page(topic):
    link = get_link(topic)
    html = get(link).text
    return html

def get_topic_text(topic):
    html_content = get_topic_page(topic)
    words = re.findall("[а-яА-Я]{3,}",html_content)
    return words

def get_topic_links(topic):
    html_content = get_topic_page(topic)
    links = re.findall(r'<a rel="nofollow" class="external text" href="([^"]+)"', html_content)
    return links

def get_link_text(link):
    html_content = get(link).text
    words = re.findall("[а-яА-Я]{3,}", html_content)
    return words



def get_common_words(topic, x):
    if x == 0:
        words_list = get_topic_text(topic)
    elif x == 1:
        links = get_topic_links(topic)

        state = True
        i = 0
        while state:
            try:
                words_list = get_link_text(links[int(i)])
                state = False
            except:
                state = True
            i +=1


    rate={}
    for word in words_list:
        if word in rate:
            rate[word]+=1
        else:
            rate[word]=1
    rate_list = list(rate.items())
    rate_list.sort(key = lambda x :-x[1])

    return rate_list


def visualize_common_words(topic, x=0):
    words = get_common_words(topic, x)
    list1 = []
    for w in words[0:10]:
        list1.append(str(f'{w[0]} встречается {w[1]} раз'))
    return list1


topic='Компьютер'
#print(visualize_common_words(topic, 1), sep='\n'')
#print(len(list1))

list2 = visualize_common_words(topic, 1)
#print(list2)

file_wiki = open('test_wiki.txt', 'w')
for l in list2:
    file_wiki.write(l + '\n')
file_wiki.close()
