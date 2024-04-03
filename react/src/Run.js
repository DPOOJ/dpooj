// Run.js
import React, { useState, useEffect } from 'react';
import { Row, Col, Input, Button, Space, Dropdown, message, Divider, Typography, Drawer, Checkbox } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import FileUploader from './FileUploader';
const { TextArea } = Input;
const { Paragraph } = Typography;

const hwIDs = [
  {
    label: '作业 1',
    key: '1',
  },
  {
    label: '作业 2',
    key: '2',
  },
  {
    label: '作业 3',
    key: '3',
  },
  {
    label: '作业 5',
    key: '5',
  },
];

function Run( { logged } ) {
  const [submitAvilable, setSubmitAvilable] = useState(false);
  const [onJudging, setOnJudging] = useState(false);
  const [hwID, setHwID] = useState(5);
  const [inputData, setInputData] = useState('');
  const [selectedErr, setSelectErr] = useState('好像还没有错误')
  const [showErrDrawer, setShowErrDrawer] = useState(false);

  useEffect(() => {
    if (!logged) {
      setOnJudging(false);
      setSubmitAvilable(false);
    } else {
      setSubmitAvilable(true);
    }
  }, [logged]);

  useEffect(() => {
    if (!logged) {
      setSubmitAvilable(false);
    } else {
      setSubmitAvilable(!onJudging);
    }
  }, [onJudging]);

  function chooseHw( { key } ) {
    setHwID(parseInt(key));
    message.success(`运行调整至作业 ${key}`);
  };

  function startSubmit() {
    if (inputData == '') {
      message.error("你还什么都没有输入>_<");
      return;
    }
  }

  function onTextAreaChange(e) {
    setInputData(e.target.value);
  }
  function translateText(text) {
    if (text == '') {
      return <p style={{color: '#DBDBDB'}}>还没有内容可以显示{'>_<;'}</p>
    }
    const paragraphs = text.split('\n').map((paragraph, index) => (
      <div key={index} style={{lineHeight:'22px', wordBreak:'break-all', wordWrap: 'break-word'}}>{paragraph}</div>
    ));
    return paragraphs;
    // return text.replaceAll('\n', '<br />')
  }
  function enterErrDrawer() {
    setShowErrDrawer(true);
  }
  function closeErrDrawer() {
    setShowErrDrawer(false);
  }
  function translateTextToCheckbox(text) {
    if (text == '') {
      return <p style={{color: '#DBDBDB'}}>还没有内容可以显示{'>_<;'}</p>
    }
    const paragraphs = text.split('\n').map((paragraph, index) => (
      <Checkbox key={index}>{paragraph}</Checkbox>
    ));
    return <Space direction='vertical'>{paragraphs}</Space>;
  }

  function test() {
    setOnJudging(!onJudging);
  }
  

  return (
    <>
      <Row wrap={false}>
        <Col>
          <Row>
            <Col 
              flex={'240px'}
              align={'center'} 
              style={{
                padding: '20px',
                border: '1px dashed',
                borderRadius: '10px',
              }}
            >
              <Space direction='vertical' size={20}>
                <Dropdown
                  menu={{
                    items: hwIDs,
                    onClick:chooseHw,
                  }}
                  disabled={!submitAvilable}
                >
                  <a onClick={(e) => e.preventDefault()}>
                    <Space>
                      <h2>进度：作业{hwID}</h2>
                      <DownOutlined />
                    </Space>
                  </a>
                </Dropdown>
                <FileUploader disabled={!submitAvilable}/>
                <Button
                  type="primary"
                  loading={onJudging}
                  disabled={!submitAvilable}
                  style={{backgroundColor: 'green'}}
                  onClick={startSubmit}
                >
                  Submit
                </Button>
                <Button onClick={test}>test</Button>
              </Space>
            </Col>
          </Row>
        </Col>
        <Col flex={'auto'} style={{marginLeft: 30}}>
          <Row>
            <Col>
              <h3>错误信息：</h3>
              <div>
                {translateText(inputData)}
              </div>
              {/* <p>{selectedErr}</p> */}
              {/* <Button type='link' onClick={enterErrDrawer}>显示更多</Button> */}
            </Col>
          </Row>
          <Divider></Divider>
          <Row>
            <Col flex={'auto'} style={{}} span={12}>
              <h3>Input:</h3>
              <TextArea 
                placeholder="please enter your input here" 
                autoSize={{minRows: 1}} 
                onChange={onTextAreaChange}
                disabled={!submitAvilable}
              />
            </Col>
            <Col flex={'auto'} style={{marginLeft: 30}} span={12}>
              <h3>Output:</h3>
              <div style={{
                border: '1px solid',
                borderRadius: '8px',
                borderColor: '#DBDBDB',
                paddingTop: '5px',
                paddingBottom: '5px',
                paddingLeft: '10px',
                paddingRight: '10px',
                }}
              >
                {translateText(inputData)}
              </div>
            </Col>
          </Row>
        </Col>
      </Row>
      <Drawer
        title="Error Information"
        placement='left'
        closable={false}
        onClose={closeErrDrawer}
        open={showErrDrawer}
        key='errDrawer'
      >
        {translateTextToCheckbox(inputData)}
      </Drawer>
    </>
  );
}

export default Run;
