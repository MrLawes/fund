console.log("匹配到扩展程序")

setInterval(function () {
    const now = new Date();
    const hour = now.getHours();
    const minute = now.getMinutes();
    console.log(now)
    console.log(hour)
    console.log(minute)
    if (hour === 21 && minute === 41) {
        login();
    }
}, 1000);


function login() {
    document.getElementsByClassName("btn--QDjHtErD")[0].click()
    console.log("taobao")
}