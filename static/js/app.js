'use strict';

var HueApp = new Vue({
  el: '#app',

  data: {
    lights: {}
  },

  created: function () {
    this.getStatus();
  },

  methods: {
    getStatus: function () {
      var that = this;
      $.get('/status', function (responseData) {
        if (responseData.success) {
          that.lights = responseData.status;
        }
      }, 'json');
    },

    isLightOn: function (light) {
      return light.state.on;
    }
  }
});
