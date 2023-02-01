setTimeout(function () {
    run();
}, 1000);

function run() {
    setInterval(function () {
        names = document.getElementsByClassName('basicInfo-item name')
        for (index = 0; index < names.length; index++) {
            name = names[index]
            console.log('name' + name)
        }
    }, 1000)

}