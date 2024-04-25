// Judge.js
import React, { useEffect } from 'react';
import { useState } from 'react';
import { Button, Row, Col, Space, Slider, InputNumber, Divider, Badge, Progress, Tag, Drawer, Table, Dropdown } from 'antd';
import { message } from 'antd';
import { DownOutlined } from '@ant-design/icons';
import $ from 'jquery'
import axios from 'axios';
import FileUploader from './FileUploader';

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
  },
  {
    label: '作业 9',
    key: '9',
  },
];

function Judge({logged}) {
  const [submitAvilable, setSubmitAvilable] = useState(false);
  const [onJudging, setOnJudging] = useState(false);
  const [judgeTimes, setJudgeTimes] = useState(10);
  const [judgeInfo, setJudgeInfo] = useState({
    'AC': 0,
    'WA': 0,
    'TLE': 0,
    'RE' : 0,
    'UKE' : 0,
    'total': 0,
    'all' : 0,
    'running': false,
  })
  const [hwID, setHwID] = useState(9);
  const [downloadInfo, setDownloadInfo] = useState([])
  const [intervalID, setIntervalID] = useState(null)

  useEffect(() => {
    const id = setInterval(() => {
      if(onJudging) {
        getResult()
      }
    }, 2000);
    return () => {
      clearInterval(id);
    }
  }, [onJudging])
  
  useEffect(() => {
    if (!logged) {
      setOnJudging(false);
      setSubmitAvilable(false);
      setJudgeInfo({
        'AC': 0,
        'WA': 0,
        'TLE': 0,
        'RE' : 0,
        'UKE' : 0,
        'total': 0,
        'all' : 0,
      })
      setDownloadInfo([])
    } else {
      setSubmitAvilable(true);
      getResult();
    }
  }, [logged]);

  useEffect(() => {
    if (!logged) {
      setSubmitAvilable(false);
    } else {
      setSubmitAvilable(!onJudging);
    }
  }, [onJudging]);

  function onJudgeTimeSliderChange(value) {
    setJudgeTimes(value);
  }
  function chooseHw( { key } ) {
    setHwID(parseInt(key));
    message.success(`评测调整至作业 ${key}`);
  };

  function startSubmit() {
    if(!logged) {
      message.error('please log in');
      return;
    }
    setOnJudging(true);
    setDownloadInfo([]);
    let postdata = {'args': judgeTimes, 'hwID': hwID};
    $.ajax({
      url: '/uploadArgs',
      type: 'post',
      data: postdata,
      dataType: 'json',
      success: function (result) {
        message.loading('正在启动评测...')
        axios.post('/start')
          .then(res => {
            if(res.data == 0) {
              clearInterval(intervalID);
              setTimeout(() => {
                getResult()
                message.success('评测完成');
              }, 2000)
            }
          })
          .catch(err => {
            message.error('追踪评测状态失败，你的评测可能还未结束')
          });
      },
      error: function (result) {
        setOnJudging(false);
        message.error('上传参数失败，你的评测未能开始')
        console.log("submit request error", result);
      }
    });
  }
  function getResult() {
    if (!logged) {
      return;
    }
    axios.post('/update')
      .then(res => {
        console.log('get result', res);
        if(res.data.code == 1 && res.data.info == "还未开始评测，请稍等") {
          message.warning("没有正在进行的评测")
          return;
        }
        if((res.data.WA != 0 || res.data.TLE != 0 || res.data.RE != 0)) {
          setDownloadInfo([{
            'key': 1,
            'no': 1,
            'result': {
              'WA': res.data.WA != 0,
              'TLE': res.data.TLE != 0,
              'RE': res.data.RE != 0,
            },
            'download': getDownloadFile,
          }])
        }
        setJudgeInfo(res.data);
        if(res.data.running == 1) {
          if(parseInt(res.data.all) >= parseInt(res.data.total)) {
            console.log("stop tracing: all >= total")
            setOnJudging(false);
          } else {
            setOnJudging(true);
          }
          setJudgeTimes(res.data.total);
        } else {
          setOnJudging(false);
        }
      })
      .catch(err => {
        message.error('网络超时')
      });
  }
  const getDownloadFile = () => {
    var data = {}
    $.ajax({
        url: '/download',
        data: data,
        type: 'post',
        success: async function (result) {
            console.log(result)
            let url = result.path;
            console.log('download:', result)
            console.log('url:', url)
            let da = await axios.get(url, {
                responseType: 'blob',
            })
            .then(res => {
              let blob = res.data;
              const $link = document.createElement('a');
              $link.href = URL.createObjectURL(blob);
              $link.download = result.filename;
              $link.click();
              message.success('下载成功')
            })
            .catch(err => {
              message.error('download error')
            });
        },
        error: function (result) {
            console.log("download err", result);
        }
    })
  }

  return (
    <>
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
            <Divider>Settings</Divider>
            <div className='judge-times'>
              <span>评测组数：{judgeTimes}</span>
              <Slider 
                min={0}
                max={20}
                step={5}
                defaultValue={judgeTimes}
                onChange={onJudgeTimeSliderChange}
                value={judgeTimes}
                disabled={!submitAvilable}
              />
              </div>
          </Space>
        </Col>
        <Col flex={'auto'} style={{marginLeft: 30}}>
          <ProgressBar judgeInfo={judgeInfo} onJudging={onJudging} />
          <Divider />
          <ResultTable resData={downloadInfo}/>
        </Col>
      </Row>
    </>
  );
}

const resColor = {
  'AC': 'green',
  'WA': 'red',
  'TLE': 'blue',
  'RE': 'purple',
  'UKE' : 'black',
};

function ProgressBar({judgeInfo, onJudging}) {
  const [curJudgeInfo, setCurJudgeInfo] = useState(judgeInfo);

  useEffect(() => {
    setCurJudgeInfo(judgeInfo);
  }, [judgeInfo])

  return (
    <>
      <h1>{onJudging ? '正在评测：' : '评测结果：'}</h1>
      <Progress
        percent={Math.floor(1.0*(curJudgeInfo.all)/parseInt(curJudgeInfo.total)*100)}
        strokeColor={'#d4380d'}
        success={{
          percent: Math.floor(1.0*(curJudgeInfo.AC)/parseInt(curJudgeInfo.total)*100),
          strokeColor: '#52c41a',
        }}
      />
      <Space style={{marginTop: 20, height: '30px'}}>
        <span style={{fontWeight: 'bold'}}>Accepted</span>
        <Badge count={curJudgeInfo.AC} color="#52c41a" />
        <span style={{fontWeight: 'bold'}}>Wrong Answer</span>
        <Badge count={curJudgeInfo.WA} color="#f5222d" />
        <span style={{fontWeight: 'bold'}}>Time Limit Exceed</span>
        <Badge count={curJudgeInfo.TLE} color="blue" />
        <span style={{fontWeight: 'bold'}}>Runtime Error</span>
        <Badge count={curJudgeInfo.RE} color="purple" />
        <span style={{fontWeight: 'bold'}}>Unknown Error</span>
        <Badge count={curJudgeInfo.UKE} color="black" />
      </Space>
    </>
  );
}

const ResultTable = ({resData}) => {
  const [open, setOpen] = useState(false);

  const showDrawer = () => {
    setOpen(true);
  };
  const onClose = () => {
    setOpen(false);
  };
  const [showData, setShowData] = useState({
    'in' : 'none',
    'ans' : 'none',
    'out' : 'none'
  });

  const columns = [
    {
      title: 'No.',
      dataIndex: 'no',
    },
    {
      title: 'result',
      dataIndex: 'result',
      render: (res) => (
        <Space span={5}>
          {res.WA ? <Tag color={resColor['WA']} key={'WA'}>WA</Tag> : <div />}
          {res.RE ? <Tag color={resColor['RE']} key={'RE'}>RE</Tag> : <div />}
          {res.TLE ? <Tag color={resColor['TLE']} key={'TLE'}>TLE</Tag> : <div />}
        </Space>
      ),
    },
    {
      title: 'Download',
      dataIndex: 'download',
      render: (download) => <Button onClick={download}>下载数据</Button>
    },
    // {
    //   title: 'show',
    //   dataIndex: 'show',
    //   render: (res) => {
    //     const st = () => {
    //       setShowData(res);
    //       showDrawer();
    //     }
    //     return <>
    //       <a onClick={st}>详细信息</a>
    //     </>
    //   }
    // },
  ];
  return (
    <>
      <h1>Wrong Data Points:</h1>
      <Table columns={columns} dataSource={resData} size="middle" />
      <Drawer
        title="详细信息"
        placement={'bottom'}
        closable={false}
        onClose={onClose}
        open={open}
        key={'bottom'}
        size='large'
        extra={
          <Space>
            <Button onClick={onClose} type='primary' style={{backgroundColor: 'red'}}>Close</Button>
          </Space>
        }
      >
        <Divider>Standard In</Divider>
        <p>{showData.in}</p>
        <Divider>Standard Answer</Divider>
        <p>{showData.ans}</p>
        <Divider>Your Answer</Divider>
        <p>{showData.out}</p>
      </Drawer>
    </>
  );
}

export default Judge;
