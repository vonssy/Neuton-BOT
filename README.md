# Neuton BOT
Neuton BOT

Register Here : [Neuton](https://t.me/NEUTON2024Bot/neuton?startapp=kentId1493482017)

## Fitur

  - Auto Get Account Information
  - Auto Complete Task
  - Multi Account

## Prasyarat

Pastikan Anda telah menginstal Python3.9 dan PIP.

## Instalasi

1. **Kloning repositori:**
   ```bash
   git clone https://github.com/vonssy/Neuton-BOT.git
   ```
   ```bash
   cd Neuton-BOT
   ```

2. **Instal Requirements:**
   ```bash
   pip install -r requirements.txt #or pip3 install -r requirements.txt
   ```

## Konfigurasi

- **query.txt:** Anda akan menemukan file `query.txt` di dalam direktori proyek. Pastikan `query.txt` berisi data yang sesuai dengan format yang diharapkan oleh skrip. Berikut adalah contoh format file:

  ```bash
  query_id=
  user=
  ```

### How To Get FreeDogs Query

Kamu dapat copy dan paste kode berikut di console pada DevTools untuk memperoleh query yang dibutuhkan, jangan lupa `allow pasting` dahulu jika pertama kali menggunakan console.

```bash
let value = sessionStorage.getItem('tapps/launchParams');
value = value.replace(/^"|"$/g, '');

let tgWebAppDataStart = value.indexOf('query_id%3D');

if (tgWebAppDataStart === -1) {
    tgWebAppDataStart = value.indexOf('user%3D');
}

if (tgWebAppDataStart !== -1) {
    let tgWebAppData = value.substring(tgWebAppDataStart);
    let ampersandPos = tgWebAppData.indexOf('&');

    if (ampersandPos !== -1) {
        tgWebAppData = tgWebAppData.substring(0, ampersandPos);
    }

    let decodedUserData = decodeURIComponent(tgWebAppData);
    let updatedUserData = decodedUserData.replace(/%25/g, '%');

    copy(updatedUserData);
    console.log('Query Id is copied.');
} else {
    console.log('Query Id not found.');
}
```

## Jalankan

```bash
python bot.py #or python3 bot.py
```

## Penutup

Terima kasih telah mengunjungi repository ini, jangan lupa untuk memberikan kontribusi berupa follow dan stars.
Jika Anda memiliki pertanyaan, menemukan masalah, atau memiliki saran untuk perbaikan, jangan ragu untuk menghubungi saya atau membuka *issue* di repositori GitHub ini.

**vonssy**