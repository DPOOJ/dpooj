import React, { useState, useEffect, useRef } from 'react';
import { Button, Row, Col, Space } from 'antd';
import { Divider } from 'antd';
import { InputNumber, Slider } from 'antd';
import { InboxOutlined } from '@ant-design/icons';
import { message, Upload } from 'antd';
import { Table, Tag } from 'antd';
import { Progress } from 'antd';
import { Badge } from 'antd';
import { Drawer  } from 'antd';
import { Form, Input, Modal } from 'antd'
import { DownOutlined } from '@ant-design/icons';
import { Dropdown, Typography } from 'antd';
import axios from 'axios';
import $ from 'jquery'

const { Dragger } = Upload;

const fileProps = {
  name: 'file',
  action: '/uploadFile',
  headers: {
    authorization: 'authorization-text',
  },
  onChange(info) {
    // console.log(info)
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
};


const IntegerStep = ({inputValue, onChange}) => {
  return (
    <>
      <Divider>args</Divider>
      <Col>
        <InputNumber
          min={1}
          max={20}
          style={{
            margin: '0 16px',
          }}
          value={inputValue}
          onChange={onChange}
        />
        <Slider
          min={1}
          max={20}
          onChange={onChange}
          value={typeof inputValue === 'number' ? inputValue : 0}
        />
      </Col>
    </>
  );
};

const ProgressBar = ({judgingInfo}) => {
  return (
    <>
      <h1>{judgingInfo.judging ? '正在评测：' : '等待评测：'}</h1>
      <Progress
        percent={Math.floor(1.0*(judgingInfo.all)/parseInt(judgingInfo.total)*100)}
        strokeColor={'#d4380d'}
        success={{
          percent: Math.floor(1.0*(judgingInfo.AC)/parseInt(judgingInfo.total)*100),
          strokeColor: '#52c41a',
        }}
      />
      {/* <h1>{judgingInfo.AC} tot:{judgingInfo.total}</h1> */}
      <Space style={{marginTop: 20, height: '30px'}}>
        <span style={{fontWeight: 'bold'}}>Accepted</span>
        <Badge count={judgingInfo.AC} color="#52c41a" />
        <span style={{fontWeight: 'bold'}}>Wrong Answer</span>
        <Badge count={judgingInfo.WA} color="#f5222d" />
        <span style={{fontWeight: 'bold'}}>Time Limit Exceed</span>
        <Badge count={judgingInfo.TLE} color="blue" />
        <span style={{fontWeight: 'bold'}}>Runtime Error</span>
        <Badge count={judgingInfo.RE} color="purple" />
        <span style={{fontWeight: 'bold'}}>Unknown Error</span>
        <Badge count={judgingInfo.UKE} color="black" />
      </Space>
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
        <>
        <Space span={5}>
          <Tag color={resColor['WA']} key={'WA'}>
            {/* {res.toUpperCase()} */}
            WA
          </Tag>
          <span>or&nbsp;&nbsp;</span>
          <Tag color={resColor['RE']} key={'RE'}>
            {/* {res.toUpperCase()} */}
            RE
          </Tag>
        </Space>
        </>
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

// var userID = null


const mimeMap = {
  xlsx: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  zip: 'application/zip'
}
 
export function downLoadZip(str, filename) {
  var url = str
  axios({
    method: 'post',
    url: url,
    responseType: 'blob',
    headers:{ 'Content-Type': 'application/json; application/octet-stream'}
  }).then(res => {
    resolveBlob(res, mimeMap.zip)
  })
  .catch(err => {
    message.error('download: network error')
  })
}
/**
 * 解析blob响应内容并下载
 * @param {*} res blob响应内容
 * @param {String} mimeType MIME类型
 */
export function resolveBlob(res, mimeType) {
    console.log(res)
    const blob = new Blob([res.data]);
    const downloadElement = document.createElement("a");
    const href = window.URL.createObjectURL(blob);
    var patt = new RegExp('filename=([^;]+\\.[^\\.;]+);*')
    var contentDisposition = decodeURI(res.headers['content-disposition'])
    var result = patt.exec(contentDisposition)
    var fileName = result[1]
    fileName = fileName.replace(/\"/g, '')
    //后台再header中传文件名
    const name = fileName;
    downloadElement.href = href;
    downloadElement.download = name;
    document.body.appendChild(downloadElement);
    downloadElement.click();
    document.body.removeChild(downloadElement); // 下载完成移除元素
    window.URL.revokeObjectURL(href); // 释放掉blob对象
}

var intervalID;



const App = () => {
  // status
  const [loadings, setLoadings] = useState(false);
  // login
  const [userID, setUserID] = useState(null)

  //slider
  const [inputValue, setInputValue] = useState(10);
  const onChange = (newValue) => {
    setInputValue(newValue);
  };
  // download
  
  const [downloadInfo, setDownloadInfo] = useState([])
  // const getDownload = () => {
  //   axios.get('/download')
  //     .then(res => {
  //       setDownloadInfo(res.data);
  //     })
  //     .catch(err => {
  //     });
  // }
  const getDownloadFile = () => {
    var data = {}
    // $("#downloadCallback")[0].innerHTML = "";
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
  //results
  const [judgingInfo, setJudingInfo] = useState({
    'AC': 0,
    'WA': 0,
    'TLE': 0,
    'RE' : 0,
    'UKE' : 0,
    'total': 0,
    'all':0,
    'judging': false
  });
  

  const getResult = (id=null) => {
    if (userID == null) {
      if(id==null) return;
    }
    // console.log('--', userID)
    axios.post('/update')
      .then(res => {
        if((res.data.WA != 0 || res.data.TLE != 0 || res.data.RE != 0)) {
          setDownloadInfo([{
            'no': 1,
            'result': {
              'WA': res.data.WA != 0,
              'TLE': res.data.TLE != 0,
              'RE': res.data.RE != 0,
            },
            'download': getDownloadFile,
          }])
        }
        // console.log(res.data);
        setJudingInfo(res.data);
        if(res.data.all == res.data.total) {
          console.log('end', res.data)
          setLoadings(false);
          clearInterval(intervalID);
        }
      })
      .catch(err => {
        message.open({
          type: 'error',
          content: 'network error'
        })
        clearInterval(intervalID);
      });
  }
  // const getUser = () => {
  //   axios.get('/user')
  //     .then(res => {
  //       setUserID(res.data)
  //       if(res.data != null) {
  //         setShowLogin(false);
  //       }
  //     })
  //     .catch(err => {
  //       console.log('fail to get userid')
  //     })
  // }
  //submit

  const enterLoading = () => {
    if(userID == null) {
      message.open({
        type: 'error',
        content: 'please log in'
      })
      return;
    }
    setLoadings(true);
    setDownloadInfo([])
    intervalID = setInterval(() => {
      // getUser();
      getResult();
    }, 2000);
    var postdata = {'args': inputValue, 'hwID' : hwID}
    $.ajax({
      url: '/uploadArgs',
      type: 'post',
      data: postdata,
      dataType: 'json',
      success: function (result) {
        message.loading('waiting...')
        axios.post('/start')
          .then(res => {
            console.log('submit: start', res)
            if(res.data == 0) {
              clearInterval(intervalID);
              console.log('submit: start: end', res);
              setTimeout(getResult, 2000);
              setTimeout(() => {
                setLoadings(false);
              }, 2000)
              // setTimeout(getResult, 4000);
            }
          })
          .catch(err => {
            message.error('submit: network error')
          });
          //console.log("suc");
          // if (result.code == "1") {
          //     console.log(result)
          //     // message.open({
          //     //   type: 'error',
          //     //   content: '用户名或密码错误'
          //     // })
          //     // $("#callbackText")[0].className = "red-text";
          //     // $("#callbackText")[0].innerHTML = result.info;
          //     return;
          // }
          // else {
          //   // message.open({
          //   //   type: 'success',
          //   //   content: '欢迎' + result.username
          //   // })
          //     // $("#callbackText")[0].className = "green-text";
          //     // $("#callbackText")[0].innerHTML = "登录成功！";
          // }
      },
      error: function (result) {
        setLoadings(false);
        message.error('upload error')
        console.log("err",result);
      }
    });
//     axios.post('/uploadArgs', {params: {'args': inputValue}})
//       .then(res => {
//         message.open({
//           type: 'loading',
//           content: 'uploading...',
//           duration: 2,
//         })
//       })
//       .catch(err => {
//         setLoadings(false);
//         message.open({
//           type: 'error',
//           content: 'submit error: network error',
//           duration: 2
// ,        })
//       })
  };

  // login
  const [showLogin, setShowLogin] = useState(false);
  const enterLogin = () => {
    setShowLogin(true);
  }
  const exitLogin = () => {
    setShowLogin(false);
  }
  // sign up
  const [showSignUp, setShowSignUp] = useState(false);
  const enterSignUp = () => {
    setShowSignUp(true);
  }
  const exitSignUp = () => {
    setShowSignUp(false);
  }
  const onFinish = (values) => {
    var postdata = {
      data: JSON.stringify({
          'username': values.username,
          'password': values.password,
      }),
    }
    $.ajax({
      url: '/handlelogin',
      type: 'post',
      data: postdata,
      dataType: 'json',
      success: function (result) {
          //console.log("suc");
          if (result.code == "1") {
              console.log(result)
              message.open({
                type: 'error',
                content: '用户名或密码错误'
              })
              // $("#callbackText")[0].className = "red-text";
              // $("#callbackText")[0].innerHTML = result.info;
              return;
          }
          else {
            message.open({
              type: 'success',
              content: '欢迎' + result.username
            })
            setUserID(userID=>{
              getResult(result.username)
              return result.username}
              )
            setShowLogin(false)
              // $("#callbackText")[0].className = "green-text";
              // $("#callbackText")[0].innerHTML = "登录成功！";
          }
      },
      error: function (result) {
          console.log("err",result);
      }
    });
  };
  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  //sign up
  const onFinishSign = (values) => {
    var postdata = {
          'username': values.username,
          'email': values.email,
          'password': values.password,
          'agpassword': values.password2,
          'code': values.valid,
    }
    console.log(values.valid, typeof(values.valid))
    if(typeof(values.valid) == 'undefined') {
      $.ajax({
        url: '/send_code',
        type: 'post',
        data: postdata,
        dataType: 'json',
        success: function (result) {
            console.log(result);
            if (result.code == "1") {
                message.open({
                  type: 'error',
                  content: '验证码已发送，请查收邮箱'
                })
                // $("#callbackText")[0].className = "red-text";
                // $("#callbackText")[0].innerHTML = result.info;
                return;
            }
            else {
              message.open({
                type: 'success',
                content: '发送成功，请稍后'
              })
              // setUserID(result.username)
              // setShowLogin(false)
                // $("#callbackText")[0].className = "green-text";
                // $("#callbackText")[0].innerHTML = "登录成功！";
            }
        },
        error: function (result) {
            console.log("err",result);
        }
      });
    }
    else {
      $.ajax({
        url: '/validate_code',
        type: 'post',
        data: postdata,
        dataType: 'json',
        success: function (result) {
            //console.log("suc");
            if (result.code == "1") {
                console.log(result)
                message.open({
                  type: 'error',
                  content: '验证码错误'
                })
                // $("#callbackText")[0].className = "red-text";
                // $("#callbackText")[0].innerHTML = result.info;
                return;
            }
            else {
              message.open({
                type: 'success',
                content: '注册成功，请返回登录'
              })
              // setUserID(result.username)
              // setShowLogin(false)
                // $("#callbackText")[0].className = "green-text";
                // $("#callbackText")[0].innerHTML = "登录成功！";
            }
        },
        error: function (result) {
            console.log("err",result);
        }
      });

    }
  };
  const onFinishFailedSign = (errorInfo) => {
    console.log('Failed:', errorInfo);
  };

  // init
  const refreshInit = () => {
    axios.post('/index')
      .then(async (res) => {
        let id = res.data.username
        let code = res.data.code
        if (code == 1) {
          message.warning('请先登录');
        } else {
          message.open({
            type: 'success',
            content: '欢迎' + id
          })
          setUserID(userID=>{
            getResult(id)
            return id;    
          });
          
        }
      })
      .catch((err) => {
        message.error('login: network error')
      })
  }

  
  const Init = function(){
    refreshInit()
  }

  useEffect(() => {
    Init()
  }, []);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const showModal = () => {
    setIsModalOpen(true);
  };
  const handleOk = () => {
    setIsModalOpen(false);
  };
  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const logout = () => {
    axios.post('logout')
      .then(res => {
        window.location.reload();
      })
      .catch(err => {
        
      })
  }

  const [hwID, setHwID] = useState(6);

  // choose homework
  const items = [
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
  ];
  
  const chooseHw = ({ key }) => {
    setHwID(parseInt(key));
    message.success(`评测调整至作业 ${key}`);
  };




  return (
    <>
      <Row justify="space-around" align="middle" style={{
        paddingTop: 15,
        paddingBottom: 15,
        paddingLeft: 30,
        paddingRight: 30,
        height: '80px',
        backgroundColor: '#020D24'
      }}>
        <Col flex='230px'>
            <span style={{
              color: 'white',
              fontSize: 40
            }}>
              DPO OJ v2
            </span>
        </Col>
        <Col flex={'auto'}>
            <Button onClick={showModal}>
            公告
            </Button>
            <Modal title="欢迎来到面向数据点在线评测系统" open={isModalOpen} onOk={handleOk} >
              <p style={{color: 'gray'}}>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;你说得对，但是《DPO在线评测系统》是由
                  <span style={{color: 'black'}}>q</span><span style={{color: 'red'}}>uanshr</span>和
                  <span style={{color: 'darkgreen'}}>cxccxc</span>
                  自主研发的一款全新在线评测系统。评测发生在一个被称作「JVM」的幻想世界，在这里被OO选中的同学可以体验到
                  「自动化评测」，引导「面向数据点编程」之力。你将扮演一位名为「内测用户」的神秘角色，在自由的在线评测系统中邂逅性格各异、
                  能力独特的数据点，和他们一起击败「程序bug」，通过「最终强测」的同时，逐步发掘「6系课设」的真相。
              </p>
              <p>
                OJ前端由不愿意透露姓名的前端新手<span style={{color: 'blue'}}>@alkaid</span>同学完成，如有不好用的地方敬请谅解&#62;_&#60;;
              </p>
              <p>免责声明：此OJ目前不进行性能测试，并且通过测试也不代表一定能通过强测</p>
              <p>请确保jar包使用jdk1.8构建</p>
              <p>注：Unknown Error几乎只因为服务器丢失数据点产生，请不必在意</p>
            </Modal>
        </Col>
        <Col flex='300px' align='right'>
          {
            userID == null ? <>
              <Space size={15}>
                <Button type='primary' onClick={enterLogin}>登录</Button>
                <Button onClick={enterSignUp}>注册</Button>
              </Space>
            </> : <>
              <Space size={15}>
                  <h3 style={{color:'white'}}>{userID}</h3>
                  <Button type='primary' style={{backgroundColor: 'red'}} onClick={logout}>登出</Button>
              </Space>
            </>
          }
        </Col>
      </Row>
      <Row>
        <Col flex={'250px'} align={'center'} style={{
          margin: 30,
          padding: 10,
          paddingBottom: 30,
          border: '1px dashed',
          borderRadius: '10px',
          maxHeight: '515px'
          }}>
          <Space direction='vertical' size={15}>
            {/* <h2>进度：hw2</h2> */}
            <Dropdown
              menu={{
                items,
                onClick:chooseHw,
              }}
            >
              <a onClick={(e) => e.preventDefault()}>
                <Space>
                  <h2>进度：作业{hwID}</h2>
                  <DownOutlined />
                </Space>
              </a>
            </Dropdown>
            {/* <Upload {...fileProps} maxCount={1}>
              <Tooltip title='请使用jdk1.8打包，否则会RE' placement='bottom'>
                <Button icon={<UploadOutlined />}>点击上传.jar文件</Button>
              </Tooltip>
            </Upload> */}
            <Dragger {...fileProps} maxCount={1} disabled={userID==null || loadings==true}>
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">点击或拖拽上传.jar文件</p>
              <p className="ant-upload-hint">
                请确保文件使用jdk1.8打包
              </p>
          </Dragger>
            <IntegerStep inputValue={inputValue} onChange={onChange}/>
            <Button
              type="primary"
              loading={loadings}
              onClick={enterLoading}
              style={{backgroundColor: 'green'}}
            >
              Submit
            </Button>
          </Space>
        </Col>
        <Col flex={'auto'} style={{margin: 20}}>
          <ProgressBar judgingInfo={judgingInfo}></ProgressBar>
          <Divider></Divider>
          <ResultTable resData={downloadInfo}></ResultTable>
          {/* <Space style={{marginTop: 15, float: 'right'}}>
            <Badge count={0} color={connect ? "#52c41a" : "red"} />
            <span style={{fontSize:'20px', fontWeight: 'bold'}}>{connect ? '服务器连接正常' : '服务器连接断开'}</span>
          </Space> */}
        </Col>
      </Row>
      <Drawer
        title="Login"
        placement={'right'}
        closable={false}
        onClose={exitLogin}
        open={showLogin}
        key={'right'}
        // size='large'
        extra={
          <Space>
            <Button onClick={exitLogin} type='primary' style={{backgroundColor: 'red'}}>Close</Button>
          </Space>
        }
      >
        <Form
          name="login"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          style={{
            maxWidth: 600,
          }}
          initialValues={{
            remember: true,
          }}
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          autoComplete="off"
        >
          <Form.Item
            label="用户名"
            name="username"
            rules={[
              {
                required: true,
                message: '请输入用户名!',
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="密码"
            name="password"
            rules={[
              {
                required: true,
                message: '请输入密码!',
              },
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            <Button type="primary" htmlType="submit">
              登录
            </Button>
          </Form.Item>
        </Form>
      </Drawer>
      <Drawer
        title="Sign Up"
        placement={'right'}
        closable={false}
        onClose={exitSignUp}
        open={showSignUp}
        key={'right'}
        // size='large'
        extra={
          <Space>
            <Button onClick={exitSignUp} type='primary' style={{backgroundColor: 'red'}}>Close</Button>
          </Space>
        }
      >
        
        <Form
          name="signup"
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          style={{
            maxWidth: 600,
          }}
          initialValues={{
            remember: true,
          }}
          onFinish={onFinishSign}
          onFinishFailed={onFinishFailedSign}
          autoComplete="off"
        >
          <Form.Item
            label="用户名"
            name="username"
            rules={[
              {
                required: true,
                message: '请输入用户名!',
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            label="密码"
            name="password"
            rules={[
              {
                required: true,
                message: '请输入密码!',
              },
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            label="再次输入密码"
            name="password2"
            rules={[
              ({getFieldValue}) => ({
                validator(rule, value){
                  if(!value || getFieldValue('password') === value){
                    return Promise.resolve()
                  }
                  return Promise.reject("密码不一致")
                }
              })
            ]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item
            label="邮件地址"
            name="email"
            rules={[
              {
                required: true,
                message: '请输入邮箱!',
              },
            ]}
          >
            <Input />
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            
            <Button htmlType='submit'>
              发送验证码
            </Button>
          </Form.Item>


          <Form.Item
            label="验证码"
            name="valid"
          >
            <Input />
          </Form.Item>

          <Form.Item
            wrapperCol={{
              offset: 8,
              span: 16,
            }}
          >
            
            <Button type="primary" htmlType="submit">
              注册并登录
            </Button>
          </Form.Item>
        </Form>
      </Drawer>
    </>
  );
};
export default App;