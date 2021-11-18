function easyHTTP() {

    // Initializing new XMLHttpRequest method.
    this.http = new XMLHttpRequest();
}


// Make an HTTP PUT Request
easyHTTP.prototype.put = function (url, data, callback) {

    // Open an object (POST, PATH, ASYNC-TRUE/FALSE)
    this.http.open('PUT', url, false);

    // Set content-type
    this.http.setRequestHeader(
        'Content-type', 'application/json');

    // Assigning this to self to have
    // scope of this into the function onload
    let self = this;

    // When response is ready
    this.http.onload = function () {
        if ([200, 201].includes(self.http.status)) {
            callback(self.http.status, self.http.responseText);
        } else {
            console.log('网络异常')
            alert('网络异常: ' + self.http.status + ':' + self.http.responseText)
            callback(self.http.status, self.http.responseText);
        }
        callback(self.http.status, self.http.responseText);
    }

    // Since the data is an object so
    // we need to stringify it
    this.http.send(JSON.stringify(data));
}


// Make an HTTP PUT Request
easyHTTP.prototype.get = function (url, data, callback) {

    // Open an object (POST, PATH, ASYNC-TRUE/FALSE)
    this.http.open('GET', url, false);

    // Set content-type
    this.http.setRequestHeader(
        'Content-type', 'application/json');

    // Assigning this to self to have
    // scope of this into the function onload
    let self = this;

    // When response is ready
    this.http.onload = function () {
        if ([200, 201].includes(self.http.status)) {
            callback(self.http.status, self.http.responseText);
        } else {
            console.log('网络异常')
            alert('网络异常: ' + self.http.status + ':' + self.http.responseText)
            callback(self.http.status, self.http.responseText);
        }
        callback(self.http.status, self.http.responseText);
    }

    // Since the data is an object so
    // we need to stringify it
    this.http.send(JSON.stringify(data));
}

