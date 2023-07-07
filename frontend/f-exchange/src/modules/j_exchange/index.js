const exc_url = `${import.meta.env.VITE_API_URL}/${import.meta.env.VITE_API_VERSION}/${import.meta.env.VITE_API_RT}/${import.meta.env.VITE_API_QS}`;

const get_exchange = function(data) {
    let model = { module: 'models.m_finance', model: 'Exchange' }
    let mp = new URLSearchParams(model);
    return fetch(`${exc_url}?${mp}`, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
          "accept": 'application/json',
          "Content-Type": 'application/json'
        },
        body: JSON.stringify(data)
      })
}

export default get_exchange