給自己參考用

insert_schema:
用於確認輸入的資料是否格式正確且沒有遺漏，並非真實結構

```
[
    {
        "collection_name": "earthquake",
        "schema":{
            "time": "datetime", 
            "focal_dep": "float", 
            "longitude": "float",
            "latitude": "float"
        }
    },
    {
        "collection_name":"reservoir",
        "schema":{
            "name":"",
            "data":[]
        }
    },
    {
        "collection_name":"electricity",
        "schema":{
            "region":"",
            "data":[]
        }
    },
    {
        "collection_name":"factory",
        schema:{
            "name":"",
            
        }
    }
]
```