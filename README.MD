# Batik Stereogram
---

# Table of Content

1. [Instalasi](#instalasi)
2. [Persiapan Database](#persiapan-database)
3. [Deploy](#deploy)
4. [Catatan](#catatan)
5. [Credits](#credits)


## Instalasi
Clone repository ini, masuk ke direktori hasil clone lalu jalankan instalasi.

> git clone https://github.com/lantip/batikstereo

> cd batikstereo

> pip install -r requirements.txt

## Persiapan Database

> flask db init

> flask db migrate -m 'Initial migration'

> flask db upgrade

## Deploy
> python app.py

## Catatan
Untuk menambahkan pattern batik, gunakan pattern ukuran 140 x 140 pixel. Tambahkan image (png atau jpg) pattern tersebut ke direktori `static/img/pattern`.

Jika ingin menambahkan detil keterangan mengenai batik tersebut, tambahkan file html di dalam direktori `templates/batik`.

Gunakan nama sama untuk image pattern dan html file tentang batiknya. 

## Credits
- Autostereogram dikembangkan dari [Denil Sonsa](https://bitbucket.org/denilsonsa/autostereogram)
- Themes menggunakan [Tabler](https://tabler.io)
- Background Image dari [GarryKillian / Freepik](https://freepik.com)
