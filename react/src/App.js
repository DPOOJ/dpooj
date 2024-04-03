// App.js
import React, { useEffect } from 'react';
import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, NavLink, BrowserRouter } from 'react-router-dom';
import { Button, Layout, Menu, Row, Space, message, Drawer } from 'antd';
import Judge from './Judge';
import Run from './Run';
import Notice from './Notice';
import LoginForm from './Login';
import SignUpForm from './SignUp';
import Analyze from './Analyze';
import axios from 'axios';

const { Header, Content, Footer } = Layout;

const links = [
  {
    label: (<NavLink to="/">评测</NavLink>),
    key: 'judge',
  },
  {
    label: (<NavLink to="/analyze">分析</NavLink>),
    key: 'analyze',
  },
  // {
  //   label: (<NavLink to="/run">运行</NavLink>),
  //   key: 'run',
  // },
  {
    label: (<NavLink to="/notice">公告</NavLink>),
    key: 'notice',
  },
]

function App() {
  // user
  const [logged, setLogged] = useState(false);
  const [userName, setUserName] = useState(null);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showSignUpForm, setShowSignUpForm] = useState(false);
  var initDone = false;

  // log in
  function enterLoginForm() { setShowLoginForm(true); }
  function exitLoginForm() { setShowLoginForm(false); }
  // sign up
  function enterSignUpForm() { setShowSignUpForm(true); }
  function exitSignUpForm() { setShowSignUpForm(false); }


  function logout() {
    axios.post('logout')
    .then(res => {
      setLogged(false);
      setUserName(null);
    })
    .catch(err => {
      console.log(err);
    })
  }

  const refreshInit = () => {
    if (initDone) {
      return;
    }
    initDone = true;
    axios.post('/index')
      .then(async (res) => {
        let name = res.data.username
        let code = res.data.code
        if (code == 1) {
          message.warning('请先登录');
        } else {
          message.success(`欢迎，${name}`)
          setUserName(name);
          setLogged(true);
        }
      })
      .catch((err) => {
        message.error('login: network error')
      })
  }
  
  useEffect(() => {
    refreshInit();
  }, [])

  return (
    <>
    <BrowserRouter>
      <div>
        <Layout>
          <Header
            style={{
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <div style={{marginRight: '48px', fontSize: '28px', color: 'white'}}>DPO OJ v2</div>
            <Menu
              theme="dark"
              mode="horizontal"
              defaultSelectedKeys={['judge']}
              items={links}
              style={{
                flex: 1,
                minWidth: 0,
              }}
            />
            { logged ? 
              <Space size={15}>
                <div style={{fontSize: '24px', color: 'white'}}>{userName}</div> 
                <Button type='primary' style={{backgroundColor: 'red'}} onClick={logout}>注销</Button>
              </Space>
              : 
              <Space>
                <Button type='primary'onClick={enterLoginForm}>登录</Button>
                <Button onClick={enterSignUpForm}>注册</Button>
              </Space>
            }
          </Header>
          <Content style={{padding: '30px', backgroundColor: 'white'}}>
            <Routes>
              <Route path='/' element={<Judge logged={logged}/>}/>
              <Route path='/run' element={<Run logged={logged}/>}/>
              <Route path='/analyze' element={<Analyze />}/>
              <Route path='/notice' element={<Notice/>}/>
            </Routes>
          </Content>
        </Layout>
      </div>
      <Drawer
        title="Login"
        placement={'right'}
        closable={false}
        onClose={exitLoginForm}
        open={showLoginForm}
        key={'right'}
        // size='large'
        extra={
          <Space>
            <Button onClick={exitLoginForm} type='primary' style={{backgroundColor: 'red'}}>Close</Button>
          </Space>
        }
      >
        <LoginForm setLogged={setLogged} setUserName={setUserName} setShowLoginForm={setShowLoginForm} />
      </Drawer>
      
      <Drawer
        title="Sign Up"
        placement={'right'}
        closable={false}
        onClose={exitSignUpForm}
        open={showSignUpForm}
        key={'right'}
        // size='large'
        extra={
          <Space>
            <Button onClick={exitSignUpForm} type='primary' style={{backgroundColor: 'red'}}>Close</Button>
          </Space>
        }
      >
        <SignUpForm setLogged={setLogged} setUserName={setUserName} setShowSignUpForm={setShowSignUpForm}/>
      </Drawer>
      </BrowserRouter>
    </>
  );
}



export default App;
