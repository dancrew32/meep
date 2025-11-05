const params = {
    query: `
      query { 
        hello
        echo(msg: "hi")
      }
    `
};
const options = {
    method: 'post',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
};
fetch('/graphql', options)
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
