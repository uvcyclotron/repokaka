var pubSubSubscriber = pubSubHubbub.createServer(options);
var topic = "http://testetstetss.blogspot.com/feeds/posts/default";
var hub = "http://pubsubhubbub.appspot.com/";

pubSubSubscriber.on("subscribe", function(data){
    console.log(data.topic + " subscribed");
});

pubSubSubscriber.listen(port);

pubsub.on("listen", function(){
    pubSubSubscriber.subscribe(topic, hub, function(err){
        if(err){
            console.log("Failed subscribing");
        }
    });
});
