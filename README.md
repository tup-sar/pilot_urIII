# pilot_urIII
Pilot for project funding request

## Function

So far (Oct 17, 2025), the script reads csv and atf files downloaded from CDLI and produces a report of the number of occurrences by year of a list of goods.

The data currently covers the 
- locations: Puzriš-Dagān, Ĝirsu, and Umma
- reigns: Amar-Suen and Šū-Suen

### Customizing the goods you want to track

Instantiate the good as an object of the class Good(). For instance, to create the object wool, include the following lines of code in pilot.py:

```
wool = Good()
wool.add_english('wool')
wool.add_sumerian('si-ki')
````

Should you want to include other Sumerian writing, just to like this:

```
wool.add_sumerian('{tuk2}siki')
````

You can also iterate over a list of writings:

```
for word in ['siki', 'si-ki', '{tug}siki', 'UMBIN', 'siki{si-ki}', 'sig', 'kig2', 'si-ik', 'szi-gi', 'szi-ik']:
    wool.add_sumerian(word)
```

After creating the object to represent the good you want to track, include it in the list of objects to be tracked. For instance, to track sheep and wool, write:

````
to_track = [sheep, wool]
````


## Directory structure

```
.
├── pilot.py                # Generate a csv report
├── data/
│   └── urIII_....csv      # metadata csv files downloaded from CDLI
│   └── urIII_....atf      # atf transliteration files downloaded from CDLI
 
```

