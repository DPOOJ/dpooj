import React, { useEffect, useState } from 'react';
import { message, Upload } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
const { Dragger } = Upload

function FileUploader( { disabled, url, text, hint, callbackFunc } ) {
    const [curDisabled, setCurDisabled] = useState(false);
    
    useEffect(() => {
        setCurDisabled(disabled);
    }, [disabled])

    const fileProps = {
      name: 'file',
      // action: '/uploadFile',
      headers: {
        authorization: 'authorization-text',
      },
      maxCount: 1,
      onChange(info) {
        // console.log(info)
        if (info.file.status !== 'uploading') {
          // console.log('uploading', info.file, info.fileList);
        }
        if (info.file.status === 'done') {
          let code = info.file.response.code
          let inf = info.file.response.info
          // console.log('upload', info.file.response)
          if (code == 0) {
            message.success(`${info.file.name}上传成功`);
          } else {
            message.error(inf)
          }
        } else if (info.file.status === 'error') {
          message.error(`${info.file.name} file upload failed.`);
        }
      },
      beforeUpload(file){
        if (file.type !== 'text/plain') {
          callbackFunc('你刚刚提交的输入无法被自动解析>_<!')
          return true;
        }
        const reader = new FileReader();
        reader.onload = e => {
            // console.log(e.target.result);
            callbackFunc(e.target.result);
        };
        reader.readAsText(file);
        return true;
    }
  };

    return (
        <div>
            <Dragger {...fileProps} disabled={curDisabled} action={url}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">{text}</p>
                <p className="ant-upload-hint">{hint}</p>
            </Dragger>
        </div>
    );
}

export default FileUploader;
