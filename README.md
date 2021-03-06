# Flask-Mysql-API

Başlatmadan önce ana dizindeki cfg dosyasınıdaki [DB] sectionı doldurulmalıdır.

`Tüm işlemler api/execute endpoint'ine yapılmaktadır. HTTP methodları ile farklı çıktılar elde edilir.`

<hr>

## Build 

Build almak için 

```sh
docker build -t <image_ismi>:<tag> .
```

Alınan buildi çalıştırmak için 

```sh
docker run -tid -p 8080:8080 <verilenimageismi>:<tag>
```

Docker Hub üzerinden çekebilmek için

```sh
docker run -tid -p 8080:8080 anilerencelik/flask-mysql-api:0.2
```

<hr>

## SELECT

`/api/execute` endpoint ine `GET`
methodu kullanılarak istek atılmalıdır.
Query parametresi olarak tablo ismi verilebilir.

Örneğin TEST adındaki tabloyu çekmek
```sh
api/execute?tablename=TEST
```
Parametre verilmediğinde Default olarak USERS tablosunu çeker.
```sh
api/execute
```
 
<hr>

## INSERT

`POST` veya `PUT` metodu yardımıyla erişilebilir. Tüm parametrelerin body de gönderilmesi gerekir. JSON olarak body gönderilmelidir. Bir örnek

```
{
    "name": "test",
    "lastname": "test",
    "email": "a@a.com"
}
```
<hr>

## DELETE

Sadece `DELETE` metodu yardımıyla erişilebilir. Tüm parametrelerin body de gönderilmesi gerekir. JSON olarak body gönderilmelidir.

Tek veri silmek için body => 
```
{
    "id": 4
}
```
Çoklu veri silmek için body => 
```
{
    "id": [1, 2, 3, 4, 5]
}
```
Verilen tüm id'leri siler
