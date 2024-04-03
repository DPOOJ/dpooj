import React, { useEffect, useState } from 'react';
import { message, Upload } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
const { Dragger } = Upload

const fileProps = {
    name: 'file',
    action: '/uploadFile',
    headers: {
      authorization: 'authorization-text',
    },
    onChange(info) {
      console.log(info)
      if (info.file.status !== 'uploading') {
        // console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        // message.success(`${info.file.name} file uploaded successfully`);
        let code = info.file.response.code
        let inf = info.file.response.info
        console.log('upload', info.file.response)
        if (code == 0) {
          message.success(`${info.file.name} file uploaded successfully`);
        } else {
          message.error(inf)
        }
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} file upload failed.`);
      }
    },
    maxCount: 1,
};

function FileUploader({disabled}) {
    const [curDisabled, setCurDisabled] = useState(false);
    
    useEffect(() => {
        setCurDisabled(disabled);
    }, [disabled])

    return (
        <div style={{maxWidth: '200px'}}>
            <Dragger {...fileProps} disabled={curDisabled}>
                <p className="ant-upload-drag-icon">
                    <InboxOutlined />
                </p>
                <p className="ant-upload-text">点击或拖拽上传.jar文件</p>
                <p className="ant-upload-hint">请确保文件使用jdk1.8打包</p>
            </Dragger>
        </div>
    );
}

export default FileUploader;
