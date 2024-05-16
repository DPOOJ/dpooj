import React, { useState, useRef, useEffect } from "react";
import { Button, Input, Table, Tag , Space, Drawer, Row, Col, message, Checkbox, Segmented} from "antd";
import { SearchOutlined, CheckCircleFilled, CloseCircleFilled, MinusCircleFilled, UserSwitchOutlined, FieldTimeOutlined, DoubleRightOutlined, LinkOutlined} from '@ant-design/icons';
import axios from 'axios'
const { TextArea } = Input;


export default function Analyze( {input, output} ) {
    const [dataInput, setDataInput] = useState('');
    const [dataOutput, setDataOutput] = useState('');
    const [tableData, setTableData] = useState([])
    const [showDrawer, setShowDrawer] = useState(false);

    useEffect(() => {
        const inp = input.split('\n');
        const outp = output.split('\n');

        let lineNumber = 0;

        const regex = /^ln (\d+)$/;
        const match = inp[0].match(regex);

        var flag = 0;


        if (match) {
            const number = parseInt(match[1]); 
            lineNumber += number + 3;
            flag = 1;
        }

        const mergedArray = [];

        for (let i = lineNumber; i < inp.length; i++) {
            mergedArray.push({
                line: i,
                in: inp[i],
                out: outp[i - lineNumber + flag]
            });
        }

        console.log(mergedArray);
        setTableData(mergedArray);
        setShowDrawer(false);
    }, [input, output])

    function onTextAreaChangeInput(e) {
        setDataInput(e.target.value);
    }
    function onTextAreaChangeOutput(e) {
        setDataOutput(e.target.value);
    }
    function openDrawer() {
        setShowDrawer(true);
    }
    function closeDrawer() {
        const input = dataInput.split('\n')
        const output = dataOutput.split('\n')

        let lineNumber = 0;
        var flag = 0;

        const regex = /^ln (\d+)$/;
        const match = input[0].match(regex);

        if (match) {
            const number = parseInt(match[1]); 
            lineNumber += number + 3;
            flag = 1;
        }

        const mergedArray = [];

        for (let i = lineNumber; i < input.length; i++) {
            mergedArray.push({
                line: i,
                in: input[i],
                out: output[i - lineNumber + flag]
            });
        }

        setTableData(mergedArray);
        setShowDrawer(false);
    }

    const columns = [
        {
            title : 'line',
            dataIndex: 'line',
            key: 'line',
        },
        {
            title : 'in',
            dataIndex: 'in',
            key: 'in',
        },
        {
            title : 'out',
            dataIndex: 'out',
            key: 'out',
        },
    ]

    return (<> 
        <Row justify="space-between" align={'middle'} style={{marginLeft: '20px', marginBottom: '20px', marginRight: '20px'}}>
            <h1>Analyze</h1>
            <Button onClick={openDrawer} type="primary">打开输入框</Button>
        </Row>
        <Table 
            columns={columns} 
            dataSource={tableData} 
            pagination={false} 
        />
        <Drawer
            title="这是一个输入框>_<"
            placement='right'
            closable={false}
            onClose={closeDrawer}
            open={showDrawer}
            key='output'
            extra={
                <Button onClick={closeDrawer} type="primary" style={{backgroundColor: "green"}}>submit</Button>
            }
            size="large"
        >
            <Col>
                <Row>
                    <TextArea 
                        onChange={onTextAreaChangeInput} 
                        autoSize={{minRows: 10}} 
                        placeholder="请在这里输入stdin（如果你愿意也可输在右边）" 
                        style={{width : '48%', margin: '1%'}}
                    />
                    <TextArea 
                        onChange={onTextAreaChangeOutput} 
                        autoSize={{minRows: 10}} 
                        placeholder="请在这里输入stdout（如果你愿意也可以输在左边）" 
                        style={{width : '48%', margin: '1%'}}
                    />
                </Row>
            </Col>
        </Drawer>
    </>)
}