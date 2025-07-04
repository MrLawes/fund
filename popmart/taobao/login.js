console.log("匹配到扩展程序")

setInterval(function () {
    const now = new Date();
    const hour = now.getHours();
    const minute = now.getMinutes();
    const second = now.getSeconds(); // 获取当前秒数
    console.log(now)
    console.log(hour)
    console.log(minute)
    console.log(second)
    if (hour === 21 && minute === 59 && second === 59) {
        login();
    }
    if (hour === 22 && minute === 0 && second === 0) {
        login();
    }
    if (hour === 22 && minute === 0 && second === 1) {
        login();
    }
    if (hour === 22 && minute === 0 && second === 2) {
        login();
    }
    if (hour === 22 && minute === 0 && second === 3) {
        login();
    }
}, 500);


function login() {
    document.getElementsByClassName("btn--QDjHtErD")[0].click()
    console.log("taobao")
}