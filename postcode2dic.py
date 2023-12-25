import pathlib
import pandas as pd

def toDic(inputFile):
    outputFile = inputFile.rsplit('.', 1)[0] + '.csv'
    zipcode = pd.read_csv(inputFile, header=None, dtype=str).fillna('').replace('nan','')
    type = pd.DataFrame(['地名']*len(zipcode[2]))
    dic = pd.DataFrame([
        zipcode[2],
        zipcode[6].replace('0','')+zipcode[7].replace('0','')+zipcode[8].replace('0',''),
        type[0]
        ],index=['zip','address','type']).transpose()
    dic.to_csv('JpPostDic.txt', index=False, header=False, sep='\t')

    dicWithHyphen = pd.DataFrame([
        zipcode[2].str[:3]+'-'+zipcode[2].str[3:],
        zipcode[6].replace('0','')+zipcode[7].replace('0','')+zipcode[8].replace('0',''),
        type[0]
        ],index=['zip','address','type']).transpose()
    dicWithHyphen.to_csv('JpPostDicWithHyphen.txt', index=False, header=False, sep='\t')


# 使用例
inputFile = input("変換したいファイルのパスを入力してください: ")

toDic(inputFile)
