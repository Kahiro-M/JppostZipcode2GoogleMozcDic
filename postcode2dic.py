import pathlib
import pandas as pd
import sys
import os
import tkinter, tkinter.filedialog, tkinter.messagebox
import urllib.request
import zipfile

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

def downloadFile(url, fileName):
    try:
        with urllib.request.urlopen(url) as response:
            with open(fileName, 'wb') as out_file:
                out_file.write(response.read())
        # print(f"Downloaded file saved as: {fileName}")
    except Exception as e:
        tkinter.messagebox.showinfo('GoogleMozc向け郵便番号辞書作成ツール',url+'をダウンロードできませんでした。終了します。')
        print(f"Error occurred: {e}")
        sys.exit()

def unzipRemove(zipFilePath):
    try:
        # ZIPファイルの解凍
        with zipfile.ZipFile(zipFilePath, 'r') as zip_ref:
            zip_ref.extractall(os.path.dirname(zipFilePath))
        # print(f"Unzipped file: {zipFilePath}")

        # 元のZIPファイルを削除
        os.remove(zipFilePath)
        # print(f"Deleted original zip file: {zipFilePath}")
        
    except Exception as e:
        tkinter.messagebox.showinfo('GoogleMozc向け郵便番号辞書作成ツール','ZIPファイルを解凍できませんでした。終了します。')
        print(f"Error occurred: {e}")
        sys.exit()

if __name__ == '__main__':
    dir_path = './'

    if(len(sys.argv)<2):
        tkinter.messagebox.showinfo('GoogleMozc向け郵便番号辞書作成ツール','住所の郵便番号最新全データ（.zip）を選択してください。\n未選択の場合は郵便局のHPから最新版を自動取得します。')
        # ファイル選択ダイアログの表示
        root = tkinter.Tk()
        root.withdraw()
        fTyp = [("","")]
        iDir = os.path.abspath(dir_path)
        file = tkinter.filedialog.askopenfilename(initialdir = iDir)
        fileList = [file]
    else:
        fileList = sys.argv[1:]
    if(len(fileList)<2 and fileList[0]==''):
        url = 'https://www.post.japanpost.jp/zipcode/dl/utf/zip/utf_ken_all.zip'  # ダウンロードしたいファイルのURL
        fileName = 'least.zip'  # 保存先のファイル名
        downloadFile(url, fileName)
        fileList = [fileName]

    unzipRemove(fileList[0])

    zipAllCsv = 'utf_ken_all.csv'

    # カレントディレクトリを取得
    curtDir = os.getcwd()
    
    # ファイルのフルパスを作成
    zipAllCsvPath = os.path.join(curtDir, zipAllCsv)
    if(os.path.isfile(zipAllCsvPath)):
        toDic(zipAllCsv)
        os.remove(zipAllCsv)
        tkinter.messagebox.showinfo('GoogleMozc向け郵便番号辞書作成ツール',curtDir+'\n　・JpPostDic.txt\n　・JpPostDicWithHyphen.txt\nを生成しました。')
    else:
        tkinter.messagebox.showinfo('GoogleMozc向け郵便番号辞書作成ツール',zipAllCsvPath+'が見付かりません。')
