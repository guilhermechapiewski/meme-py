from re import compile

from meme import Meme, PostRepository

class MemeCloud(object):
    
    def __init__(self):
        self.wordCount = {}
        self.user = None
        self.limit = None
        self.content = ''
        self.blacklist = [
#    'about','all','am','an','and','another','any','anybody','anyone','anything','are','because','best','both','by','each','each','et','other',
#                'either','everybody','everyone','everything','few','from','get','going','good','have','he','her','hers','herself','him','himself','his','i','is',
#		'it','its','itself','like','little','many','me','mine','more','most','much','myself','neither','no','on','one','nobody',
#		'none','nothing','one','another','other','others','our','ours','ourselves','several','she','so','some','somebody',
#		'someone','something','that','their','theirs','them','themselves','there','these','they','this','those','to','us','was','we','were','will','with','what',
#		'whatever','which','whichever','who','whoever','whom','whomever','whose','you','your','yours','yourself',
]

    def load_memes(self, user='bigodines', limit=10):
        self.user = user
        self.limit = limit
        postRepo = PostRepository()
        posts = postRepo.searchByUser(user=self.user,limit=self.limit)
        p = compile(r'<.*?>')
        self.content =  p.sub(''," ".join([x.content for x in posts ]))

    def count(self):
        words = self.content.split()
        for word in words:
            if len(word) <= 3: continue
            # TODO: check against blacklist
            if self.wordCount.get(word):
                self.wordCount[word] += 1
            else:
                self.wordCount[word] = 1

    def sort(self):
        if len(self.content) < 1: return []
        if len(self.wordCount) < 1: 
            self.count()

        items=self.wordCount.items()
        backitems=[ [v[1],v[0]] for v in items]
        backitems.sort(reverse=True)
        sortedlist=[ (backitems[i][1],backitems[i][0]) for i in range(0,len(backitems))]
        return sortedlist

    def show(self, sortedCloud=None):
        html = {}
        if sortedCloud:
            higherCount = int(sortedCloud[0][1])
            incVal = int(higherCount/5) 
            if incVal == 0: incVal = 1
            for item in sortedCloud:
                font_size = int(item[1]/incVal)
                html[item[0]] = "<span class='size%d'>%s</span>\n" % (font_size, item[0])

            #shuffle(html)
            return " ".join([x[1] for x in html.items()]).encode('UTF-8')
             

if __name__ == "__main__":
    cloud = MemeCloud()
    cloud.load_memes(user='bigodines')
    cloud.count()
    print cloud.show(cloud.sort())
