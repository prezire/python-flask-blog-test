AuthMixin = {
  data: function () {
    return {
      logged: Auth.logged()
    };
  },
  mounted: function(){
    Auth.loggedOrRedirect();
  }
};