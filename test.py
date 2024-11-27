import json

import lark_oapi as lark
from lark_oapi.api.task.v2 import *


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 以下示例代码是根据 API 调试台参数自动生成，如果存在代码问题，请在 API 调试台填上相关必要参数后再使用
def main():
    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
    client = lark.Client.builder() \
        .enable_set_token(True) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: UploadAttachmentRequest = UploadAttachmentRequest.builder() \
        .user_id_type("") \
        .request_body(InputAttachment.builder()
            .resource_type()
            .resource_id("b59aa7a3-e98c-4830-8273-cbb29f89b837")
            .file()
            .build()) \
        .build()

    # 发起请求
    option = lark.RequestOption.builder().user_access_token("u-fQlMXW6dB3pp1422u5v_fy1gltp_04ZziGG0lky00as7").build()
    response: UploadAttachmentResponse = client.task.v2.attachment.upload(request, option)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.task.v2.attachment.upload failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))


if __name__ == "__main__":
    main()