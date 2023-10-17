# UAA

Unifi Access 打卡紀錄後台系統 - UAA

## Start

 Mac 或 Windows下載 [Docker Desktop](https://www.docker.com/products/docker-desktop) ， 若是 Linux 下載 [Docker Engine](https://docs.docker.com/engine/install/)

點擊綠色按鈕「Code」 後，選擇「 Download ZIP 」即可下載

在此目錄中啟用該服務 :



```shell
docker compose up   # /path/to/UnifiAccessAttendance-main  ;  Windows's Powershell or MAC's Terminal
```
若是 Linux :

```shell
sudo docker-compose up   # /path/to/UnifiAccessAttendance-main
```

至任一瀏覽器 (e.g., Chrome, Edge) 輸入 [localhost:4000](http://localhost:4000) 即可前往 UAA

## Use

1. 第一次使用需設定 Unifi IP
2. 於原系統建立 Unifi OS 帳號
3. 透過 Unifi OS 帳號登入 UAA

## Notes

* Unifi Access 版本需  v1.9.1 或更高
* 僅有 Unifi Access 權限為 FullManagement 才可使用 UAA

## Programming Language Framework

Frontend - [Vud.js](https://vuejs.org/) ,  Backend - [Fastapi](https://fastapi.tiangolo.com/)
