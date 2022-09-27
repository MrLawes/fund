function mv() {

    setInterval(function () {
        const http = new easyHTTP;
        const data = {};
        http.get(
            'http://127.0.0.1:8000/v4/mv/get_download_url/',
            data, function (status, responseText) {
                let input_ele = document.getElementsByTagName('input')[0]
                let download_url = JSON.parse(responseText)['download_url']
                if (download_url) {
                    let evt = document.createEvent('HTMLEvents');
                    evt.initEvent('input', true, true);
                    input_ele.value = download_url
                    input_ele.dispatchEvent(evt)

                    // 下载完毕。。。。。。

                }

                // let t=document.getElementsByClassName('c_l_area c_a_n')[0];
                // let evt = document.createEvent('HTMLEvents');
                // evt.initEvent('input', true, true);
                // t.value='setValue';
                // t.dispatchEvent(evt)
                //
                //
            }
        );
    }, 1000000000)
    // }, 1000)
}

mv();