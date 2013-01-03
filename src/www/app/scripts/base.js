"use strict";

(function(window) {
    var document = window.document;

window.log = function(){
  if(window.console){
    try{
            console.log( Array.prototype.slice.call(arguments) );
    } catch(ex) {
        log('Error in console', ex);
    }

  }
};

document.getElementById('login').onclick = function(){
    var username = document.getElementById('form_username');
    var password = document.getElementById('form_password');
    log('Login', username, password);
    return false;
};

})(window);
