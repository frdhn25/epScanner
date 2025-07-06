#!/usr/bin/python

#Author Firdhan Happyanda

import requests                         # Untuk mengirim request HTTP
from bs4 import BeautifulSoup           # Untuk parsing struktur HTML
from urllib.parse import urljoin        # Untuk gabungkan URL relatif menjadi absolut
import argparse                         # Untuk parsing input argumen CLI (contoh: -u https://...)


# Fungsi utama: deteksi form POST dan parameternya
def find_post_forms(url):
    try:
        # Ambil isi HTML dari URL target
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Error jika status bukan 200
    except Exception as e:
        print(f"[!] Gagal mengakses URL: {e}")
        return []

    # Parsing HTML menggunakan BeautifulSoup dan parser lxml
    soup = BeautifulSoup(response.text, "lxml")

    # Temukan semua <form> yang method-nya POST
    forms = soup.find_all("form", method=lambda m: m and m.lower() == "post")

    # Jika tidak ada form POST
    if not forms:
        print("\n[!] Tidak ditemukan form dengan method POST.")
        return []

    result = []  # Menyimpan hasil akhir

    # Loop semua form yang ditemukan
    for i, form in enumerate(forms, start=1):
        # Ambil endpoint dari atribut action
        action = form.get("action")
        full_url = urljoin(url, action) if action else "[NO ACTION]"

        param_names = []  # Menyimpan nama-nama parameter

        # Ambil semua <input> dengan name, dan exclude input type="reset"
        for input_tag in form.find_all("input"):
            name = input_tag.get("name")
            input_type = input_tag.get("type", "").lower()
            if name and input_type != "reset":  # Exclude jika type reset
                param_names.append(name)

        # Ambil semua <select name="...">
        for select_tag in form.find_all("select"):
            name = select_tag.get("name")
            if name:
                param_names.append(name)

        # Ambil semua <textarea name="...">
        for textarea_tag in form.find_all("textarea"):
            name = textarea_tag.get("name")
            if name:
                param_names.append(name)

        # Cetak hasil dari form
        print(f"\n[+] Form {i}")
        print(f"[*] Endpoint (action): {full_url}")
        if param_names:
            print("Parameter:")
            for param in param_names:
                print(f" - {param}")
        else:
            print("Parameter: [Tidak ada parameter ditemukan]")

        # Simpan hasil form ke list
        result.append({
            "endpoint": full_url,
            "params": param_names
        })

    return result


# Blok utama: menerima input dari terminal (via -u atau --url)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deteksi Form POST dan Parameter HTML")
    parser.add_argument("-u", "--url", required=True, help="URL target (contoh: https://example.com)")
    args = parser.parse_args()

    target_url = args.url.strip()

    # Validasi format URL
    if not target_url.startswith(("http://", "https://")):
        print("[!] URL harus diawali dengan http:// atau https://")
    else:
        hasil = find_post_forms(target_url)
        if not hasil:
            print("\n[!] Tidak ditemukan endpoint POST atau parameter.")
