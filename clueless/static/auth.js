
export function loginUser(username, password){
  console.log("loginUser()");
  const url = "/api/auth/jwt/login";

  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);
  params.append('grant_type', '');
  params.append('client_secret', '');
  params.append('scope', '');

  axios.post(url, params)
    .then((response) => {
      console.log(response.data);
      const token = response.data["access_token"]
      console.log(`Logged in, setting cookie ${token}`)
      document.cookie = `token=${token}`;

    })
    .catch( function(error) {
      console.log(error)
    });
}
     
export function verify(token){
  console.log("verify()");
  const url = "/api/auth/whoami";

  //token = getCookie("token")

  console.log(token)

  axios.get(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    }
  })
    .then((response) => {
      console.log(response.data);
      console.log("Verified")
      document.cookie = "token=" + response.data["access_token"];

      return response.data
      
    })
    .catch(function(error) {
      console.log(error)
      console.log("Not logged in")
      window.location.href = "/login";
    });
}

