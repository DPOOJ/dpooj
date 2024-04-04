import React, { useState, useRef } from "react";
import { Button, Input, Table, Tag , Space, Drawer, Row, Col, message, Checkbox, Segmented} from "antd";
import { SearchOutlined, CheckCircleFilled, CloseCircleFilled, WarningFilled, UserSwitchOutlined, FieldTimeOutlined, DoubleRightOutlined} from '@ant-design/icons';
import axios from 'axios'
const { TextArea } = Input;

const colorOfType = {
    'OPEN' : 'green',
    'CLOSE' : 'red',
    'ARRIVE' : 'blue',
    'IN' : '#87d068',
    'OUT' : '#D91215',
    'ERR' : 'black',
    'INPUT' : 'green',
    'OUTPUT' : 'blue',
    'REQUEST' : 'purple',
    'RESET' : 'geekblue',
    'RESET_ACCEPT' : 'magenta',
    'RESET_BEGIN' : 'gold',
    'RESET_END' : 'cyan',
    'RECEIVE' : '#2db7f5',
}

export default function Analyze() {
    const [dataInput, setDataInput] = useState('');
    const [dataOutput, setDataOutput] = useState('');
    const [tableData, setTableData] = useState([])
    const [showDrawer, setShowDrawer] = useState(false);
    const [filterErr, setFilterErr] = useState(true);
    const [tableSize, setTableSize] = useState('middle');
    
    function onCheckBoxChange(e) {
        setFilterErr(e.target.checked)
    }
    function openDrawer() {
        setShowDrawer(true);
    }
    function closeDrawer() {
        axios.post('/statistics?src=analyze')
            .then(res => {

            })
            .catch(err => {

            })
        let input = matchText(dataInput);
        let output = matchText(dataOutput);
        var res = [...input, ...output]
        res.sort((a, b) => {
            return a.timestamp - b.timestamp
        })
        setTableData(res);
        setShowDrawer(false);
    }

    const searchInput = useRef(null);
    const handleSearch = (confirm) => {
      confirm();
    };
    const handleReset = (clearFilters, confirm) => {
      clearFilters();
      confirm();
    };

    const getColumnSearchProps = (dataIndex) => ({
      filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters, close }) => (
        <div
          style={{
            padding: 8,
          }}
          onKeyDown={(e) => e.stopPropagation()}
        >
            <Input
                ref={searchInput}
                placeholder={`Search ${dataIndex}`}
                value={selectedKeys[0]}
                onChange={(e) => setSelectedKeys(e.target.value ? [e.target.value] : [])}
                onPressEnter={() => handleSearch(confirm)}
                style={{
                marginBottom: 8,
                display: 'block',
                }}
            />
            <Space>
                <Button
                    type="primary"
                    onClick={() => handleSearch(confirm)}
                    icon={<SearchOutlined />}
                    size="small"
                    style={{
                        width: 90,
                    }}
                >
                    Search
                </Button>
                <Button
                    onClick={() => {clearFilters && handleReset(clearFilters, confirm);}}
                    size="small"
                    style={{
                        width: 90,
                    }}
                >
                    Reset
                </Button>
                <Button
                    type="link"
                    size="small"
                    onClick={() => {
                        close();
                    }}
                >
                    close
                </Button>
            </Space>
        </div>
      ),

      filterIcon: (filtered) => (
        <SearchOutlined
            style={{
                color: filtered ? '#1677ff' : undefined,
            }}
        />
      ),

      onFilter: (value, record) =>
            record[dataIndex] == value || record[dataIndex] == '',

      onFilterDropdownOpenChange: (visible) => {
            if (visible) {
                setTimeout(() => searchInput.current?.select(), 100);
            }
        },
    });

    const columns = [
        {
            title : 'inout',
            dataIndex: 'inout',
            key: 'inout',
            render: (inout) => <Tag color={colorOfType[inout]}>{inout}</Tag>,
            filters: [
                {
                    text: 'all',
                    value: '',
                },
                {
                    text: 'input only',
                    value: 'OUTPUT',
                },
                {
                    text: 'output only',
                    value: 'INPUT',
                },
            ],
            onFilter: (value, record) => record.inout != value,
            filterMultiple: false,
        },
        {
            title : 'origin',
            dataIndex: 'origin',
            key: 'origin',
        },
        {
            title : 'type',
            dataIndex: 'type',
            key: 'type',
            render: (type) => <Tag color={colorOfType[type]}>{type}</Tag>
        },
        {
            title : 'timestamp',
            dataIndex: 'timestamp',
            key: 'timestamp',
        },
        {
            title : 'floor',
            dataIndex: 'floor',
            key: 'floor',
        },
        {
            title : 'passengerID',
            dataIndex: 'passengerID',
            key: 'passengerID',
            ...getColumnSearchProps('passengerID'),
        },
        {
            title : 'elevatorID',
            dataIndex: 'elevatorID',
            key: 'elevatorID',
            filters: [
                {
                    text: '1',
                    value: '1',
                },
                {
                    text: '2',
                    value: '2',
                },
                {
                    text: '3',
                    value: '3',
                },
                {
                    text: '4',
                    value: '4',
                },
                {
                    text: '5',
                    value: '5',
                },
                {
                    text: '6',
                    value: '6',
                },
            ],
            onFilter: (value, record) => record.elevatorID == value || record.elevatorID == '',
        },
        {
            title: 'elevatorSettings',
            dataIndex: 'elevatorSettings',
            key: 'elevartorSettings',
            render: (value) => <>
                {   value.maxPassenger == '' && value.moveTime == '' ? <div></div> : 
                    <div>
                        <Space>
                            <UserSwitchOutlined />{value.maxPassenger}
                            <FieldTimeOutlined />{value.moveTime}
                        </Space>
                    </div>
                }
            </>
        },
        {
            title : 'passengers',
            dataIndex : 'passengers',
            key : 'passengers',
        },
        // {
        //     title : 'others',
        //     dataIndex: 'others',
        //     key: 'others',
        //     render: (info) => <>
        //         <Space direction="horizontal" size={10} align="end">
        //             {
        //                 info['type'] == 'CORRECT' ? <CheckCircleFilled color="green"/> :
        //                 info['type'] == 'WRONG' ? <CloseCircleFilled color="red"/> : 
        //                 <WarningFilled color="yellow"/>
        //             }
        //             <div>{info['message']}</div>
        //         </Space>
        //     </>
        // },
    ]

    function onTextAreaChangeInput(e) {
        setDataInput(e.target.value);
    }
    function onTextAreaChangeOutput(e) {
        setDataOutput(e.target.value);
    }
    function setToString(s) {
        var text = '';
        s.forEach (function(value) {
            text = text + value + ', ';
        })
        return text.slice(0, text.length - 2);
    }
    function matchText(data) {
        let datalist = data.split('\n')
        let res = [];
        let ele_passengers = {
            '0' : new Set(), '1' : new Set(), '2' : new Set(), '3' : new Set(), '4' : new Set() , '5' : new Set(), '6' : new Set()
        };
        for (var i = 0; i < datalist.length; i++) {
            let t = match(datalist[i]);
            if(t['type'] == 'ERR' && filterErr) {
                continue;
            }
            if (t['origin'] == '') {
                continue;
            }
            let eleId = t['elevatorID'];
            if (!(eleId == '1' || eleId == '2' || eleId == '3' || eleId == '4' || eleId == '5' || eleId == '6')) {
                eleId = '0';
            }
            if (t['type'] == 'IN') {
                let pasId = t['passengerID'];
                ele_passengers[eleId].add(pasId);
            }
            if (t['type'] == 'OUT') {
                let pasId = t['passengerID'];
                ele_passengers[eleId].delete(pasId);
            }
            res.push({
                'key': `${t['type']}-${i+1}`, 
                ...match(datalist[i]), 
                'passengers' : eleId == 0 ? '' : setToString(ele_passengers[eleId]),
                'others' : {
                    'type' : 'CORRECT',
                    'message' : ''
                }
            });
        }
        return(res);
    }
    return (<> 
        <Row justify="space-between" align={'middle'} style={{marginLeft: '20px', marginBottom: '20px', marginRight: '20px'}}>
            <h1>Analyze</h1>
            <Segmented 
                options={['small', 'middle', 'large']}
                onChange={(value) => {
                    setTableSize(value);
                }}
                defaultValue='middle'
            />
            <Button onClick={openDrawer} type="primary">打开输入框</Button>
        </Row>
        <Table columns={columns} dataSource={tableData} pagination={false} size={tableSize}/>
        <Drawer
            title="这是一个输入框>_<"
            placement='right'
            closable={false}
            onClose={closeDrawer}
            open={showDrawer}
            key='output'
            extra={
                <Button onClick={closeDrawer} type="primary" style={{backgroundColor: "green"}}>分析筛选</Button>
            }
            size="large"
        >
            <Col>
                <Checkbox style={{margin: '1%'}} onChange={onCheckBoxChange} defaultChecked={true}>过滤所有格式错误的输入输出</Checkbox>
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

function match(text) {
const inputString = text;

const regexArrive       = /\[ *([\d.]+)\]ARRIVE-(\d+)-(\d+)/;
const regexOpen         = /\[ *([\d.]+)\]OPEN-(\d+)-(\d+)/;
const regexClose        = /\[ *([\d.]+)\]CLOSE-(\d+)-(\d+)/;
const regexIn           = /\[ *([\d.]+)\]IN-(\d+)-(\d+)-(\d+)/;
const regexOut          = /\[ *([\d.]+)\]OUT-(\d+)-(\d+)-(\d+)/;
const regexFrom         = /\[ *([\d.]+)\](\d+)-FROM-(\d+)-TO-(\d+)/;
const regexReset        = /\[ *([\d.]+)\]RESET-Elevator-(\d+)-(\d+)-([\d.]+)/;
const regexResetAccept  = /\[ *([\d.]+)\]RESET_ACCEPT-(\d+)-(\d+)-([\d.]+)/;
const regexResetBgein   = /\[ *([\d.]+)\]RESET_BEGIN-(\d+)/;
const regexResetEnd     = /\[ *([\d.]+)\]RESET_END-(\d+)/;
const regexReceive      = /\[ *([\d.]+)\]RECEIVE-(\d+)-(\d+)/;

let matchArrive = inputString.match(regexArrive);
let matchOpen = inputString.match(regexOpen);
let matchClose = inputString.match(regexClose);
let matchIn = inputString.match(regexIn);
let matchOut = inputString.match(regexOut);
let matchFrom = inputString.match(regexFrom);
let matchReset = inputString.match(regexReset);
let matchResetAccept = inputString.match(regexResetAccept);
let matchResetBegin = inputString.match(regexResetBgein);
let matchResetEnd = inputString.match(regexResetEnd);
let matchReceive = inputString.match(regexReceive);

if (matchArrive) {
    const timestamp = parseFloat(matchArrive[1]);
    const floor = matchArrive[2];
    const elevatorID = matchArrive[3];
    // console.log("ARRIVE:", timestamp, floor, elevatorID);
    return {
        'inout' : 'OUTPUT',
        'type': 'ARRIVE',
        'timestamp': timestamp+0.5,
        'passengerID' : '',
        'floor': floor,
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else if (matchOpen) {
    const timestamp = parseFloat(matchOpen[1]);
    const floor = matchOpen[2];
    const elevatorID = matchOpen[3];
    // console.log("OPEN:", timestamp, floor, elevatorID);
    return {
        'inout' : 'OUTPUT',
        'type': 'OPEN',
        'timestamp': timestamp+0.5,
        'passengerID' : '',
        'floor': floor,
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else if (matchClose) {
    const timestamp = parseFloat(matchClose[1]);
    const floor = matchClose[2];
    const elevatorID = matchClose[3];
    // console.log("CLOSE:", timestamp, floor, elevatorID);
    return {
        'inout' : 'OUTPUT',
        'type': 'CLOSE',
        'timestamp': timestamp+0.5,
        'passengerID' : '',
        'floor': floor,
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else if (matchIn) {
    const timestamp = parseFloat(matchIn[1]);
    const passengerID = matchIn[2];
    const floor = matchIn[3];
    const elevatorID = matchIn[4];
    // console.log("IN:", timestamp, passengerID, floor, elevatorID);
    return {
        'inout' : 'OUTPUT',
        'type': 'IN',
        'timestamp': timestamp+0.5,
        'passengerID' : passengerID,
        'floor': floor,
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else if (matchOut) {
    const timestamp = parseFloat(matchOut[1]);
    const passengerID = matchOut[2];
    const floor = matchOut[3];
    const elevatorID = matchOut[4];
    // console.log("OUT:", timestamp, passengerID, floor, elevatorID);
    return {
        'inout' : 'OUTPUT',
        'type': 'OUT',
        'timestamp': timestamp+0.5,
        'passengerID' : passengerID,
        'floor': floor,
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else if (matchFrom) {
    const timestamp = parseFloat(matchFrom[1]);
    const passengerID = matchFrom[2];
    const beginFloor = matchFrom[3];
    const endFloor = matchFrom[4];
    // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
    return {
        'inout' : 'INPUT',
        'type': 'REQUEST',
        'timestamp': timestamp,
        'passengerID' : passengerID,
        'floor' : `${beginFloor} → ${endFloor}`,
        'elevatorID' : '',
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else if (matchReset) {
    const timestamp = parseFloat(matchReset[1]);
    const elevatorID = matchReset[2];
    const maxPassenger = matchReset[3];
    const moveTime = parseFloat(matchReset[4]);
    // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
    return {
        'inout' : 'INPUT',
        'type': 'RESET',
        'timestamp': timestamp,
        'passengerID' : '',
        'floor' : '',
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': maxPassenger,
            'moveTime': moveTime,
        },
        'origin' : text,
    }
}  else if (matchResetAccept) {
    const timestamp = parseFloat(matchResetAccept[1]);
    const elevatorID = matchResetAccept[2];
    const maxPassenger = matchResetAccept[3];
    const moveTime = parseFloat(matchResetAccept[4]);
    // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
    return {
        'inout' : 'OUTPUT',
        'type': 'RESET_ACCEPT',
        'timestamp': timestamp+0.5,
        'passengerID' : '',
        'floor' : '',
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': maxPassenger,
            'moveTime': moveTime,
        },
        'origin' : text,
    }
} else if (matchResetBegin) {
    const timestamp = parseFloat(matchResetBegin[1]);
    const elevatorID = matchResetBegin[2];
    // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
    return {
        'inout' : 'OUTPUT',
        'type': 'RESET_BEGIN',
        'timestamp': timestamp+0.5,
        'passengerID' : '',
        'floor' : '',
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
}   else if (matchResetEnd) {
    const timestamp = parseFloat(matchResetEnd[1]);
    const elevatorID = matchResetEnd[2];
    // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
    return {
        'inout' : 'OUTPUT',
        'type': 'RESET_END',
        'timestamp': timestamp+0.5,
        'passengerID' : '',
        'floor' : '',
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
}  else if (matchReceive) {
    const timestamp = parseFloat(matchReceive[1]);
    const passengerID = matchReceive[2];
    const elevatorID = matchReceive[3];
    // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
    return {
        'inout' : 'OUTPUT',
        'type': 'RECEIVE',
        'timestamp': timestamp+0.5,
        'passengerID' : passengerID,
        'floor' : '',
        'elevatorID' : elevatorID,
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
} else {
    // console.log("No match found", text);
    return {
        'inout' : 'ERR',
        'type': 'ERR',
        'timestamp': '',
        'passengerID' : '',
        'floor': '',
        'elevatorID' : '',
        'elevatorSettings' : {
            'maxPassenger': '',
            'moveTime': '',
        },
        'origin' : text,
    }
}

}