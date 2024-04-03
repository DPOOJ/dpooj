import React from "react";
import { Form, message, Input, Button } from 'antd'
import $ from 'jquery'

export default function SignUpForm( { setLogged, setUserName, setShowSignUpForm } ) {
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
                    return;
                }
                else {
                  message.open({
                    type: 'success',
                    content: '发送成功，请稍后'
                  })
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
                if (result.code == "1") {
                    console.log(result)
                    message.open({
                      type: 'error',
                      content: '验证码错误'
                    })
                    return;
                }
                else {
                  message.open({
                    type: 'success',
                    content: '注册成功，请返回登录'
                  })
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

    return (
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
              注册
            </Button>
          </Form.Item>
        </Form>
    )
}