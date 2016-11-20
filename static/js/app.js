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
          var lights = responseData.status;
          that.lights = Object.keys(lights)
            .reduce(function (acc, k) {
              var light = lights[k];
              light['id'] = k;
              acc[k] = light;
              return acc;
            }, {});
        }
      }, 'json');
    },

    isLightOn: function (light) {
      return light.state.on;
    },

    toggleLight: function (light) {
      var that = this;
      var url = '/status/' + light.id;
      var newState = !this.isLightOn(light);

      $.post(url, {'on': newState}, function (responseData) {
        if (responseData.success) {
          light.state.on = newState;
        } else {
          console.error('Could not set state: ' + responseData);
        }
      }, 'json');
    }
  }
});
