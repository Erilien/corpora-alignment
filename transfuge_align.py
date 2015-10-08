# coding: utf-8

import sys, os, re, codecs
import unicodedata

source = codecs.open("corpus-atal/termer_source/corpus.lem", "r", "utf-8")
target = codecs.open("corpus-atal/termer_target/corpus.lem", "r", "utf-8")

source_string = source.read()
target_string = target.read()
source_tokens = source_string.split(" ")
target_tokens = target_string.split(" ")
#result_source = codecs.open("resultat_source", "w", "utf-8")
#result_target = codecs.open("resultat_target", "w", "utf-8")
#result_transfuge = codecs.open("resultat_transfuges", "w", "utf-8")
#result_cognats = codecs.open("resultat_cognats", "w", "utf-8")
result_stat = codecs.open("resultat_stats", "w", "utf-8")
result_precision = codecs.open("resultat_precision", "w", "utf-8")
final_source_dico = {}
final_target_dico = {}
final_source_lst = []
final_target_lst = []
transfuge_lst = []
cognat_lst = []

good_pos_fr = ["SBC", "ADJ", "ADJ2PAR", "ADJ1PAR", "VCJ", "ADV"]
good_pos_en = ["NN", "JJ", "NNS", "NNP", "VBG", "VB", "VBZ", "VBN"]

for token in source_tokens:
  pos = token.split("/")[0].split(":")[0]
  lemma = token.split("/")[-1].split(":")[0]
  lemma = unicodedata.normalize('NFD', lemma).encode('ascii', 'ignore')
  if not pos in good_pos_fr:
    if not lemma.lower() in final_source_dico.keys():
      final_source_dico[lemma.lower()]=1
    else:
      final_source_dico[lemma.lower()] += 1

for elt in final_source_dico:
  #result_source.write(elt + " = " + str(final_source_dico[elt]) + "\n")
  if final_source_dico[elt] > 1:
    final_source_lst.append(elt)
    
for token in target_tokens:
  if "/" in token:
    pos = token.split("/")[1]
    lemma = token.split("/")[-2]
    if not pos in good_pos_en:
      if not lemma.lower() in final_target_dico.keys():
  			final_target_dico[lemma.lower()]=1
      else:
  		  final_target_dico[lemma.lower()] += 1
			
for elt in final_target_dico:
	#result_target.write(elt + " = " + str(final_target_dico[elt]) + "\n")
	if final_target_dico[elt] > 1:
		final_target_lst.append(elt)
		
for elt in final_source_lst:
  if elt in final_target_lst:
    transfuge_lst.append(elt)
    #result_transfuge.write(elt + "\n")
  
for elt_source in final_source_lst:
  if len(elt_source) > 4 and not elt_source in transfuge_lst:
    prefixe_src = elt_source[:4]
    for elt_target in final_target_lst:
      target_src = elt_target[:4]
      if prefixe_src == target_src:
        cognat_lst.append((elt_source, elt_target))
        #result_cognats.write(elt_source+" : "+elt_target+"\n")
        

result_stat.write(str(len(final_source_lst)) + " mots francais \n" + str(len(final_target_lst)) + " mots anglais \n" + str(len(transfuge_lst)) + " transfuges \n" + str(len(cognat_lst)) + " cognats \n")

#result_source.close()
#result_target.close()
#result_transfuge.close()
#result_cognats.close()
result_stat.close()

source.close()
target.close()