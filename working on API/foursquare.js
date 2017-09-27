url='https://api.foursquare.com/v2/venues/4ef3e29ca69d3d38d5bd93a9?client_id=02ZEPEK2153SCZD1VCAJKT5O1JQIDPD4CS2XC1N50I12LJSG&client_secret=0LXE02XDG0G4POGWBHNTBMQU5ZYIPSJHLCOEHKC2HWIHGECZ&v=20130815&v=20170927&m=foursquare';
 
function Get(yoururl)
{
    var Httpreq = new XMLHttpRequest();
    Httpreq.open("GET",yoururl,false);
    Httpreq.send();
    return Httpreq.responseText;
}
 
var json_obj = JSON.parse(Get(url));
var category=json_obj.response.venue.categories[0].name;
var price_message = json_obj.response.venue.price;
var price_tier = json_obj.venue.price.tier
console.log(json_obj, price_message);