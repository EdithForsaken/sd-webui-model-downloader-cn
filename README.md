## sd-webui-model-downloader-cn
> **DOWNLOAD**
- Model civitai pengunduhan berkecepatan tinggi tanpa tangga dalam negeri
- Pengunduhan sekali klik, pengenalan otomatis jenis model, pemilihan jalur pengunduhan otomatis
- pembantuCheckpoint、LoRA、LyCORIS、VAE、TextualInversion(embedding)、Hypernetwork
- Mendukung pratinjau gambar model dan secara otomatis mengunduh gambar model ke direktori yang sama dengan model

![](https://files.tzwm.me/images/sd-webui-model-downloader-cn/preview.png)


## Instalasi

### Instalasi langsung melalui webui (disarankan)

![](https://files.tzwm.me/images/sd-webui-model-downloader-cn/extension_install.png)


### unduh dan pasang

1. Unduh semua file dari repositori ini
2. Buka ritsletingnya dan lemparkan seluruh folder ke dalam direktori ekstensi di direktori webui.
3. Memulai ulang webui

###Penginstalan baris perintah

1. Buka folder webui dari baris perintah
2. Implementasi

```
cd extensions && git clone --depth 1 https://github.com/tzwm/sd-webui-model-downloader-cn.git
```

3.  重启 webui

## memanfaatkan

### Unduh berbagai versi model yang berbeda

![](https://files.tzwm.me/images/sd-webui-model-downloader-cn/banner_url_tips.png)

## TODO

- [ ] Tampilan kemajuan pengunduhan
- [x] Mempratinjau informasi lebih lanjut tentang model, termasuk gambar, dll.
- [ ] Rekomendasi Model
- [ ] Setelah mengunduh LoRA, sebuah file wildcard secara otomatis dibuat yang berisi kata-kata pemicu, yang memudahkan pemicu sekali klik berikutnya untuk diaktifkan tanpa harus mencari kata-kata pemicu di mana-mana.

##Pertukaran bantuan timbal balik


![]([https://oss.talesofai.cn/public/qrcode_20230413-183818.png?cc0429](https://i.ibb.co/pwKsh1t/image-1.png))

## ChangeLog

- v1.1.3 20230629
  - Memperbaiki sedikit kesalahan saat memasukkan alamat yang salah.
- v1.1.0 20230624
  - Menambahkan pratinjau gambar model, dan secara otomatis mengunduh gambar model ke direktori yang sama dengan model.
- v1.0.1 20230621
  - Mencoba memperbaiki masalah di mana file util.py tidak dapat dimuat pada beberapa platform.
- v1.0.0 20230621
  - Implementasi pengunduhan otomatis bebas tangga dasar
