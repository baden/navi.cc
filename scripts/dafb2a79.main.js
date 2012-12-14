require.config({
  shim: {
  },

  paths: {
    hm: 'vendor/hm',
    esprima: 'vendor/esprima',
    jquery: 'vendor/jquery.min'
  }
});

require(['app', 'lib'], function(app, lib) {
  // use app here
  console.log(app);
  console.log(lib);

  console.log('angular is ', angular);

});
