// Run.js
import React, { useState, useEffect } from 'react';
import { Row, Col, Input, Button, Space, Dropdown, message, Divider, Typography, Drawer, Checkbox, Tabs } from 'antd';
import { BrowserRouter as Router, Route, Routes, NavLink, Link } from 'react-router-dom';
import { DownOutlined, DownloadOutlined } from '@ant-design/icons';
import FileUploader from './FileUploader';
import axios from 'axios';
import { error } from 'jquery';
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
  {
    label: '作业 6',
    key: '6',
  },
  {
    label: '作业 7',
    key: '7',
  }
];

function Run( { logged, selfTestCallback } ) {
  const [submitAvilable, setSubmitAvilable] = useState(false);
  const [onJudging, setOnJudging] = useState(false);
  const [hwID, setHwID] = useState(7);
  const [inputData, setInputData] = useState('');
  const [resultData, setResultData] = useState({
    'debuginfo': '什么都没有>_<',
    'debuginfo_path': '',
    'log': '这里也什么都没有>_<',
    'log_path': '',
    'out': '什么都没有>_<',
    'out_path': '',
    'in': '什么都没有>_<',
    'in_path': ''
  })
  const [showErrDrawer, setShowErrDrawer] = useState(false);
  const [selectInput, setselectInput] = useState('2');
  
  const inputItems = [
    {
      label: '手动输入',
      key: '1',
      // disabled: true,
      children: (
        <>
          <Button type='primary' style={{marginBottom: '18px'}} onClick={() => {
            let postdata = {'Text': inputData}
            // console.log(postdata)
            axios.post('/uploadSelfTestInputText', postdata)
              .then(res => {
                message.success('上传成功')
                setselectInput('2');
              })
              .catch(err => {
                message.error('上传失败')
              })
          }}>提交输入</Button>
          <TextArea 
            placeholder="please enter your input here" 
            autoSize={{minRows: 1}} 
            onChange={onInputTextAreaChange}
            disabled={!submitAvilable}
          />
        </>
      )
    },
    {
      label: '显示输入',
      key: '2',
      // disabled: true,
      children: (
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
      )
    },
    {
      label: '上传文件',
      key: '3',
      children: (
        <FileUploader 
          disabled={!submitAvilable}
          url='/uploadSelfTestInputFile'
          text={'点击或拖拽上传输入文件'}
          hint={'请确保输入的合法性，最好上传.txt文件，而且最好别太长，不然卡的结束不了评测'}
          callbackFunc={uplaodCallback}
        />
      )
    },
  ]
  useEffect(() => {
    if (!logged) {
      setOnJudging(false);
      setSubmitAvilable(false);
    } else {
      getResult();
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
    setOnJudging(true);
    axios.post('/uploadSelfTestArgs', {
      'hwID': hwID
    })
      .then(res => {
        axios.post('/startSelfTest')
          .then(res => {
            message.success('运行结束')
            let data = res.data;
            console.log('result', data);
            setResultData(data);
            setOnJudging(false);
          })
          .catch(err => {
            message.error('开始运行失败')
            setOnJudging(false);
          })
      })
      .catch(err => {
        message.error('上传参数失败')
        setOnJudging(false);
      })
  }

  function getResult() {
    axios.post('/updateSelfTest')
      .then(res => {
        let data = res.data;
        setResultData(data);
        setInputData(data.in);
      })
      .catch(err => {

      })
  }

  function onInputTextAreaChange(e) {
    setInputData(e.target.value);
  }
  function translateText(text) {
    if (text == '') {
      return <p style={{color: '#DBDBDB'}}>没有可以显示的东西{'>_<;'}</p>
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
  function onInputChooseChange(e) {
    setselectInput(e.target)
  }
  function downloadText(text, filename) {
    const content = text;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    
    URL.revokeObjectURL(url);
    document.body.removeChild(link);
  }
  function downloadOInput() {
    downloadText(inputData, 'input.txt');
  }
  function downloadOutput() {
    downloadText(resultData.out, 'output.txt');
  }
  function downloadDebugInfo() {
    downloadText(resultData.debuginfo, 'debuginfo.txt');
  }
  function downloadLog() {
    downloadText(resultData.log, 'log.txt');
  }
  function uplaodCallback(text) {
    setInputData(text);
    setselectInput('2');
  }
  function onLinkToAnalzeClick()  {
    selfTestCallback(inputData, resultData.out)
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
                <div style={{maxWidth: '200px'}}>
                  <FileUploader 
                    disabled={!submitAvilable}
                    url='/uploadFile'
                    text={'点击或拖拽上传.jar文件'}
                    hint={'请确保文件使用jdk1.8打包'}
                    callbackFunc={(res) => {}}
                  />
                </div>
                <Button
                  type="primary"
                  loading={onJudging}
                  disabled={!submitAvilable}
                  style={{backgroundColor: 'green'}}
                  onClick={startSubmit}
                >
                  Submit
                </Button>
              </Space>
            </Col>
          </Row>
        </Col>
        <Col flex={'auto'} style={{marginLeft: 30}}>
          <Row>
            <Col>
              <Space>
                <h3>评测结果:</h3>
                <Button type="text" icon={<DownloadOutlined />} size={'small'} onClick={downloadDebugInfo} />
              </Space>
              <div>
                {translateText(resultData.debuginfo)}
              </div>
              <Space>
                <h3>详细信息:</h3>
                <Button type="text" icon={<DownloadOutlined />} size={'small'} onClick={downloadLog} />
              </Space>
              <div>
                {translateText(resultData.log)}
              </div>
            </Col>
          </Row>
          <Divider></Divider>
          <Row>
            <Col flex={'auto'} style={{width: '40%'}} span={12}>
                <Space>
                  <h3>Input:</h3>
                  <Button type="text" icon={<DownloadOutlined />} size={'small'} onClick={downloadOInput} />
                </Space>
              <Tabs defaultActiveKey='1' items={inputItems} onChange={onInputChooseChange} activeKey={selectInput}/>
            </Col>
            <Col flex={'auto'} style={{marginLeft: 30, width: '40%'}} span={12}>
              <Row align={'middle'}>
                <Space>
                  <h3>Output:</h3>
                  <Button type="text" icon={<DownloadOutlined />} size={'small'} onClick={downloadOutput} />
                  <Button type='primary'>
                    <Link to='/analyze' onClick={onLinkToAnalzeClick}>转入分析</Link>
                  </Button>
                </Space>
              </Row>
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
                {translateText(resultData.out)}
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
