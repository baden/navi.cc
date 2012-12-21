"use strict";

(function(window) {

window.log = function(){
  if(window.console){
    try{
            console.log( Array.prototype.slice.call(arguments) );
    } catch(ex) {
        log('Error in console', ex);
    }

  }
};

})(window);
