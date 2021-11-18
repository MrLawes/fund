function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time * 1000));
}


function douyin() {

    if (location.pathname == '/') {
        douyin_index()
    }
    if (location.pathname.startsWith("/user/")) {
        if (location.search == '?enter_from=recommend&enter_method=top_bar') {
            douyin_my_user()
        }
    }

}

function douyin_index() {
    console.log(new Date() + ' 点击我的头像')
    sleep(1).then(() => {
        var touxiang = document.getElementsByTagName('img')[0]
        touxiang.click();
    })
}

function douyin_my_user() {

    window.fens_count;
    window.timeout;
    window.timeout = 1;


    sleep(window.timeout).then(() => {
        console.log(new Date() + ' 点击关注')
        var divs = document.getElementsByTagName('div')
        for (i = 0; i < divs.length; i++) {
            if (divs[i].innerHTML == '关注') {
                // 更新粉丝数量
                window.fens_count = divs[i].parentElement.nextElementSibling.children[1].innerText
                divs[i].click()
            }
        }
    })

    window.timeout += 1
    sleep(window.timeout).then(() => {
        console.log(new Date() + ' 更新粉丝数据到数据库')
        const http = new easyHTTP;
        const data = {
            fens_count: window.fens_count,
        };
        http.put(
            'http://127.0.0.1:8000/v4/douyin/users/3/',
            data, function (status, responseText) {
                console.log(new Date() + ' 请求返回: ' + responseText)
                window.test = responseText;
            }
        );
    })

    window.timeout += 1
    sleep(window.timeout).then(() => {
        console.log(new Date() + ' 点击综合排序 -> 最早关注')
        earliest = document.getElementById('earliest')
        earliest.click()
    })


    // window.timeout += 1;
    // setTimeout(function () {
    //     console.log(new Date() + ' 点击 关注 -> 最早关注')
    //     earliest = document.getElementById('earliest')
    //     earliest.click()
    // }, 1000 * window.timeout);

    //
    // // 抖音个人中心，找到关注并点击
    // setTimeout(function () {
    //     var divs = document.getElementsByTagName('div')
    //     for (i = 0; i < divs.length; i++) {
    //         if (divs[i].innerHTML == '关注') {
    //
    //             // 更新粉丝数量
    //             window.fens_count = divs[i].parentElement.nextElementSibling.children[1].innerText
    //             divs[i].click()
    //             console.log(new Date() + ' 点击关注：')
    //         }
    //     }
    // }, 1000 * window.timeout);
    //
    // const http = new easyHTTP;
    // const data = {
    //     fens_count: window.fens_count,
    // };
    // http.put(
    //     'http://127.0.0.1:8000/v4/douyin/users/3/',
    //     data, function (status, responseText) {
    //         console.log(new Date() + ' 请求参数: ' + data.toString)
    //         console.log(new Date() + ' 请求返回: ' + responseText)
    //         window.test = responseText;
    //     });
    //
    // window.timeout += 1;
    // setTimeout(function () {
    //     console.log(new Date() + ' 点击 关注 -> 最早关注')
    //     earliest = document.getElementById('earliest')
    //     earliest.click()
    // }, 1000 * window.timeout);


    //
    //
    // for (i = 0; i = window.fens_count; i++) {
    //
    //     setTimeout(function () {
    //         var touxiang = document.getElementsByTagName('img')[0]
    //         touxiang.click();
    //     }, 1000 * i);
    //
    //
    // }
    //
    // if (window.fens_count) {
    //
    //
    //     console.log(2222222)
    // }

    // sleep(1)
    // earliest = document.getElementById('earliest')
    // earliest.click()
    // console.log(new Date() + ' 点击 关注 -> 最早关注')
    //
    // console.log(new Date() + ' 准备下滑')
    // sleep(1)

    // const http = new easyHTTP;
    // http.get(
    //     'http://127.0.0.1:8000/v4/douyin/users/3/',
    //     {}, function (status, responseText) {
    //         // let fens_count = JSON.parse(responseText)['fens_count']
    //         let fens_count = 30
    //         for (i = 0; i < fens_count; i++) {
    //             sleep(1)
    //             console.log(new Date() + ' scrollTo:'+i)
    //             earliest = document.getElementById('earliest')
    //             let fens = earliest.parentElement.parentElement.parentElement.nextElementSibling
    //             fens.scrollTo(0, i * 100)
    //         }
    //     });

}


douyin();