const exc_url = `${import.meta.env.VITE_API_URL}/${import.meta.env.VITE_API_VERSION}/${import.meta.env.VITE_API_RT}/${import.meta.env.VITE_API_QS}`;

const get_exchange = function(data, loading) {
    let model = { module: 'models.m_finance', model: 'Exchange' }
    if (data.hasOwnProperty('limit')) {
      model['limit'] = data.limit
    }
    let mp = new URLSearchParams(model);
    return fetch(`${exc_url}?${mp}`, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
          "accept": 'application/json',
          "Content-Type": 'application/json'
        },
        body: JSON.stringify(data)
      }).then(response => {
        loading.value = false;
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes("application/json")) {
          msge = "Oops, we haven't got JSON!"
          error.value = msge;
          throw new TypeError(msge);
        }
        return response.json()
      })
}

const formatCurrency = (value) => {
  if (typeof value !== 'number') {
    alert('Invalid input! Please enter a valid number.');
    return;
  }
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}


export { get_exchange, formatCurrency }