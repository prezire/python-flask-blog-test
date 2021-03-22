class Auth{
  static login(){}
  
  static logout(){
    //TODO: Revoke API.
    sessionStorage.clear();
  }
  
  static logged(){
    let token = sessionStorage.getItem('token');
    
    let exp = sessionStorage.getItem('expires_on');
    let now = moment().format('YYYY-MM-DD hh:mm:ss');
    var diff = moment.duration(moment(exp).diff(moment(now)));
    return diff.seconds() > 0;
  }
  
  static tokenType() {
    return sessionStorage.getItem('type');
  }
  
  static loggedOrRedirect(){
    let b = Auth.logged();
    let forGuestPages = ['/admin/login', '/admin/register'];
    let inc = forGuestPages.includes(location.pathname);
    if(b) {
      if(inc){
        location.href = '/posts';
      }
    } else {
      if(!inc){
        location.href = forGuestPages[0];
      }
    }
  }
  
  static send(url, method, data={}){
    return axios.create({
      baseURL: API_BASE_URL,
      data: data,
      headers: {'Authorization': 'Bearer ' + Auth.tokenType()}
    })[method](url);
  }
}