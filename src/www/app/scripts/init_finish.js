"use strict";

(function(window) {

    window.config.inits.push(function(){
        console.log(['== Last init (TBD!). Config:', config]);
    });
    config.inits.forEach(function(single){single();});
    delete config.inits;

    setTimeout(function(){document.body.removeChild(document.getElementById('loading_div'));}, 200);

//log('finish');


})(window);
