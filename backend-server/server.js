const express = require("express");
const ejs = require("ejs");
const bodyParser = require("body-parser");
// const mongoose = require("mongoose");
const unirest = require("unirest");

const app = express();


app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));
app.set("view engine", "ejs");


app.get("/", function (req, res) {
    res.render("index");
});

app.post("/currloc", function (req, res) {
    var apiCall = unirest("GET",
        "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"
    );
    apiCall.headers({
        "x-rapidapi-host": "ip-geolocation-ipwhois-io.p.rapidapi.com",
        "x-rapidapi-key": "srclZqaa9imshAk9Xzz55u27oltLp1SqdiFjsnmva9PTpf2j3f"
    });
    apiCall.end(function (result) {
        if (res.error) throw new Error(result.error);
        console.log(result.body);
        res.send(result.body);
    });
});

const PORT = 3000;
app.listen(PORT, function () {
    console.log("Server listening on port 3000");
});