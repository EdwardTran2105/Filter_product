import json

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用
# 复制该 Demo 后, 需要将 "YOUR_APP_ID", "YOUR_APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def DB():
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a63f1c47b3b8d010") \
        .app_secret("hRcpoJJ3WDr0K0w9kR0T6eVJ7y0pDhEX") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: ListAppTableRecordRequest = ListAppTableRecordRequest.builder() \
        .app_token("IkF8bLyBBau9desAkQllY8JKgud") \
        .table_id("tbloP02DaJyGPE2Q") \
        .build()

    # 发起请求
    response: ListAppTableRecordResponse = client.bitable.v1.app_table_record.list(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.bitable.v1.app_table_record.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    records_container = []

    # Duyệt qua từng item trong response và thêm vào records_container
    for item in response.data.items:
        record_data = {
            "Mã vật tư": item.fields.get("Mã vật tư", ""),
            "Màu": item.fields.get("Màu", ""),
            "Record ID": item.record_id,
            "m2": item.fields.get("m2","")
        }
        records_container.append(record_data)
    
    for item in records_container:
        print (item)

if __name__ == "__main__":
    DB()
