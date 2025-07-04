console.log("匹配到扩展程序")

setTimeout(function () {
    login();
}, 500);

function login() {
    document.getElementsByClassName("btn--QDjHtErD")[0].click()
    console.log("login")
}