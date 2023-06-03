# 在本機、cluster啟動mongoDB docker
執行
```
bash prepare_db.sh -ip your_ip -network your_network
```
port預設為27017:27017

# DB schema
總共有4個collection
- earthquake
```
    "schema":{
        "time": datetime.datetime
        "focal_dep": float, 
        "longitude": float,
        "latitude": float
    }
```
Note: datetime格式 = `"%Y-%m-%d %H:%M:%S"`，格式為字串


- reservoir
```
    "schema":{
        'time': datetime.datetime,
        'percentage': float,
        'water_supply': float,
        'name': str
    }
```

- factory
```
    "schema":{
        'factory': str,
        'time': datetime.datetime,
        'M_L': float,
        'focal_dep': float,
        'longitude': float,
        'latitude': float,
        'magnitude': float
    }
```
Note: magnitude是指這次地震對該廠區的震度

- electricity
```
    "schema":{
        'region': str,
        'power_usage': float,
        'power_generate': float,
        'time': datetime.datetime
    }
```

# API

## Insert data
- insert_earthquake_data(data: Union[dict, list])
    - 輸入資料須包含對各廠區的震度計算結果
    - 僅此API可接受batch input (type = list)
    - 必要欄位
        - time: datatime/str
        - magnitude: dict(對各廠區的震度資訊)
- insert_electricity_data(data: dict)
    - 必要欄位
        - region: str
- insert_reservoir_data(data: dict)
    - 必要欄位
        - name: str (水庫名稱)

## Retrieve data
- retrieve_reservoir_data_by_name(quantity: int, name: str)
- retrieve_electricity_data_by_region(quantity: int, region:str)
- retrieve_earthquake_data(quantity: int)
- retrieve_earthquake_data_by_factory(quantity: int, factory: str)

## 其他開放API
- reset()
    - 這個method會洗掉整個DB
- clean_collection(collection: str)
    - 洗掉特定collection的所有資料 (collection列表見schema)
- clean_all_collection()
    - 功能同reset

## Constructor
- \_\_init\_\_(
    ip: Optional[str] = None,
    port: Optional[int]=None,
    db_name: Optional[str] = "my_mongoDB",
    collection_list:  Optional[list] = None
)
    - 這些參數都是可選，如果不給ip、port、collection_list的話則預設從db_config讀取
    - db_name會影響到實際存取的DB，不用更動

- 不更動到db_config的狀況下，db instance可以不用給參數就啟動

## DB執行範例
```
python3 API_example.py
```



## 2023/6/1 Note:
- **因為有改到API name(為了符合PEP8)，所以大家注意一下現在更名後的API name**

- **因為有改到DB程式的名子(為了符合PEP8)，所以大家把import改成`from db.MongoDB import MongoDB`**

- **因為DB架構有重構，現在要架設DB到cluster前不再需要先跑generate_schema.py了**

- 移除insert_schema.py，改由 [HeywardLiu](https://github.com/HeywardLiu) 提供的strongtyping檢查資料型態，保持基本驗證性的同時讓輸入更自由
- 感謝 [HeywardLiu](https://github.com/HeywardLiu) 提供的超猛架構跟為DB付出的心力