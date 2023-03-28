setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        toolbar_left = document.getElementsByClassName('toolbar-left')[0]
        if (toolbar_left.children.length <= 4) {
            iiilab = document.createElement("a");
            textnode = document.createTextNode("https://bilibili.iiilab.com/");
            iiilab.appendChild(textnode)
            span = document.createElement("span");
            span.appendChild(iiilab);
            toolbar_left.appendChild(span);
            console.log(toolbar_left.children.length)
        }

    }, 1000)
}

