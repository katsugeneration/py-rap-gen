# Download wiki data
wget "https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2" -O "jawiki-latest-pages-articles.xml.bz2"
bzip2 -d "jawiki-latest-pages-articles.xml.bz2"

# Parse Wiki data
git clone "https://github.com/attardi/wikiextractor.git"
python wikiextractor/WikiExtractor.py -o articles -b 10G --processes 10 jawiki-latest-pages-articles.xml
python - << EOS
import re
kakko = re.compile(r"[(（](.+?)[)）]")
space = re.compile(r"[\s「」]")

w = open('articles.txt', 'w', encoding='utf-8')
with open('articles/AA/wiki_00') as f:
    for line in f:
        if line.startswith('<doc'):
            continue
        elif line.startswith('</doc'):
            continue
        line = re.sub(kakko, "", line).strip()
        line = re.sub(space, "", line).strip()
        line = line.strip().split('。')
        if all(l == '' for l in line):
            continue
        for l in line:
            w.write(l + '\n')
w.close()
EOS
cat articles.txt | mecab -F"%m %f[8]\t" -U"%m <UNKNOWN>\t" -E"\n" -b 100000 > data