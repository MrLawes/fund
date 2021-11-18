function sleep(timeout) {
    const http = new easyHTTP;
    const data = {};
    http.get(
        'http://127.0.0.1:8000/v4/douyin/users/sleep/?timeout=' + timeout,
        data, function (err, post) {
            if (err) {
                alert(1)
                alert(err)
            } else {
                alert(2)
                alert(err)
            }
        });
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

    console.log('准备点击我的头像')
    sleep(1)
    console.log('准备点击我的头像')
    console.log('准备点击我的头像')
    sleep(1)
    console.log('准备点击我的头像')
    console.log('准备点击我的头像')
    sleep(1)
    console.log('准备点击我的头像')
    console.log('准备点击我的头像')
    sleep(1)
    console.log('准备点击我的头像')

    // 抖音首页，找到个人中心，并点击
    sleep(1000).then(() => {
        var touxiang = document.getElementsByTagName('img')[0]
        touxiang.click();
    })
}

function douyin_my_user() {

    // 抖音个人中心，找到关注并点击
    console.log('准备点击关注')
    sleep(1000).then(() => {
        var divs = document.getElementsByTagName('div')
        for (i = 0; i < divs.length; i++) {
            if (divs[i].innerHTML == '关注') {

                // 更新粉丝数量
                var fens_count = divs[i].parentElement.nextElementSibling.children[1].innerText
                const http = new easyHTTP;
                const data = {
                    fens_count: fens_count,
                };
                http.put(
                    'http://127.0.0.1:8000/v4/douyin/users/3/',
                    data, function (err, post) {
                        if (err) {
                            console.log(err);
                        } else {
                            console.log(post);
                        }
                    });
                divs[i].click()
            }
        }
    })

    console.log('准备点击最早关注')
    // 点击最早关注
    sleep(1000).then(() => {
        earliest = document.getElementById('earliest')
        earliest.click()
    })

    sleep(1000).then(() => {
        console.log('准备下滑')
    })


    sleep_new(1)
    console.log('sleep 1')
    sleep_new(2)
    console.log('sleep 2')
    sleep_new(3)
    console.log('sleep 3')
    sleep_new(4)
    console.log('sleep 4')
    // while (i < 10) {
    //     sleep(1000).then(() => {
    //         console.log(i)
    //         // fens.scrollTo(0, 100)
    //         i++;
    //     })
    //
    // }

    // while (1) {
    //     // 滚动粉丝列
    earliest = document.getElementById('earliest')
    let fens = earliest.parentElement.parentElement.parentElement.nextElementSibling
    fens.scrollTo(0, 200)

}

// document.getElementsByTagName('span')

douyin();