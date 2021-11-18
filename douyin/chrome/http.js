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

        // Callback function (Error, response text)
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

        // Callback function (Error, response text)
        callback(null, self.http.responseText);
    }

    // Since the data is an object so
    // we need to stringify it
    this.http.send(JSON.stringify(data));
}

