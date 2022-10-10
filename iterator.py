import os
import io
from bs4 import BeautifulSoup
import re
import shutil
import datetime



adresa="/".join(os.getcwd().split(os.sep)[:-1])

stranci = io.open("stranci.txt", mode='r',  encoding="utf-8")
lista_s=[]
for line in stranci:
  stripped_line = line.strip()
  lista_s.append(stripped_line)
stranci.close()

deca = io.open("deca.txt", mode='r',  encoding="utf-8")
lista_d=[]
for line in deca:
  stripped_line = line.strip()
  lista_d.append(stripped_line)
deca.close()

abecedarij=""
broj=1
for file in sorted(os.listdir(adresa)):
    broj+=1
    if file.endswith(".html"):
        if  "%i" in str(file):
          os.rename(adresa+"/"+file,adresa+"/"+file.replace("%i",""))
          file=file.replace("%i","")
        f = io.open(adresa+"/"+file,'r+',encoding="utf-8")
        lines1 = f.readlines() # read old content
        if(len(lines1)<=2):
          f.close()
          os.remove(adresa+"/"+file) 
          continue
        
        soup = BeautifulSoup("\n".join(lines1).replace('href="tlex://','class="audio_izgovor" href="https://rjecnik.hr/mreznik/wp-content/uploads/2021/mreznik_mediji/').replace(".mp3/",".mp3").replace("C:/Program%20Files%20(x86)/TLexSuite/Data/Speaker.gif","https://rjecnik.hr/mreznik/wp-content/uploads/2021/05/Speaker-4.gif").replace('class="Lemma__slika"><img','class="Lemma__slika"><img class="galerija"')+'<script>$(".audio_izgovor").click(function(i){i.preventDefault(),zvuk=$(this).attr("href"),new Audio(zvuk).play()});</script>', 'html.parser')
       
        tag = soup.find_all('span', {"class" : "vanjska_poveznica__poveznica"})
        for x in tag:
          try:
            x.name="a"
            x.attrs['href'] = x.string
            x.attrs['target'] = "_blank"
          except AttributeError:
            print(file)
        tvorbena=soup.find_all('span', {"class" : "Tvorbena_raz"})
        for x in tvorbena:
          try:
            reference=x.find_all('span')
            ref_broj="0"
            for y in reference:
              try:
                if y.attrs['class'][0]  == "Lemma__HomonymNumber":
                  ref_broj=y.string
                elif y.attrs['class'][0]  == "References":
                  y.name="a"
                  if ref_broj in ["1","2","3","4","5","6","7","8","9","10"]:
                    y.attrs['href'] = "../"+str(y.string.replace("ć","c").replace("č","c").replace("ž","z").replace("š","s").replace("đ","d").replace(" ","-"))+"_"+ref_broj+"-neizvorni"
                  else:
                    y.attrs['href'] = "../"+str(y.string.replace("ć","c").replace("č","c").replace("ž","z").replace("š","s").replace("đ","d").replace(" ","-"))+"-neizvorni"
              except AttributeError:
                print(file)
          except AttributeError:
            print(file)
        poveznice=soup.find_all('span', {"class" : "Poveznice"})
        for x in poveznice:
          try:
            reference=x.find_all('span')
            ref_broj="0"
            for y in reference:
              try:
                if y.attrs['class'][0]  == "Lemma__HomonymNumber":
                  ref_broj=y.string
                  print(ref_broj)
                elif y.attrs['class'][0]  == "References":
                  y.name="a"
                  if ref_broj in ["1","2","3","4","5","6","7","8","9","10"]:
                    y.attrs['href'] = "../"+str(y.string.replace("ć","c").replace("č","c").replace("ž","z").replace("š","s").replace("đ","d").replace(" ","-"))+"_"+ref_broj+"-neizvorni"
                  else:
                    y.attrs['href'] = "../"+str(y.string.replace("ć","c").replace("č","c").replace("ž","z").replace("š","s").replace("đ","d").replace(" ","-"))+"-neizvorni"
              except AttributeError:
                print(file)
          except AttributeError:
            print(file)
          
        
        span=soup.find('span', {"class" : "Lemma__LemmaSign"})
        if span==None:
          span=soup.find('span', {"class" : "Lemma_Djeca__natuknica"})
        if span==None:
          span=soup.find('span', {"class" : "Lemma_Stranci__natuknica"})
        span2=soup.find('span', {"class" : "Definicija__definicija"})
        try:
          natuknica=str(span.string.replace("%i",""))
          prvo_slovo=str(file[0])
          if str(file[-6]).isnumeric():
            abecedarij+='<a class="natuknica osnova" href="./'+natuknica+'">'+natuknica+ '<sup>'+str(file[-6])+'</sup></a>\n'
          else:
            abecedarij+='<a class="natuknica osnova" href="./'+natuknica+'">'+natuknica+'</a>\n'
        except AttributeError:
          try:
            natuknica=span.text
          except AttributeError:
            natuknica=""
        try:
          natuknica2=span2.string
        except AttributeError:
          natuknica2=""
        try:
          natuknica2=natuknica2.split("\n")
          natuknica2=natuknica2[0].lstrip().rstrip()
        except AttributeError:
          natuknica2=""
        razmak="\n"
        appendString = """<title>"""+natuknica+"""</title><meta name="description" content='"""+natuknica2+"""'>"""
        # dodavanje modula mijenjati po potrebi
        modul_link=""

        f.seek(0) # go back to the beginning of the file
        f.write(appendString) # write new content at the beginning
        # osnovni
        f.write(str(soup)+"\n")
        """if soup.find('span', {"class" : "Lemma_Stranci__natuknica"})==None:
          if natuknica in lista_s:
            #zamijeni dva i tri u pravom izvozu
            modul_link="<button class='stranci_veza'><a href='../"+natuknica.replace("ć","c").replace("č","c").replace("ž","z").replace("š","s").replace("đ","d").replace(" ","-")+"-neizvorni'>modul za osobe koje uče hrvatski kao ini jezik</a></button>"
            f.write(modul_link) 
        if soup.find('span', {"class" : "Lemma_Djeca__natuknica"})==None:
          if natuknica in lista_d:
            modul_link="<button class='deca_veza'><a href='../"+natuknica.replace("ć","c").replace("č","c").replace("ž","z").replace("š","s").replace("đ","d").replace(" ","-")+"-ucenici'>modul za učenike</a></button>"
            f.write(modul_link)"""
        f.write("\n<kraj>")
        f.close()
        try:
          if natuknica[0:2].lower()=="dž":
            os.rename(adresa+"/"+file,adresa+"/dž/"+file.replace(file[0:2],"dž"))
          elif natuknica[0:2].lower()=="lj":
            os.rename(adresa+"/"+file,adresa+"/lj/"+file.replace(file[0:2],"lj"))
          elif natuknica[0:2].lower()=="nj":
            os.rename(adresa+"/"+file,adresa+"/nj/"+file.replace(file[0:2],"nj"))
          elif natuknica[0].lower()=="ć":
            os.rename(adresa+"/"+file,adresa+"/ć/"+file.replace(file[0],"c"))
          elif natuknica[0].lower()=="č":
            os.rename(adresa+"/"+file,adresa+"/č/"+file.replace(file[0],"c"))
          elif natuknica[0].lower()=="đ":
            os.rename(adresa+"/"+file,adresa+"/đ/"+file.replace(file[0],"d"))
          elif natuknica[0].lower()=="š":
            os.rename(adresa+"/"+file,adresa+"/š/"+file.replace(file[0],"s"))
          elif natuknica[0].lower()=="ž":
            os.rename(adresa+"/"+file,adresa+"/ž/"+file.replace(file[0],"z"))
          elif natuknica[0].lower()=="a":
            os.rename(adresa+"/"+file,adresa+"/a/"+file.replace(file[0],"a"))
          elif natuknica[0].lower()=="b":
            os.rename(adresa+"/"+file,adresa+"/b/"+file.replace(file[0],"b"))
          elif natuknica[0].lower()=="c":
            os.rename(adresa+"/"+file,adresa+"/c/"+file.replace(file[0],"c"))
          elif natuknica[0].lower()=="d":
            os.rename(adresa+"/"+file,adresa+"/d/"+file.replace(file[0],"d"))
          elif natuknica[0].lower()=="e":
            os.rename(adresa+"/"+file,adresa+"/e/"+file.replace(file[0],"e"))
          elif natuknica[0].lower()=="f":
            os.rename(adresa+"/"+file,adresa+"/f/"+file.replace(file[0],"f"))
          elif natuknica[0].lower()=="g":
            os.rename(adresa+"/"+file,adresa+"/g/"+file.replace(file[0],"g"))
          elif natuknica[0].lower()=="h":
            os.rename(adresa+"/"+file,adresa+"/h/"+file.replace(file[0],"h"))
          elif natuknica[0].lower()=="i":
            os.rename(adresa+"/"+file,adresa+"/i/"+file.replace(file[0],"i"))
          elif natuknica[0].lower()=="j":
            os.rename(adresa+"/"+file,adresa+"/j/"+file.replace(file[0],"j"))
          elif natuknica[0].lower()=="k":
            os.rename(adresa+"/"+file,adresa+"/k/"+file.replace(file[0],"k"))
          elif natuknica[0].lower()=="l":
            os.rename(adresa+"/"+file,adresa+"/l/"+file.replace(file[0],"l"))
          elif natuknica[0].lower()=="m":
            os.rename(adresa+"/"+file,adresa+"/m/"+file.replace(file[0],"m"))
          elif natuknica[0].lower()=="n":
            os.rename(adresa+"/"+file,adresa+"/n/"+file.replace(file[0],"n"))
          elif natuknica[0].lower()=="o":
            os.rename(adresa+"/"+file,adresa+"/o/"+file.replace(file[0],"o"))
          elif natuknica[0].lower()=="p":
            os.rename(adresa+"/"+file,adresa+"/p/"+file.replace(file[0],"p"))
          elif natuknica[0].lower()=="r":
            os.rename(adresa+"/"+file,adresa+"/r/"+file.replace(file[0],"r"))
          elif natuknica[0].lower()=="s":
            os.rename(adresa+"/"+file,adresa+"/s/"+file.replace(file[0],"s"))
          elif natuknica[0].lower()=="t":
            os.rename(adresa+"/"+file,adresa+"/t/"+file.replace(file[0],"t"))
          elif natuknica[0].lower()=="u":
            os.rename(adresa+"/"+file,adresa+"/u/"+file.replace(file[0],"u"))
          elif natuknica[0].lower()=="v":
            os.rename(adresa+"/"+file,adresa+"/v/"+file.replace(file[0],"v"))
          elif natuknica[0].lower()=="z":
            os.rename(adresa+"/"+file,adresa+"/z/"+file.replace(file[0],"z"))
        except IndexError:
          print()
parametri=["</","<p","<s"]
abeceda=["a","b","c","d","đ","dž","e"]
for slovo in abeceda:
  for file in sorted(os.listdir(adresa+"/"+slovo)):
      broj+=1
      if file.endswith(".html"):
          f = io.open(adresa+"/"+slovo+"/"+file,'r+',encoding="utf-8", errors='ignore')
          lines1 = f.readlines() # read old content
          broj_linije=0
          for line in lines1:
            broj_linije+=1
            if line[0:3]=="<kr":
              break
          f.close()
          f = io.open(adresa+"/"+slovo+"/"+file,'w',encoding="utf-8")
          print(broj_linije)
          lines1=lines1[0:broj_linije-1]
          f.seek(0)
          f.write(str("".join(lines1)))
          f.close()
