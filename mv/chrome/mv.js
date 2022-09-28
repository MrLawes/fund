function mv() {

    setInterval(function () {
        const http = new easyHTTP;
        const data = {};
        http.get(
            'http://127.0.0.1:8000/v4/mv/get_download_url/',
            data, function (status, responseText) {
                let input_ele = document.getElementsByTagName('input')[0]
                let download_url = JSON.parse(responseText)['download_url']
                console.log('获得下载内容:' + responseText)
                if (download_url) {
                    let mv_id = JSON.parse(responseText)['id']
                    let evt = document.createEvent('HTMLEvents');
                    evt.initEvent('input', true, true);
                    input_ele.value = download_url
                    input_ele.dispatchEvent(evt)
                    document.getElementsByTagName('button')[1].click()
                    http.get(
                        'http://127.0.0.1:8000/v4/mv/sleep/',
                        {}, function (status, responseText) {
                        })
                    let name = document.getElementsByClassName('caption')[0].innerText
                    let href = document.getElementsByClassName('btn btn-success')[0].href
                    http.put(
                        'http://127.0.0.1:8000/v4/mv/' + mv_id + '/set_downloading',
                        {'name': name, 'href': href}, function (status, responseText) {
                        })
                    // document.getElementsByClassName('btn btn-success')[0].click()
                    http.get(
                        'http://127.0.0.1:8000/v4/mv/sleep/',
                        {}, function (status, responseText) {
                        })
                    // setTimeout(function () {
                    //     // const data = {};
                    //     // http.get(
                    //     //     'http://127.0.0.1:8000/v4/mv/get_download_url/',
                    //     //     data, function (status, responseText) {
                    //     //         let input_ele = document.getElementsByTagName('input')[0]
                    //     //         let download_url = JSON.parse(responseText)['download_url']
                    //     //         if (download_url) {
                    //     //             let evt = document.createEvent('HTMLEvents');
                    //     //             evt.initEvent('input', true, true);
                    //     //             input_ele.value = download_url
                    //     //             input_ele.dispatchEvent(evt)
                    //     //             document.getElementsByTagName('button')[1].click()
                    //     //             let_name = document.getElementsByClassName('caption')[0].innerText
                    //     //             console.log(let_name)
                    //     //
                    //     //         }
                    //     //     }
                    //     // );
                    // }, 5000)

                }
            }
        );
    }, 3000)
    // }, 1000)
}

mv();