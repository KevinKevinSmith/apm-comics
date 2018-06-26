var bookURL = "https://s3.amazonaws.com/YOUR_BUCKET_NAME/covers/"
var apiURL = "https://aaaaaaaaaaa.execute-api.us-east-1.amazonaws.com/prod/"

function loadBooks() {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
            if (xmlhttp.status == 200) {
                var result = xmlhttp.responseText;
                var jsonResult = JSON.parse(result);
                var innerBooks = "";
                for (var item in jsonResult) {
                    var title = jsonResult[item].title;
                    var isbn = jsonResult[item].isbn;
                    try {
                        var shortText = jsonResult[item].description.split(/\s+/).slice(0, 20).join(" ") + "...";
                    }
                    catch (err) {
                        var shortText = "";
                    }

                    var bookThumbnail = bookURL + isbn + "-L.jpg";
                    var book = "<div class=\"col-lg-3 col-md-6 mb-4\"> <div class=\"card\"> <img class=\"card-img-top\" src=\"{2}\" alt=\"\"> <div class=\"card-body\"> <h4 class=\"card-title\">{0}</h4> <p class=\"card-text\">{1}</p> </div> <div class=\"card-footer\"> <a href=\"item.html?isbn={3}\" class=\"btn btn-primary\">Buy Me!</a> </div> </div> </div>".format(title, shortText, bookThumbnail, isbn);
                    innerBooks = innerBooks + book + "\n\n";
                }
                document.getElementById('bookList').innerHTML = innerBooks;
            }
            else if (xmlhttp.status == 400) {
                alert('There was an error 400');
            }
            else {
                alert('something else other than 200 was returned');
            }
        }
    };

    xmlhttp.open("GET", apiURL+"/getItems", true);
    xmlhttp.send();
};

function loadItemDetails(requestedISBN)
{
    var jsonResult = getItemDetails(requestedISBN);

    var title = jsonResult.title;
    var isbn = jsonResult.isbn;
    var author = jsonResult.authors;
    var descr = jsonResult.description;
    var bookThumbnail = "https://s3.amazonaws.com/malones-comics-dev/covers/" + isbn + "-L.jpg";

    document.getElementById('item-title').innerHTML = title;
    document.getElementById('item-image').setAttribute("src", bookThumbnail);
    document.getElementById('item-author').innerHTML = author;
    document.getElementById('item-description').innerHTML = descr;

    loadCartButtons(isbn);

};

function loadCartButtons(isbn){
    var result = checkItemCart(isbn);
    if(result != undefined)
    {
        if(result['quantity']>0){
            document.getElementById('itmQty').value=result['quantity'];
            document.getElementById('removeCartButton').style.display='inline';
        }
        else{
            document.getElementById('itmQty').value=1;
            document.getElementById('removeCartButton').style.display='none';
        }
    }
    else{
        document.getElementById("addToCartDiv").innerText="Please login to add this item to your cart."
    }
}

function getItemDetails(requestedISBN) {
    var xmlhttp = new XMLHttpRequest();

    var postData = {"isbn": requestedISBN};
    xmlhttp.open("POST", apiURL+"/getItem", false);
    xmlhttp.send(JSON.stringify(postData));
    var result = xmlhttp.responseText;
    var jsonResult = JSON.parse(result);

    return jsonResult;
};

String.prototype.format = function () {
    var a = this;
    for (var k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
};

function getCustomerStatus() {
    var xmlhttp = new XMLHttpRequest();
    var email = document.getElementById("email").value;

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
            if (xmlhttp.status == 200) {
                var result = xmlhttp.responseText;
                var jsonResult = JSON.parse(result);

                if (jsonResult['status'] != "exists") {
                    hideRegistrationDiv(false);
                }
                else {
                    var greeting = jsonResult["first_name"] + " " + jsonResult["last_name"];
                    setAlertBanner("success", "<strong>Congrats " + greeting + "!</strong> Your account has been found.");
                    createSessionCookie(email);
                }

            }
            else if (xmlhttp.status == 400) {
                alert('There was an error 400');
            }
            else {
                alert('something else other than 200 was returned');
            }
        }
    };

    xmlhttp.open("POST", apiURL+"/getCustomer", true);
    xmlhttp.send("{\"action\": \"get\" , \"email\": \"" + email + "\"}");
};

function createSessionCookie(email)
{
    var sessionGUID = createSession(email);
    console.log(sessionGUID);
    Cookies.set('sessionGUID', sessionGUID, {expires: 13});
}

function createCustomer() {
    var xmlhttp = new XMLHttpRequest();
    var custDetails = {};

    var elements = document.getElementsByTagName("input");
    for (var ii = 0; ii < elements.length; ii++) {
        if (elements[ii].type == "text") {
            custDetails[elements[ii].id] = elements[ii].value;
        }
    }

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
            if (xmlhttp.status == 200) {
                var result = xmlhttp.responseText;
                var jsonResult = JSON.parse(result);

                if (jsonResult['status'] == "created") {
                    hideRegistrationDiv(true);
                    clearAllTextBoxes();
                    setAlertBanner("success", "<strong>Congrats!</strong> Your account has been created. Please login to continue");
                }
                else {
                    hideRegistrationDiv();
                    clearAllTextBoxes();
                    setAlertBanner("danger", "<strong>Oops!</strong> Your account has not been created. Please try again.");
                }

            }
            else if (xmlhttp.status == 400) {
                alert('There was an error 400');
            }
            else {
                alert('something else other than 200 was returned');
            }
        }
    };

    var postData = {"action": "create", "details": custDetails};
    xmlhttp.open("POST", apiURL+"/getCustomer", true);
    xmlhttp.send(JSON.stringify(postData));
};

function clearAllTextBoxes() {
    var elements = document.getElementsByTagName("input");
    for (var ii = 0; ii < elements.length; ii++) {
        if (elements[ii].type == "text") {
            elements[ii].value = "";
        }
    }
    hideAlertBanner();
};

function hideRegistrationDiv(hide) {
    if (hide == true) {
        document.getElementById("registrationDiv").style.display = "none";
    }
    else {
        document.getElementById("registrationDiv").style.display = "block";
    }

};

function hideAlertBanner() {
    var alertBanner = document.getElementById("alertBannerDiv");
    alertBanner.style.display = "none";
    alertBanner.removeAttribute("class");
    alertBanner.innerHTML = "";
};

function setAlertBanner(type, msg) {
    var alertBanner = document.getElementById("alertBannerDiv");
    alertBanner.setAttribute("class", "alert alert-" + type);
    alertBanner.innerHTML = msg;
    alertBanner.style.display = "block";
};

function createSession(email) {
    var xmlhttp = new XMLHttpRequest();

    var postData = {"email": email};
    xmlhttp.open("POST", apiURL+"/getSession", false);
    xmlhttp.send(JSON.stringify(postData));
    var result = xmlhttp.responseText;
    var jsonResult = JSON.parse(result);

    return jsonResult['sessionGUID'];
};

function checkSession(banner) {
    var sessionGUID = Cookies.get("sessionGUID")
    if (sessionGUID == undefined){
        if(banner)
        {
            setAlertBanner("danger", "Please log in to access this page. <a href=\"account.html\"></a>")
        }
        return undefined;
    }
    else
    {
        return sessionGUID;
    }
};

function getCart(){
    var sessionGUID = checkSession(true);
    if (sessionGUID != undefined){
        var xmlhttp = new XMLHttpRequest();
        var postData = {"action": "getcart", "sessionGUID": sessionGUID};
        xmlhttp.open("POST", apiURL+"/getCart", false);
        xmlhttp.send(JSON.stringify(postData));
        var result = xmlhttp.responseText;
        var jsonResult = JSON.parse(result);

        var tableRef = document.getElementById("cartBody")

        //Insert a row in the table at the last row
        for (var i=0; i<jsonResult.length; i++) {
            var newRow = tableRef.insertRow(-1);

            var newCell = newRow.insertCell(-1);
            newCell.innerHTML = jsonResult[i].isbn;

            var newCell = newRow.insertCell(-1);
            newCell.innerHTML = jsonResult[i].iteminfo.title;

            var newCell = newRow.insertCell(-1);
            newCell.innerHTML = "<input type=\"number\" class=\"item_qty\" id=\"qty_\""+jsonResult[i].isbn+"\" value=\""+jsonResult[i].quantity+"\">";

        }

        document.getElementById("cartDiv").style.display = "block";
    }
};

function setItemCart(isbn, quantity)
{
    var sessionGUID = checkSession(false);
    if (sessionGUID != undefined){
        var xmlhttp = new XMLHttpRequest();
        var postData = {"action": "additem", "sessionGUID": sessionGUID, "isbn": isbn, "quantity": quantity};
        xmlhttp.open("POST", apiURL+"/getCart", false);
        xmlhttp.send(JSON.stringify(postData));
        var result = xmlhttp.responseText;
        var jsonResult = JSON.parse(result);
        if (jsonResult['quantity'] == quantity){
            if(quantity>0)
            {
                setAlertBanner("success","Item successfully added to cart");
            }
            else
            {
                setAlertBanner("success","Item successfully removed from the cart");
            }

        }
        else{
            console.log(jsonResult)
            setAlertBanner("danger","Item was not successfully added to the cart");
        }

    }
}

function checkItemCart(isbn)
{
    var sessionGUID = checkSession(false);
    if (sessionGUID != undefined){
        var xmlhttp = new XMLHttpRequest();
        var postData = {"action": "checkitem", "sessionGUID": sessionGUID, "isbn": isbn};
        xmlhttp.open("POST", apiURL+"/getCart", false);
        xmlhttp.send(JSON.stringify(postData));
        var result = xmlhttp.responseText;
        var jsonResult = JSON.parse(result);
        return jsonResult
    }
}

function deleteSession()
{
    Cookies.remove("sessionGUID");
};

function hideLoginForm()
{
    if(checkSession()!=undefined)
    {
        document.getElementById("loginForm").style.display="none";
        document.getElementById("logoutForm").style.display="block";
    }
    else
    {
        document.getElementById("loginForm").style.display="block";
        document.getElementById("logoutForm").style.display="none";
    }
}