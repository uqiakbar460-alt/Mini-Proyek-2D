import os

header=["User_ID","Product_ID","Category","Price (Rs.)","Discount","Final_Price (Rs.)","Payment_Method","Purchase_Date"]

def file(file):
    return os.path.exists(file)

def angka_valid(teks):
    teks=teks.strip()
    if teks == "":
        return False
    bagian = teks.split(".")
    if len (bagian) > 2:
        return False
    for b in bagian:
        if not b.isdigit():
            return False

    return True