import React, { useState, useRef, useEffect } from "react";
import { Button, Input, Table, Tag , Space, Drawer, Row, Col, message, Checkbox, Segmented} from "antd";
import { SearchOutlined, CheckCircleFilled, CloseCircleFilled, MinusCircleFilled, UserSwitchOutlined, FieldTimeOutlined, DoubleRightOutlined, LinkOutlined} from '@ant-design/icons';
import axios from 'axios'
const { TextArea } = Input;

const colorOfType = {
    'OPEN' : 'green',
    'CLOSE' : 'red',
    'ARRIVE' : 'blue',
    'IN' : '#87d068',
    'OUT' : '#D91215',
    'RESET' : 'geekblue',
    'RESET(DC)' : 'geekblue',
    'RESET_BEGIN' : 'gold',
    'RESET_END' : 'cyan',
    'RECEIVE' : '#2db7f5',
    
    'REQUEST' : 'purple',
    'RESET_ACCEPT' : 'magenta',
    'RESET_ACCEPT(DC)' : 'magenta',

    'INPUT' : 'green',
    'OUTPUT' : 'blue',

    'ERR' : 'black',
}

var timeOff = 0.05;

export default function Analyze( {input, output} ) {
    const [dataInput, setDataInput] = useState('');
    const [dataOutput, setDataOutput] = useState('');
    const [tableData, setTableData] = useState([])
    const [showDrawer, setShowDrawer] = useState(false);
    const [filterErr, setFilterErr] = useState(true);
    const [tableSize, setTableSize] = useState('middle');
    const [timestampOffset, setTimestampOffset] = useState(0.05);
    var filterErrorType = true;
    useEffect(() => {
        filterErrorType = filterErr
    }, [filterErr])
    
    function onCheckBoxChange(e) {
        setFilterErr(e.target.checked)
    }
    function openDrawer() {
        setShowDrawer(true);
    }
    function closeDrawer() {
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

    useEffect(() => {
        setDataInput(input);
        setDataOutput(output);
        let _input = matchText(input);
        let _output = matchText(output);
        var res = [..._input, ..._output]
        res.sort((a, b) => {
            return a.timestamp - b.timestamp
        })
        setTableData(res);
    }, [input, output])

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
            width: '80px',
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
            width: '120px',
            render: (type) => <Tag color={colorOfType[type]}>{type}</Tag>
        },
        {
            title : 'timestamp',
            dataIndex: 'timestamp',
            key: 'timestamp',
            width: '100px',
        },
        {
            title : 'floor',
            dataIndex: 'floor',
            key: 'floor',
            width: '100px',
        },
        {
            title : 'passengerID',
            dataIndex: 'passengerID',
            key: 'passengerID',
            width: '110px',
            ...getColumnSearchProps('passengerID'),
        },
        {
            title : 'elevatorID',
            dataIndex: 'elevatorID',
            key: 'elevatorID',
            width: '100px',
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
                {
                    text: '1-A',
                    value: '1-A',
                },
                {
                    text: '1-B',
                    value: '1-B',
                },
                {
                    text: '2-A',
                    value: '2-A',
                },
                {
                    text: '2-B',
                    value: '2-B',
                },
                {
                    text: '3-A',
                    value: '3-A',
                },
                {
                    text: '3-B',
                    value: '3-B',
                },
                {
                    text: '4-A',
                    value: '4-A',
                },
                {
                    text: '4-B',
                    value: '4-B',
                },
                {
                    text: '5-A',
                    value: '5-A',
                },
                {
                    text: '5-B',
                    value: '5-B',
                },
                {
                    text: '6-A',
                    value: '6-A',
                },
                {
                    text: '6-B',
                    value: '6-B',
                },
            ],
            onFilter: (value, record) => record.elevatorID == value || record.elevatorID == '',
        },
        {
            title: 'elevatorSettings',
            dataIndex: 'elevatorSettings',
            key: 'elevartorSettings',
            width: '130px',
            render: (value) => <>
                {   value.capacity == '' && value.speed == '' ? <div></div> : 
                    <div>
                        <Space>
                            <UserSwitchOutlined />{value.capacity}
                            <FieldTimeOutlined />{value.speed}
                            {
                                value.translateFloor == '' ? '' : 
                                <Space>
                                    <LinkOutlined />{value['translateFloor']}
                                </Space>
                            }
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
        {
            title : 'received',
            dataIndex : 'received',
            key : 'received',
        },
        // {
        //     title : 'others',
        //     dataIndex: 'others',
        //     key: 'others',
        //     render: (info) => <>
        //         <Space direction="horizontal" size={10} align="end">
        //             {
        //                 info['type'] == 'CORRECT' ? <CheckCircleFilled style={{color: "green"}}/> :
        //                 info['type'] == 'WRONG' ? <CloseCircleFilled style={{color: "red"}}/> : 
        //                 <MinusCircleFilled style={{color: "gray"}}/>
        //             }
        //             <div>{info['message']}</div>
        //         </Space>
        //     </>
        // },
        // {
        //     title : 'others',
        //     dataIndex: 'others',
        //     key: 'others',
        //     render: (info) => <>
        //         <Space direction="horizontal" size={10} align="end">
        //             {
        //                 info['type'] == 'CORRECT' ? <CheckCircleFilled style={{color: "green"}}/> :
        //                 info['type'] == 'WRONG' ? <CloseCircleFilled style={{color: "red"}}/> : 
        //                 <MinusCircleFilled style={{color: "gray"}}/>
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
    function onTimestampOffsetChange(e) {
        timeOff = parseFloat(e.target.value)
        setTimestampOffset(e.target.value);
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
            '0' : new Set(), '1' : new Set(), '2' : new Set(), '3' : new Set(), '4' : new Set() , '5' : new Set(), '6' : new Set(),
            '0' : new Set(), '1-A' : new Set(), '2-A' : new Set(), '3-A' : new Set(), '4-A' : new Set() , '5-A' : new Set(), '6-A' : new Set(),
            '0' : new Set(), '1-B' : new Set(), '2-B' : new Set(), '3-B' : new Set(), '4-B' : new Set() , '5-B' : new Set(), '6-B' : new Set(),
        };
        let ele_received = {
            '0' : new Set(), '1' : new Set(), '2' : new Set(), '3' : new Set(), '4' : new Set() , '5' : new Set(), '6' : new Set(),
            '0' : new Set(), '1-A' : new Set(), '2-A' : new Set(), '3-A' : new Set(), '4-A' : new Set() , '5-A' : new Set(), '6-A' : new Set(),
            '0' : new Set(), '1-B' : new Set(), '2-B' : new Set(), '3-B' : new Set(), '4-B' : new Set() , '5-B' : new Set(), '6-B' : new Set(),
            '0' : new Set(), '1' : new Set(), '2' : new Set(), '3' : new Set(), '4' : new Set() , '5' : new Set(), '6' : new Set(),
            '0' : new Set(), '1-A' : new Set(), '2-A' : new Set(), '3-A' : new Set(), '4-A' : new Set() , '5-A' : new Set(), '6-A' : new Set(),
            '0' : new Set(), '1-B' : new Set(), '2-B' : new Set(), '3-B' : new Set(), '4-B' : new Set() , '5-B' : new Set(), '6-B' : new Set(),
        };
        // let ele_opening = [false, false, false, false, false, false, false];
        // let ele_setting = {
        //     '0':{'speed': 400, 'capacity': 6}, '1':{'speed': 400, 'capacity': 6}, '2':{'speed': 400, 'capacity': 6}, '3':{'speed': 400, 'capacity': 6}, 
        //     '4':{'speed': 400, 'capacity': 6}, '5':{'speed': 400, 'capacity': 6}, '6':{'speed': 400, 'capacity': 6}, 
        // }
        // let ele_resetting = [false, false, false, false, false, false, false];
        // let ele_floor = [1,1,1,1,1,1,1];
        // let wait_passengers = new Set();
        // let pas_received = new Set();
        // let ele_opening = [false, false, false, false, false, false, false];
        // let ele_setting = {
        //     '0':{'speed': 400, 'capacity': 6}, '1':{'speed': 400, 'capacity': 6}, '2':{'speed': 400, 'capacity': 6}, '3':{'speed': 400, 'capacity': 6}, 
        //     '4':{'speed': 400, 'capacity': 6}, '5':{'speed': 400, 'capacity': 6}, '6':{'speed': 400, 'capacity': 6}, 
        // }
        // let ele_resetting = [false, false, false, false, false, false, false];
        // let ele_floor = [1,1,1,1,1,1,1];
        // let wait_passengers = new Set();
        // let pas_received = new Set();
        for (var i = 0; i < datalist.length; i++) {
            let t = match(datalist[i]);
            var others = {'type' : 'CORRECT','message' : ''}
            if(t['type'] == 'ERR' && filterErrorType) {
                continue;
            }
            if (t['origin'] == '') {
                continue;
            }
            let eleId = t['elevatorID'];
            if (!(eleId[0] == '1' || eleId[0] == '2' || eleId[0] == '3' || eleId[0] == '4' || eleId[0] == '5' || eleId[0] == '6')) {
            if (!(eleId[0] == '1' || eleId[0] == '2' || eleId[0] == '3' || eleId[0] == '4' || eleId[0] == '5' || eleId[0] == '6')) {
                eleId = '0';
                // others={'type':'WRONG','message':'电梯编号错误'}
                // others={'type':'WRONG','message':'电梯编号错误'}
            }
            // if (t['type'] == 'OPEN') {
            //     if (ele_opening[eleId] == true) {
            //         others = {'type':'WRONG', 'message':'门已开'}
            //     } else if (ele_resetting[eleId] == true) {
            //         others = {'type':'WRONG', 'message':'重置中开门'}
            //     } else if (ele_floor[eleId] != t['floor']) {
            //         others = {'type':'WRONG', 'message':`开门楼层错误 当前:${ele_floor[eleId]}`}
            //     } else {
            //         ele_opening[eleId] = true;
            //     }
            // }
            // else if (t['type'] == 'CLOSE') {
            //     if (ele_opening[eleId] == false) {
            //         others = {'type':'WRONG', 'message':'门已关'}
            //     } else if (ele_resetting == true) {
            //         others = {'type':'WRONG', 'message':'重置中关门'}
            //     } else if (ele_floor[eleId] != t['floor']) {
            //         others = {'type':'WRONG', 'message':`关门楼层错误 当前:${ele_floor[eleId]}`}
            //     } else {
            //         ele_opening[eleId] = false;
            //     }
            // }
            // else if (t['type'] == 'ARRIVE') {
            //     if (ele_received[eleId].size === 0) {
            //         others = {'type': 'WRONG', 'message':'没有RECEIVE'}
            //     } else if (Math.abs(ele_floor[eleId] - t['floor']) != 1) {
            //         others = {'type': 'WRONG', 'message':`移动层数不为1: ${ele_floor[eleId]}-${t['floor']}`}
            //     } else if (t['floor'] > 11 || t['floor'] < 1) {
            //         others = {'type': 'WRONG', 'message':'楼层非法'}
            //     } else if (ele_resetting[eleId] == true) {
            //         others = {'type': 'WRONG', 'message':'重置中移动'}
            //     } else {
            //         ele_floor[eleId] = t['floor'];
            //     }
            // }
            // if (t['type'] == 'OPEN') {
            //     if (ele_opening[eleId] == true) {
            //         others = {'type':'WRONG', 'message':'门已开'}
            //     } else if (ele_resetting[eleId] == true) {
            //         others = {'type':'WRONG', 'message':'重置中开门'}
            //     } else if (ele_floor[eleId] != t['floor']) {
            //         others = {'type':'WRONG', 'message':`开门楼层错误 当前:${ele_floor[eleId]}`}
            //     } else {
            //         ele_opening[eleId] = true;
            //     }
            // }
            // else if (t['type'] == 'CLOSE') {
            //     if (ele_opening[eleId] == false) {
            //         others = {'type':'WRONG', 'message':'门已关'}
            //     } else if (ele_resetting == true) {
            //         others = {'type':'WRONG', 'message':'重置中关门'}
            //     } else if (ele_floor[eleId] != t['floor']) {
            //         others = {'type':'WRONG', 'message':`关门楼层错误 当前:${ele_floor[eleId]}`}
            //     } else {
            //         ele_opening[eleId] = false;
            //     }
            // }
            // else if (t['type'] == 'ARRIVE') {
            //     if (ele_received[eleId].size === 0) {
            //         others = {'type': 'WRONG', 'message':'没有RECEIVE'}
            //     } else if (Math.abs(ele_floor[eleId] - t['floor']) != 1) {
            //         others = {'type': 'WRONG', 'message':`移动层数不为1: ${ele_floor[eleId]}-${t['floor']}`}
            //     } else if (t['floor'] > 11 || t['floor'] < 1) {
            //         others = {'type': 'WRONG', 'message':'楼层非法'}
            //     } else if (ele_resetting[eleId] == true) {
            //         others = {'type': 'WRONG', 'message':'重置中移动'}
            //     } else {
            //         ele_floor[eleId] = t['floor'];
            //     }
            // }
            else if (t['type'] == 'IN') {
                // if (ele_opening[eleId] == false) {
                //     others = {'type':'WRONG', 'message':'门没开'}
                // } else {
                //     if (!ele_received[eleId].has(pasId)) {
                //         others = {'type':'WRONG', 'message':'未RECEIVE'}
                //     } else if (ele_resetting[eleId] == true) {
                //         others = {'type': 'WRONG', 'message':'重置中进入'}
                //     } else {
                //         wait_passengers.delete(pasId);
                //     }
                // }
                let pasId = t['passengerID'];
                ele_passengers[eleId].add(pasId);
            }
            else if (t['type'] == 'OUT') {
                // if (ele_opening[eleId] == false) {
                //     others = {'type':'WRONG', 'message':'门没开'}
                // } else if (ele_resetting[eleId] == true) {
                //     others = {'type': 'WRONG', 'message':'重置中离开'}
                // } else {
                //     if (!ele_passengers[eleId].has(pasId)) {
                //         others = {'type':'WRONG', 'message':'电梯里没这个人'}
                //     } else {
                //         pas_received.delete(pasId);
                //     }
                // }
                let pasId = t['passengerID'];
                ele_passengers[eleId].delete(pasId);
                ele_received[eleId].delete(pasId);
            }
            else if (t['type'] == 'RECEIVE') {
                let pasId = t['passengerID']
                // if (ele_received[eleId].has(pasId)) {
                //     others = {'type':'WRONG','message':'本电梯RECEIVE过这个人'}
                // } else if (pas_received.has(pasId)) {
                //     others = {'type':'WRONG','message':'这个人已经RECEIVE过'}
                // } else if (ele_resetting[eleId] == true) {
                //     others = {'type': 'WRONG', 'message':'重置中RECEIVE'}
                // } else {
                //     pas_received.add(pasId);
                // }
                ele_received[eleId].add(pasId);
                // if (ele_received[eleId].has(pasId)) {
                //     others = {'type':'WRONG','message':'本电梯RECEIVE过这个人'}
                // } else if (pas_received.has(pasId)) {
                //     others = {'type':'WRONG','message':'这个人已经RECEIVE过'}
                // } else if (ele_resetting[eleId] == true) {
                //     others = {'type': 'WRONG', 'message':'重置中RECEIVE'}
                // } else {
                //     pas_received.add(pasId);
                // }
                ele_received[eleId].add(pasId);
            }
            // else if (t['type'] == 'RESET_ACCEPT') {
            // else if (t['type'] == 'RESET_ACCEPT') {

            // }
            // }
            else if (t['type'] == 'RESET_BEGIN') {
                // if (ele_passengers[eleId].size !== 0) {
                //     others = {'type':'WRONG','message':'电梯未清空'}
                // } else if (ele_opening[eleId] == true) {
                //     others = {'type':'WRONG','message':'没关门'}
                // } else if (ele_resetting[eleId] == true) {
                //     others = {'type': 'WRONG', 'message':'重置中重置'}
                // } else {
                //     ele_resetting[eleId] = true;
                //     ele_received[eleId].forEach((pasId) => {
                //         pas_received.delete(pasId);
                //     })
                // }
                ele_received[eleId] = new Set();
            }
            // else if (t['type'] == 'RESET_END') {
            //     if (ele_resetting[eleId] != true) {
            //         others = {'type': 'WRONG', 'message':'没有开始重置，不能结束'}
            //     } else {
            //         ele_resetting[eleId] = false;
            //     }
            // }
            // else if (t['type'] == 'REQUEST') {
            //     wait_passengers.add(t['passengerID'])
            //     others = {'type':'none', 'message':''}
            // }
            // else if (t['type'] == 'RESET') {
            //     others = {'type':'none', 'message':''}
            // }
            // else {
            //     others = {'type':'none', 'message':''}
            // }
                // if (ele_passengers[eleId].size !== 0) {
                //     others = {'type':'WRONG','message':'电梯未清空'}
                // } else if (ele_opening[eleId] == true) {
                //     others = {'type':'WRONG','message':'没关门'}
                // } else if (ele_resetting[eleId] == true) {
                //     others = {'type': 'WRONG', 'message':'重置中重置'}
                // } else {
                //     ele_resetting[eleId] = true;
                //     ele_received[eleId].forEach((pasId) => {
                //         pas_received.delete(pasId);
                //     })
                // }
                ele_received[eleId] = new Set();
            }
            // else if (t['type'] == 'RESET_END') {
            //     if (ele_resetting[eleId] != true) {
            //         others = {'type': 'WRONG', 'message':'没有开始重置，不能结束'}
            //     } else {
            //         ele_resetting[eleId] = false;
            //     }
            // }
            // else if (t['type'] == 'REQUEST') {
            //     wait_passengers.add(t['passengerID'])
            //     others = {'type':'none', 'message':''}
            // }
            // else if (t['type'] == 'RESET') {
            //     others = {'type':'none', 'message':''}
            // }
            // else {
            //     others = {'type':'none', 'message':''}
            // }
            res.push({
                'key': `${t['type']}-${i+1}`, 
                ...match(datalist[i]), 
                'passengers' : t['type'] == 'REQUEST' ? '' : eleId == 0 ? '' : setToString(ele_passengers[eleId]),
                'passengers' : t['type'] == 'REQUEST' ? '' : eleId == 0 ? '' : setToString(ele_passengers[eleId]),
                'received' : eleId == 0 ? '' : setToString(ele_received[eleId]),
                'others' : others,
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
            <Space size={10}>
                <TextArea 
                    onChange={onTimestampOffsetChange}
                    defaultValue={timestampOffset}
                    autoSize={{maxRows: 1}}
                    style={{width: '100px'}}
                />
                <Button onClick={() => {
                        setDataInput(dataInput);
                        setDataOutput(dataOutput);
                        let _input = matchText(dataInput);
                        let _output = matchText(dataOutput);
                        var res = [..._input, ..._output]
                        res.sort((a, b) => {
                            return a.timestamp - b.timestamp
                        })
                        setTableData(res);
                    }}>
                    设置输出时间偏移
                </Button>
            </Space>
            <Button onClick={openDrawer} type="primary">打开输入框</Button>
        </Row>
        <Table 
            columns={columns} 
            dataSource={tableData} 
            pagination={false} 
            size={tableSize}
            scroll={{y:'calc(100vh - 300px)'}}
        />
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

    const regexArrive       = /\[ *([\d.]+)\]ARRIVE-(\d+)-(\d+-?[A|B]?)/;
    const regexOpen         = /\[ *([\d.]+)\]OPEN-(\d+)-(\d+-?[A|B]?)/;
    const regexClose        = /\[ *([\d.]+)\]CLOSE-(\d+)-(\d+-?[A|B]?)/;
    const regexIn           = /\[ *([\d.]+)\]IN-(\d+)-(\d+)-(\d+-?[A|B]?)/;
    const regexOut          = /\[ *([\d.]+)\]OUT-(\d+)-(\d+)-(\d+-?[A|B]?)/;
    const regexFrom         = /\[ *([\d.]+)\](\d+)-FROM-(\d+)-TO-(\d+)/;
    const regexReset        = /\[ *([\d.]+)\]RESET-Elevator-(\d+)-(\d+)-([\d.]+)/;
    const regexDCReset      = /\[ *([\d.]+)\]RESET-DCElevator-(\d+)-(\d+)-(\d+)-([\d.]+)/;
    const regexResetAccept  = /^\[ *([\d.]+)\]RESET_ACCEPT-(\d+)-(\d+)-([\d.]+)$/;
    const regexDCResetAccept  = /^\[ *([\d.]+)\]RESET_ACCEPT-(\d+)-(\d+)-(\d+)-([\d.]+)$/;
    const regexResetBgein   = /\[ *([\d.]+)\]RESET_BEGIN-(\d+)/;
    const regexResetEnd     = /\[ *([\d.]+)\]RESET_END-(\d+)/;
    const regexReceive      = /\[ *([\d.]+)\]RECEIVE-(\d+)-(\d+-?[A|B]?)/;

    let matchArrive = inputString.match(regexArrive);
    let matchOpen = inputString.match(regexOpen);
    let matchClose = inputString.match(regexClose);
    let matchIn = inputString.match(regexIn);
    let matchOut = inputString.match(regexOut);
    let matchFrom = inputString.match(regexFrom);
    let matchReset = inputString.match(regexReset);
    let matchDCReset = inputString.match(regexDCReset);
    let matchResetAccept = inputString.match(regexResetAccept);
    let matchDCResetAccept = inputString.match(regexDCResetAccept);
    let matchResetBegin = inputString.match(regexResetBgein);
    let matchResetEnd = inputString.match(regexResetEnd);
    let matchReceive = inputString.match(regexReceive);

    if (matchArrive) {
        const timestamp = parseFloat(matchArrive[1]) + timeOff;
        const floor = matchArrive[2];
        const elevatorID = matchArrive[3];
        // console.log("ARRIVE:", timestamp, floor, elevatorID);
        return {
            'inout' : 'OUTPUT',
            'type': 'ARRIVE',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor': floor,
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchOpen) {
        const timestamp = parseFloat(matchOpen[1]) + timeOff;
        const floor = matchOpen[2];
        const elevatorID = matchOpen[3];
        // console.log("OPEN:", timestamp, floor, elevatorID);
        return {
            'inout' : 'OUTPUT',
            'type': 'OPEN',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor': floor,
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchClose) {
        const timestamp = parseFloat(matchClose[1]) + timeOff;
        const floor = matchClose[2];
        const elevatorID = matchClose[3];
        // console.log("CLOSE:", timestamp, floor, elevatorID);
        return {
            'inout' : 'OUTPUT',
            'type': 'CLOSE',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor': floor,
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchIn) {
        const timestamp = parseFloat(matchIn[1]) + timeOff;
        const passengerID = matchIn[2];
        const floor = matchIn[3];
        const elevatorID = matchIn[4];
        // console.log("IN:", timestamp, passengerID, floor, elevatorID);
        return {
            'inout' : 'OUTPUT',
            'type': 'IN',
            'timestamp': timestamp,
            'passengerID' : passengerID,
            'floor': floor,
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchOut) {
        const timestamp = parseFloat(matchOut[1]) + timeOff;
        const passengerID = matchOut[2];
        const floor = matchOut[3];
        const elevatorID = matchOut[4];
        // console.log("OUT:", timestamp, passengerID, floor, elevatorID);
        return {
            'inout' : 'OUTPUT',
            'type': 'OUT',
            'timestamp': timestamp,
            'passengerID' : passengerID,
            'floor': floor,
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
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
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchReset) {
        const timestamp = parseFloat(matchReset[1]);
        const elevatorID = matchReset[2];
        const capacity = matchReset[3];
        const speed = parseFloat(matchReset[4]);
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'INPUT',
            'type': 'RESET',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': capacity,
                'speed': speed,
                'translateFloor':'',
            },
            'origin' : text,
        }
    }  else if (matchDCReset) {
        const timestamp = parseFloat(matchDCReset[1]);
        const elevatorID = matchDCReset[2];
        const translateFloor = matchDCReset[3];
        const capacity = matchDCReset[4];
        const speed = parseFloat(matchDCReset[5]);
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'INPUT',
            'type': 'RESET(DC)',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': capacity,
                'speed': speed,
                'translateFloor': translateFloor,
                'translateFloor':'',
            },
            'origin' : text,
        }
    }  else if (matchDCReset) {
        const timestamp = parseFloat(matchDCReset[1]);
        const elevatorID = matchDCReset[2];
        const translateFloor = matchDCReset[3];
        const capacity = matchDCReset[4];
        const speed = parseFloat(matchDCReset[5]);
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'INPUT',
            'type': 'RESET(DC)',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': capacity,
                'speed': speed,
                'translateFloor': translateFloor,
            },
            'origin' : text,
        }
    }  else if (matchResetAccept) {
        const timestamp = parseFloat(matchResetAccept[1]) + timeOff;
        const elevatorID = matchResetAccept[2];
        const capacity = matchResetAccept[3];
        const speed = parseFloat(matchResetAccept[4]);
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'OUTPUT',
            'type': 'RESET_ACCEPT',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': capacity,
                'speed': speed,
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchDCResetAccept) {
        const timestamp = parseFloat(matchDCResetAccept[1]) + timeOff;
        const elevatorID = matchDCResetAccept[2];
        const translateFloor = matchDCResetAccept[3];
        const capacity = matchDCResetAccept[4];
        const speed = parseFloat(matchDCResetAccept[5]);
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'OUTPUT',
            'type': 'RESET_ACCEPT(DC)',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': capacity,
                'speed': speed,
                'translateFloor': translateFloor,
                'translateFloor':'',
            },
            'origin' : text,
        }
    } else if (matchDCResetAccept) {
        const timestamp = parseFloat(matchDCResetAccept[1]) + timeOff;
        const elevatorID = matchDCResetAccept[2];
        const translateFloor = matchDCResetAccept[3];
        const capacity = matchDCResetAccept[4];
        const speed = parseFloat(matchDCResetAccept[5]);
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'OUTPUT',
            'type': 'RESET_ACCEPT(DC)',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': capacity,
                'speed': speed,
                'translateFloor': translateFloor,
            },
            'origin' : text,
        }
    } else if (matchResetBegin) {
        const timestamp = parseFloat(matchResetBegin[1]) + timeOff;
        const elevatorID = matchResetBegin[2];
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'OUTPUT',
            'type': 'RESET_BEGIN',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    }   else if (matchResetEnd) {
        const timestamp = parseFloat(matchResetEnd[1]) + timeOff;
        const elevatorID = matchResetEnd[2];
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'OUTPUT',
            'type': 'RESET_END',
            'timestamp': timestamp,
            'passengerID' : '',
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
            },
            'origin' : text,
        }
    }  else if (matchReceive) {
        const timestamp = parseFloat(matchReceive[1]) + timeOff;
        const passengerID = matchReceive[2];
        const elevatorID = matchReceive[3];
        // console.log("FROM:", timestamp, passengerID, beginFloor, endFlood);
        return {
            'inout' : 'OUTPUT',
            'type': 'RECEIVE',
            'timestamp': timestamp,
            'passengerID' : passengerID,
            'floor' : '',
            'elevatorID' : elevatorID,
            'elevatorSettings' : {
                'capacity': '',
                'speed': '',
                'translateFloor':'',
                'translateFloor':'',
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
                'capacity': '',
                'speed': '',
                'translateFloor':'',
            },
            'origin' : text,
        }
    }

}