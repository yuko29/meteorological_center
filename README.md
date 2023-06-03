# meteorological_center


## Getting Start

To start up the app:
```
$ docker compose up
```

To stop and delete all the containers:
```
$ docker compose down
```

## Score Criteria
- 程式可以成功啟起來 – 50%
- 滿足User requirements – 20 %
- 簡報 (含user story, UI Design introduction, Architecture, and demo) – 10%
- Code with unit test(w12) – 5%
- Monitor metrics(w15) – 5%
- Follow 12 factors(w1) –每一項+1分→ 以簡報敘述，埋在扣裡不算！
  1. Codebase
  2. Dependencies
  3. Config
  4. Backing Services
  5. Build, Release, Run
  6. Processes
  7. Port Binding
  8. Concurrency
  9. Disposability
  10. Dev/Prod Parity
  11. Logs
  12. Admin Processes


## User requirements
- TSMC Meteorological center
  1. 成功爬取並呈現 1.水庫水情 2.電力負載狀況 3.地震歷史紀錄，
  各項皆5%，共15%
  2. 完成其他額外功能符合user story分數往上增加


## User Story

### Version 1
- 大壯是台積電的廠務工程師
- 他需要瀏覽台水、台電、中央氣象局等不同的網站，才能分別得知水、電、地震的狀況；進入網站後，還需要另外搜索自己所在的區域
- 因為這些網站僅客觀展現出數據，大壯還必須根據自身經驗，判斷哪些數據會對廠區營運有影響
- 他希望有個一頁式的整合頁面，根據廠區做劃分，提供各廠區所需要的水、電、氣象等資訊
- 透過一頁式的整合網頁，他可以快速地掌握地區狀況並做出預警

### Version 2
作為一位關心環境狀況的居民，你希望能夠進入應用程式，以便隨時隨地了解所居住區域的水庫、電力和地震即時狀況。

當你進入應用程式後，可以選取所在地區，應用程式會自動獲取當地水庫、電力和地震相關的數據和圖表，並精簡成圖表來呈現，可以輕易的了解目前的水庫水情、電力負載狀況和地震歷史紀錄，以便採取必要的行動。

例如：
1. 如果發現當地水庫水情較差，我可以節約用水，以減少對水庫的負擔。
2. 如果當地電力負載較高，可以避免在高峰期使用大量電力，以減少對電網的負擔。
3. 如果發生地震時，可以即時查看詳細資訊，以得知各地可能災情。

這個應用程式可以提供了實時且簡單明瞭的數據圖表，讓用戶快速了解和應對目前的水庫、電力和地震情況。

## UI Design & User Experience
1. 水庫水情
  - 提供了即時的水庫水情報告，以可視化的精簡上色圖示呈現，方便用戶直觀地比較不同水庫之間的數據和趨勢，並且可以點擊進入查看各個水庫的實時數據和歷史記錄。
2. 電力負載狀況
  - 提供了即時的電力負載狀況報告，包括及時用電量、最大供電能力，方便用戶觀看，並且可以點擊進入查看更詳細的用電情況和趨勢。
3. 地震歷史紀錄
  - 提供了最新地震紀錄，包含地震震度大小及時間，並且可以點擊進入查看歷史地震的詳細資料和相關數據。

## Application Architecture
應用程式架構包含多個部分，負責處理用戶請求、數據抓取、分析和展示圖表數據。

用戶透過 Web Frontend 輸入查詢

Web Frontend 向 Web Backend 發送請求

Web Backend 從 Database 檢索相關數據進行計算、分析和展示圖表數據。

Content Crawler 會和 target website 進行互動，自動抓取需要的資料，包括水庫水情、電力負載、地震歷史紀錄等等，儲存到database中。

整個架構旨在提供用戶可靠、高效、方便的資訊查詢和展示工具。

