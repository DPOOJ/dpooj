import React from "react";
import { Form, Input, Button, message } from 'antd'
import $ from 'jquery'

function LoginForm( { setLogged, setUserName, setShowLoginForm } ) {

    function submitLoginForm(values) {
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
                if (result.code == "1") {
                    message.error(result.info)
                    return;
                }
                else {
                    message.success('欢迎，' + result.username);
                    setLogged(true);
                    setUserName(values.username);
                    setShowLoginForm(false);
                    return;
                }
            },
            error: function (result) {
                console.log("err",result);
            }
        });
    };
    function submitLoginFormFailed(err) {
        console.log('Failed:', err);
    };

    return (
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
            onFinish={submitLoginForm}
            onFinishFailed={submitLoginFormFailed}
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
    );
}

export default LoginForm;