function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time * 1000));
}


function douyin() {

    if (location.pathname == '/') {
        douyin_index()
    }
    if (location.pathname.startsWith("/user/")) {
        if (location.pathname == '/user/MS4wLjABAAAA9B2cv7UtaBaj5ZCZaSMew-HMYF-k17nY_VGrZWP7fGK10hLQBbhjWzGdBSCIcZj8') {
            douyin_my_user()
        } else {
            douyin_friend_user()
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
    window.scrollto;
    window.scrollto = 1;
    const http = new easyHTTP;

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
        console.log(new Date() + ' 点击综合排序 -> 最近关注')
        // earliest = document.getElementById('earliest')
        earliest = document.getElementById('latest')
        earliest.click()
    })


    var divs = document.getElementsByTagName('div')
    for (i = 0; i < divs.length; i++) {
        if (divs[i].innerHTML == '关注') {
            let fens_count = 1500
            // let fens_count = divs[i].parentElement.nextElementSibling.children[1].innerText
            i = divs.length
            console.log(new Date() + ' 滚动 ' + fens_count + ' 次')
            for (j = -1; j < fens_count; j++) {
                window.timeout += 5
                sleep(window.timeout).then(() => {
                    console.log(new Date() + ' 滚动 ' + window.scrollto)
                    window.scrollto += 1
                    earliest = document.getElementById('earliest')
                    let fens = earliest.parentElement.parentElement.parentElement.nextElementSibling
                    fens.scrollTo(0, window.scrollto * 97)
                    let fen = fens.children[0].children[(window.scrollto - 1) * 3]
                    let fen_info = fen.children[1].children[0].children[0].children[0]
                    let relationship = fen.children[2].innerText
                    let first_name = fen_info.innerText
                    let fen_href = fen_info.href
                    console.log(new Date() + ' relationship: ' + relationship)
                    console.log(new Date() + ' fen_name: ' + first_name)
                    console.log(new Date() + ' fen_href: ' + fen_href)
                    var data = {'relationship': relationship, 'first_name': first_name, 'href': fen_href}
                    http.post(
                        'http://127.0.0.1:8000/v4/douyin/users/',
                        data, function (status, responseText) {
                            console.log(new Date() + ' 请求返回: ' + responseText)
                        }
                    );
                    fen_info.click()

                })
            }
        }
    }


}

function douyin_friend_user() {
    const http = new easyHTTP;
    const data = {
        href: location.pathname,
    };
    http.get(
        'http://127.0.0.1:8000/v4/douyin/users/get_user_by_href/?href=' + location.pathname,
        data, function (status, responseText) {
            console.log(new Date() + ' 请求返回: ' + responseText)
            let user_id = JSON.parse(responseText)['id']
            if (user_id) {
                let header = document.getElementsByTagName('header')[0]
                let username = header.parentElement.parentElement.parentElement.children[1].children[0].children[1].children[0].children[2].innerText
                let user_info = header.parentElement.parentElement.parentElement.children[1].children[0].children[1].children[0].children[0].children
                let relationship = header.parentElement.parentElement.parentElement.children[1].children[0].children[1].children[0].children[4].children[0].innerText
                let follow_count = user_info[1].children[0].children[1].innerText
                if (follow_count.includes('w') || follow_count.includes('W')) {
                    follow_count = follow_count.replace(/W/i, "") * 10000
                }
                let fens_count = user_info[1].children[1].children[1].innerText
                if (fens_count.includes('w') || fens_count.includes('W')) {
                    fens_count = fens_count.replace(/W/i, "") * 10000
                }
                let head_url = user_info[0].children[0].children[0].src
                put_data = {
                    'username': username,
                    'follow_count': follow_count,
                    'fens_count': fens_count,
                    "head_url": head_url,
                    "relationship": relationship,
                }
                http.put(
                    'http://127.0.0.1:8000/v4/douyin/users/' + user_id + '/',
                    put_data, function (status, responseText) {
                        console.log(new Date() + ' 请求返回: ' + responseText)
                        need_delete = JSON.parse(responseText)['need_delete']
                        if (need_delete) {
                            document.getElementsByTagName('button')[1].click()
                        }
                    }
                );
            }
        }
    );
    if (!location.search.includes('close=false')) {
        sleep(3).then(() => {
            window.close()
        })
    }
}

douyin();