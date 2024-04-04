import React from "react";
import { Card, Row, Col } from "antd";

export default function Notice() {
    return (
        <>
            <Row gutter={16}>
                <Col span={12}>
                    <Card
                        title="欢迎来到面向数据点在线评测系统"
                        style={{marginBottom: 20, color: 'gray'}}
                        headStyle={{backgroundColor: '#E8E8E8'}}
                        bodyStyle={{backgroundColor: '#F7F7F7'}}
                    >
                        <p style={{color: 'gray'}}>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;你说得对，但是《DPO在线评测系统》是由
                        <span style={{color: 'black'}}>q</span><span style={{color: 'red'}}>uanshr</span>
                        和<span style={{color: 'darkgreen'}}>cxccxc</span>
                        自主研发的一款全新在线评测系统。评测发生在一个被称作「JVM」的幻想世界，在这里被OO选中的同学可以体验到
                        「自动化评测」，引导「面向数据点编程」之力。你将扮演一位名为「内测用户」的神秘角色，在自由的在线评测系统中邂逅性格各异、
                        能力独特的数据点，和他们一起击败「程序bug」，通过「最终强测」的同时，逐步发掘「6系课设」的真相。
                        </p>
                        <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;OJ前端由不愿意透露姓名的前端新手<span style={{color: 'blue'}}>@alkaid</span>同学完成，如有不好用的地方敬请谅解&#62;_&#60;;</p>
                        
                    </Card>
                    <Card
                        title="分析功能使用须知"
                        style={{marginBottom: 20}}
                        headStyle={{backgroundColor: '#E8E8E8'}}
                        bodyStyle={{backgroundColor: '#F7F7F7'}}
                    >
                        <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;点击"打开输入框"按钮，之后在文本框内输入要分析的结果，之后点击“分析筛选”关闭。表格会显示输出，点击"passengerID"或"elevatorID"边的按钮即可筛选指定数据</p>
                        <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;PS：目前只有简单的筛选功能</p>
                    </Card>
                </Col>
                <Col span={12}>
                    <Card
                        title="免责声明"
                        style={{marginBottom: 20}}
                        headStyle={{backgroundColor: '#E8E8E8'}}
                        bodyStyle={{backgroundColor: '#F7F7F7'}}
                    >
                        <p>此OJ目前不进行性能测试</p>
                        <p>通过测试也不代表一定能通过强测</p>
                    </Card>
                    <Card
                        title="使用须知"
                        style={{marginBottom: 20}}
                        headStyle={{backgroundColor: '#E8E8E8'}}
                        bodyStyle={{backgroundColor: '#F7F7F7'}}
                    >
                        <p>请确保jar包使用jdk1.8构建</p>
                        <p>Unknown Error几乎只因为服务器丢失数据点产生，请不必在意</p>
                    </Card>
                    <Card
                        title="自测功能实用须知"
                        style={{marginBottom: 20}}
                        headStyle={{backgroundColor: '#E8E8E8'}}
                        bodyStyle={{backgroundColor: '#F7F7F7'}}
                    >
                        <p>请确保jar包使用jdk1.8构建</p>
                        <p>请确保输入的合法性，要有时间戳，比如{'[1.000]1-FROM-2-TO-3'}</p>
                        <p>中途退出页面可能导致评测结果无法追踪，当然等120s以后再回来肯定能看到...</p>
                    </Card>
                </Col>
            </Row>
        </>
    )
}