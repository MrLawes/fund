function douyin() {


    if (location.pathname == '/') {
        douyin_index()
    }
    if (location.pathname.startsWith("/user/")) {
        douyin_user()
    }

}

function douyin_index() {
    // 抖音首页，找到个人中心，并点击
    setTimeout(function () {
        var touxiang = document.getElementsByTagName('img')[0]
        touxiang.click();
    }, 2000);
}

function douyin_user() {
    // 抖音个人中心，找到关注并点击
    setTimeout(function () {
        var divs = document.getElementsByTagName('div')
        for (i = 0; i < divs.length; i++) {
            if (divs[i].innerHTML == '关注') {
                divs[i].click()
            }
        }
        // 点击最早关注
        setTimeout(function () {
            earliest = document.getElementById('earliest')
            earliest.click()

            // 滚动粉丝列
            setTimeout(function () {
                fens = a.parentElement.parentElement.parentElement.nextElementSibling
            }, 1000);

            // window.scrollTo({"behavior": "smooth", "top": 110})
        }, 1000);


    }, 1000);
}

document.getElementsByTagName('span')

douyin();