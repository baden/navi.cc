// Generated by CoffeeScript 1.3.3
'use strict';

describe("filter", function() {
  beforeEach(module("app.filters"));
  return describe("interpolate", function() {
    beforeEach(module(function($provide) {
      $provide.value("version", "TEST_VER");
    }));
    return it("should replace VERSION", inject(function(interpolateFilter) {
      return expect(interpolateFilter("before %VERSION% after")).toEqual("before TEST_VER after");
    }));
  });
});
