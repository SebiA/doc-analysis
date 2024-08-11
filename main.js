async function getData() {
  const url = "YOUR_API_URL_HERE";
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    updateHTML(json);
  } catch (error) {
    console.error(error.message);
  }
}


function updateHTML(data){
  document.querySelector('#result').innerHTML = data['body'];
}


getData();

