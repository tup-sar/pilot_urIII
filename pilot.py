# imports:
# datetime to timestamp the output file
# csv to read CDLI cvs files

from datetime import datetime
import csv, io

now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

# objects of this class holds goods and their names in English, Sumerian, and Akkadian
# the class also define methods to add new terms in each of the languagues
# the occurrence list holds  CDLI id's of the objects where the term occurs


class Good():
    def __init__(self):
        self.english = set()
        self.sumerian = set()
        self.akkadian = set()
        self.occurrences = []
    def add_english(self, term):
        self.english.add(term)
    def add_sumerian(self, term):
        self.sumerian.add(term)
    def add_akkadian(self, term):
        self.akkadian.add(term)
    def append_occurrence(self, term):
        self.occurrences.append(term)

property = Good()
property.add_english("property")
property.add_sumerian("nig2-szu")

beer = Good()
beer.add_sumerian("kasz")
beer.add_english("beer")

oil = Good()
oil.add_sumerian('i3')
oil.add_english('oil')

grain = Good()
grain.add_sumerian('sze')
grain.add_english('grain')

bread = Good()
bread.add_sumerian('ninda')
bread.add_english('bread')

sheep = Good()
sheep.add_sumerian('udu')
sheep.add_sumerian('udu-hi-a')
sheep.add_english('sheep')

ox = Good()
ox.add_sumerian('gu4')
ox.add_sumerian('hu4-hi-a')
ox.add_english('ox')

onion = Good()
onion.add_sumerian('szum2')
onion.add_english('onion')

silver = Good()
silver.add_sumerian('ku3-babbar')
silver.add_sumerian('kug-babbar')
silver.add_english('silver')

leek = Good()
leek.add_english('leek')
for word in ['ga-rasz{sar}', 'ga-rasz', 'gar3-szum', 'garasz4{sar}','{u2}gar3-szum']:
    leek.add_sumerian(word)

duck = Good()
duck.add_english('duck')
duck.add_sumerian('bibad')
duck.add_sumerian('bibad{muszen}')

duck.add_sumerian('uz')

horse = Good()
horse.add_english('horse')
horse.add_sumerian('si2-si2')
horse.add_sumerian('{ansze}si2-si2')

shoe = Good()
shoe.add_english('shoe')
for word in ['a2-bu-ru-um-ma', 'a2-bu-ru-ma', 'a2-bu-ru-ru-ma', 'a2-bu-ru-um'
             '{kusz}e-sir2', 'e-sir2', '{kusz}esir4', '{kusz}esir5', '{kusz}e-sir', 
             '{kusz}esirₓ(LAK173)', 'esir5', 'esir3', 'esir4', 'esir2', 'esirx(LAK173)', 
             '{kusz}e-sir2-e-sir2', '{kusz}esir2', '{kusz}esir3', 
             '{urud}e-sir2']:
    shoe.add_sumerian(word)
              

# define a list of goods you want to track

to_track = [beer, oil, bread, grain, sheep, ox, onion]

# define the locations you want to track

locations = {'Puzriš-Dagan (mod. Drehem)': 'pd', 'Girsu (mod. Tello)': 'girsu', 'Umma (mod. Tell Jokha)': 'umma'}

# define the kings whose reigns you want to track

kings = {'Amar-Suen': 'as', 'Šū-Suen': 'ss'}
reign_lengths = { 'as': 9, 'ss': 9}

# prepare variables to hold the names of the files that will be read
list_of_csv_files = []
list_of_atf_files = []
for location in locations:
    for king in kings:
        file_name = 'data/urIII_'+locations[location]+'_'+kings[king]
        list_of_atf_files.append(file_name+'_texts.atf')
        list_of_csv_files.append(file_name+'_meta_data.csv')

# loop over the atf files that need to be read, in order to annotated the occurrences
# Observation: this is not at all time efficient! Remember this is a pilot, please
for file in list_of_atf_files:
    f = io.open(file,'r', encoding='utf-8')
    for line in f:
        if "&P" in line[:2]:
            present_text = line[2:8]
        line = line.replace("_","")
        line = line.replace("#", "")
        split_line = line.split(" ")
        for piece in split_line:
            for good in to_track:
                if piece in good.sumerian:
                    good.append_occurrence(present_text)
    f.close()

# open the file to write the report
h = io.open('reports/report_'+now+'.csv','w', encoding='utf-8')

# now loop through the csv metadata files to get the year of the document and
# to count how many documents per year (for each good)
# the counting is stored in the counts dictionary: 
# - each key has the form of a tuple 
#              tup = (provenience,item_king,item_year,next(iter(good.english)))
#              Obs: next(iter(good.english)) simply gets the first English term of the good
# - the value associated to each key is the number of occurrences of the term under
#   that king's year-th year of reign in a document from that provenience
counts = {}
for file in list_of_csv_files:
    with open(file,'r', newline = '') as g:
        reader = csv.DictReader(g)
        count = 0
        for line in reader:
            cdli_n = line["artifact_id"]
            date = line["dates"]
            provenience = line["provenience"]
            if "," in date:
                date = date.split(",")
            else:
                date = [date]
                    
            for good in to_track:
                if cdli_n in good.occurrences:
                    for item in date:
                        item = str(item)
                        item = item.replace(" ","")
                        position = item.find(".")
                        item_king = item[:position]
                        item_year = item[position+1:position+3]
                        string_to_print = provenience+","+item_king+","+item_year+","+next(iter(good.english))+","+cdli_n+"\n"
                        tup = (provenience,item_king,item_year,next(iter(good.english)))
                        if tup in counts.keys():
                            counts[tup] = counts[tup] + 1
                        else:
                            counts[tup] = 1

# print the results in a user-friendly way and in a csv file to be 
# that can be imported in excel                        
for location in locations:
    print(location)
    h.write(location+"\n")
    good_names = ""
    for good in to_track:
        if good_names == "":
            good_names = next(iter(good.english))
        else:
            good_names = good_names+","+next(iter(good.english))
    print(",,"+good_names)
    h.write(",,"+good_names+"\n")
    for king in kings:
        for year in range(1,reign_lengths[kings[king]]+1):
            year = f"{year:02d}"
            all_occurrences = ""
            for good in to_track:
                good_name = next(iter(good.english))
                tup = (location, king, year, good_name)
                if tup in counts.keys():
                    occurrences  = str(counts[tup])
                else:
                    occurrences = "0"
                if all_occurrences == "":
                    all_occurrences = occurrences
                else:
                    all_occurrences = all_occurrences+","+occurrences
            string_to_print = king+','+year+','+all_occurrences+'\n'
            print(string_to_print,end='')
            h.write(string_to_print)
        
h.close()
