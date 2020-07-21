item_pie();
item_bar();
item_gauge();

function item_pie() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var data = JSON.parse(xmlHttp.responseText);
            var Chart = echarts.init(document.getElementById('item_pie'));
            var option_pie = {
                tooltip: {},
                series: [
                    {
                        name: '访问来源',
                        type: 'pie',
                        center: ['50%', '50%'],
                        radius: '65%',
                        data: data,
                        roseType: 'angle',

                        itemStyle: {
                            emphasis: {
                                shadowBlur: 200,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: { //字体样式
                            normal: {
                                textStyle: {
                                    // color: 'rgba(255, 255, 255, 0.3)'
                                    color: 'black'
                                }
                            }
                        },
                        labelLine: { //线条样式
                            normal: {
                                lineStyle: {
                                    // color: 'rgba(255, 255, 255, 0.3)'
                                    color: 'orange'
                                }
                            }
                        }

                    }
                ]
            };
            Chart.setOption(option_pie);
        }
    };
    xmlHttp.open("GET", '/custom_page/echartsData/', true);
    xmlHttp.send();
}

function item_bar() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var data = JSON.parse(xmlHttp.responseText);
            var names = [];
            var values = [];
            for (var i = 0; i < data.length; i++) {
                names.push(data[i].name);
                values.push(data[i].value);
            }
            var Chart = echarts.init(document.getElementById('item_bar'));
            var option_bar = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                legend: {
                    data: ['AAA', 'BBB']
                },
                xAxis: {
                    data: names
                },
                yAxis: {},
                series: [{
                    name: 'AAA',
                    type: 'bar',
                    data: values,
                    color: 'darkred'
                }, {
                    name: 'BBB',
                    type: 'bar',
                    data: values,
                    color: 'black'
                }]
            };
            Chart.setOption(option_bar);
        }
    };
    xmlHttp.open("GET", '/custom_page/echartsData/', true);
    xmlHttp.send();
}

function item_gauge() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
//            var data = JSON.parse(xmlHttp.responseText);
            var data = [{'name': '完成率', 'value': (Math.random() * 100).toFixed(2)}];
            var Chart = echarts.init(document.getElementById('item_gauge'));
            var option_gauge = {
                tooltip: {
                    formatter: "{a} <br/>{b} : {c}%"
                },
                toolbox: {
                    feature: {
                        restore: {},
                        saveAsImage: {}
                    }
                },
                series: [
                    {
                        name: '业务指标',
                        type: 'gauge',
                        detail: {formatter: '{value}%'},
                        data: data
                    }
                ]
            };
            Chart.setOption(option_gauge);
        }
    };
    xmlHttp.open("GET", '/custom_page/echartsData/', true);
    xmlHttp.send();
}

function pie() {
    document.getElementById('demoItems').hidden = true;
    document.getElementById('return').hidden = false;
    document.getElementById('main_pie').hidden = false;
    document.getElementById('main_bar').hidden = true;
    document.getElementById('main_gauge').hidden = true;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var data = JSON.parse(xmlHttp.responseText);
            var myChart = echarts.init(document.getElementById('main_pie'));
            var option_pie = {
                tooltip: {},
                series: [
                    {
                        name: '访问来源',
                        type: 'pie',
                        center: ['50%', '50%'],
                        radius: '65%',
                        data: data,
                        roseType: 'angle',

                        itemStyle: {
                            emphasis: {
                                shadowBlur: 200,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        },
                        label: { //字体样式
                            normal: {
                                textStyle: {
                                    // color: 'rgba(255, 255, 255, 0.3)'
                                    color: 'black'
                                }
                            }
                        },
                        labelLine: { //线条样式
                            normal: {
                                lineStyle: {
                                    // color: 'rgba(255, 255, 255, 0.3)'
                                    color: 'orange'
                                }
                            }
                        }

                    }
                ]
            };
            myChart.setOption(option_pie);
        }
    };
    xmlHttp.open("GET", '/custom_page/echartsData/', true);
    xmlHttp.send();
}

function bar() {
    document.getElementById('demoItems').hidden = true;
    document.getElementById('return').hidden = false;
    document.getElementById('main_pie').hidden = true;
    document.getElementById('main_bar').hidden = false;
    document.getElementById('main_gauge').hidden = true;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
            var data = JSON.parse(xmlHttp.responseText);
            var names = [];
            var values = [];
            for (var i = 0; i < data.length; i++) {
                names.push(data[i].name);
                values.push(data[i].value);
            }
            var myChart = echarts.init(document.getElementById('main_bar'));
            var option_bar = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                legend: {
                    data: ['AAA', 'BBB']
                },
                xAxis: {
                    data: names
                },
                yAxis: {},
                series: [{
                    name: 'AAA',
                    type: 'bar',
                    data: values,
                    color: 'darkred'
                }, {
                    name: 'BBB',
                    type: 'bar',
                    data: values,
                    color: 'black'
                }]
            };
            myChart.setOption(option_bar);
        }
    };
    xmlHttp.open("GET", '/custom_page/echartsData/', true);
    xmlHttp.send();
}

function gauge() {
    document.getElementById('demoItems').hidden = true;
    document.getElementById('return').hidden = false;
    document.getElementById('main_pie').hidden = true;
    document.getElementById('main_bar').hidden = true;
    document.getElementById('main_gauge').hidden = false;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
//            var data = JSON.parse(xmlHttp.responseText);
            var data = [{'name': '完成率', 'value': (Math.random() * 100).toFixed(2)}];
            var Chart = echarts.init(document.getElementById('main_gauge'));
            var option_gauge = {
                tooltip: {
                    formatter: "{a} <br/>{b} : {c}%"
                },
                toolbox: {
                    feature: {
                        restore: {},
                        saveAsImage: {}
                    }
                },
                series: [
                    {
                        name: '业务指标',
                        type: 'gauge',
                        detail: {formatter: '{value}%'},
                        data: data
                    }
                ]
            };
            Chart.setOption(option_gauge);
        }
    };
    xmlHttp.open("GET", '/custom_page/echartsData/', true);
    xmlHttp.send();
}

function showBTN() {
    document.getElementById('demoItems').hidden = false;
    document.getElementById('return').hidden = true;
    document.getElementById('main_pie').hidden = true;
    document.getElementById('main_bar').hidden = true;
    document.getElementById('main_gauge').hidden = true;
}

function turnURL() {
    location.href = "http://localhost:8069/web#id=48&action=187&model=product.template&view_type=form&menu_id=89"
}
