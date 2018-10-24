# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 22:21:21 2018

@author: Eduardo
"""

import os
import re
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def extrairCNJparaTXT(pdfOrigem):
    pagenums = set()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(pdfOrigem, 'rb')
    txtSaida = pdfOrigem.replace('.pdf', '.txt').replace('PDF_', 'TXT_')
    
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)

    cnjs = re.findall('\d{4,7}-\d{2}.\d{4}.\d{1}.\d{2}.\d{4}', output.getvalue())

    for cnj in cnjs:
        with open(txtSaida, "a") as myfile:
            myfile.write(cnj+'\n')     
    
    infile.close()
    converter.close()
    output.close()
    
def buscaPDFs(diretorioRaiz): 
    listaArquivos = []
    for dirName, subdirList, fileList in os.walk(diretorioRaiz):
        if os.path.exists(dirName.replace('PDF_', 'TXT_')) == False:
            os.makedirs(dirName.replace('PDF_', 'TXT_'))   
            
        for fname in fileList:
            listaArquivos.append(dirName+'\\'+fname)
    return listaArquivos

def removerCNJDuplicados():
    infilename= r'D:\Faculdade\TCC\Arquivos\TXT_Extraido\saida.txt'
    outfilename = r'D:\Faculdade\TCC\Arquivos\TXT_Extraido\saida2.txt'
    lines_seen = set() # holds lines already seen
    outfile = open(outfilename, "w")
    for line in open(infilename, "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    

pastaRaiz = r'D:\Faculdade\TCC\Arquivos\PDF_Extraido'
arquivosPdfs = buscaPDFs(pastaRaiz)

for arquivo in arquivosPdfs:
    extrairCNJparaTXT(arquivo)
